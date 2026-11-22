"""Exact rational-OGF and shared-state transfers for recurrence-defined sequences.

Author: Komorebi P.

For a linear recurrence with initial vector v and coefficients c, the OGF is
P(x)/Q(x), Q(x)=1-sum(c_i*x**(i+1)), with a finite, exactly computed P.
The identity follows by equating coefficients and is global for the supplied
recurrence definition. It does not independently establish that all terms of
an OEIS entry agree with a claimed recurrence.

A/B is represented as a Laurent monomial x**shift times a rational function
with nonzero denominator constant term. Negative shifts are legitimate.
All arithmetic uses fractions.Fraction and integer coefficients.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path
import sqlite3

from oeis_formula_database import evaluate
from sequence_transfer_miner import _solve_unique,_hash_terms


def trim(p):
    p=[Q(x) for x in p]
    while len(p)>1 and p[-1]==0:p.pop()
    return p


def pmul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)


def psub(a,b):
    return trim([(a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])


def pdivmod(a,b):
    a,b=trim(a),trim(b)
    if b==[0]:raise ZeroDivisionError('zero polynomial')
    out=[Q(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b)
        factor=a[-1]/b[-1]
        out[k]+=factor
        a=psub(a,[Q(0)]*k+[factor*t for t in b])
    return trim(out),a


def gcdpoly(a,b):
    a,b=trim(a),trim(b)
    while b!=[0]:
        _,r=pdivmod(a,b)
        a,b=b,r
    return trim([x/a[-1] for x in a]) if a!=[0] else [Q(1)]


def ogf_from_recurrence(spec):
    if not isinstance(spec,dict) or spec.get('op')!='linear_recurrence':
        return None
    init=spec.get('initial');coef=spec.get('coefficients')
    if (not isinstance(init,list) or not isinstance(coef,list) or
        not init or len(init)!=len(coef) or
        any(type(i) is not int for i in init+coef)):
        return None
    degree=len(init)
    q=[Q(1)]+[-Q(c) for c in coef]
    p=[Q(init[n])-sum(Q(coef[j-1])*init[n-j] for j in range(1,n+1))
       for n in range(degree)]
    return {'P':trim(p),'Q':trim(q),'initial':init,'coefficients':coef}


def rational_ogf_filter(source,target):
    """Exactly returns target(x)/source(x) as x^shift * N(x)/D(x)."""
    if source is None or target is None:return None
    n=pmul(target['P'],source['Q'])
    d=pmul(source['P'],target['Q'])
    if n==[0] or d==[0]:return None
    def valuation(p):
        return next(i for i,x in enumerate(p) if x)
    sn,sd=valuation(n),valuation(d)
    power=sn-sd
    n=n[sn:];d=d[sd:]
    factor=gcdpoly(n,d)
    n,rn=pdivmod(n,factor);d,rd=pdivmod(d,factor)
    if rn!=[0] or rd!=[0]:raise AssertionError('polynomial gcd is not exact')
    scale=d[0]
    return {'shift':power,'numerator':[str(x/scale) for x in n],
            'denominator':[str(x/scale) for x in d],
            'interpretation':'target OGF = x^shift*(N/D)*source OGF over Q((x))'}


def _coefficients(spec,count):
    init=spec['initial'];c=spec['coefficients']
    d=len(init);a=list(init)
    for n in range(d,count):
        a.append(sum(c[j]*a[n-j-1] for j in range(d)))
    return a[:count]


def same_kernel_projection(source,target):
    """Find b_n=sum_j alpha_j*a_(n+j), with recurrence proof for all n."""
    if source is None or target is None or source['coefficients']!=target['coefficients']:
        return None
    d=len(source['initial'])
    av=_coefficients(source,3*d+12)
    bv=_coefficients(target,3*d+12)
    # All shifts of a recurrence solution satisfy the same recurrence.
    # First d target values determine every subsequent value uniquely.
    coefficients=_solve_unique([[Q(av[n+j]) for j in range(d)]
                                for n in range(d)], [Q(bv[n]) for n in range(d)])
    if coefficients is None:return None
    if any(sum(coefficients[j]*av[n+j] for j in range(d))!=bv[n]
           for n in range(2*d+10)):
        raise AssertionError('shared recurrence projection verification failed')
    return {'coefficients':[str(x) for x in coefficients],
            'source_shifts':list(range(d)),
            'proof':'Both expressions satisfy the same order-d linear recurrence and match d initial values'}


def ensure_schema(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS certified_recurrence_ogfs(
        formula_id TEXT PRIMARY KEY,
        oeis_id TEXT NOT NULL,
        offset INTEGER NOT NULL,
        numerator_json TEXT NOT NULL,
        denominator_json TEXT NOT NULL,
        coefficients_json TEXT NOT NULL,
        initial_json TEXT NOT NULL,
        checked_terms INTEGER NOT NULL,
        source_digest TEXT NOT NULL,
        proof_scope TEXT NOT NULL CHECK(proof_scope='rational_ogf_of_supplied_recurrence')
    );
    CREATE INDEX IF NOT EXISTS idx_recurrence_ogf_source ON certified_recurrence_ogfs(oeis_id);
    CREATE TABLE IF NOT EXISTS certified_recurrence_projections(
        source_formula_id TEXT NOT NULL,
        target_formula_id TEXT NOT NULL,
        source_oeis_id TEXT NOT NULL,
        target_oeis_id TEXT NOT NULL,
        coefficients_json TEXT NOT NULL,
        checked_terms INTEGER NOT NULL,
        source_digests_json TEXT NOT NULL,
        proof_scope TEXT NOT NULL CHECK(proof_scope='same_linear_recurrence_initial_value_proof'),
        PRIMARY KEY(source_formula_id,target_formula_id)
    );
    ''')


def certify(db,max_checks=32):
    ensure_schema(db)
    db.execute('DELETE FROM certified_recurrence_ogfs')
    db.execute('DELETE FROM certified_recurrence_projections')
    records=[];stats=Counter()
    for fid,sid,raw_spec,offset,terms_raw,status in db.execute('''
        SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,f.verification
        FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE f.origin='komorebi_curated' AND f.evaluator_json IS NOT NULL
        ORDER BY s.oeis_id,f.formula_id'''):
        if status!='finite_checked' or offset!=0:
            # Evaluator index n=0 begins at its recurrence initial vector.
            # Nonzero OEIS offsets need a separate index-alignment proof.
            continue
        spec=json.loads(raw_spec)
        canonical=ogf_from_recurrence(spec)
        if canonical is None:continue
        observed=[int(x) for x in json.loads(terms_raw)]
        checked=min(len(observed),max_checks)
        if checked<8 or _coefficients(canonical,checked)!=observed[:checked]:
            stats['rejected']+=1;continue
        if any(evaluate(spec,offset+n)!=observed[n] for n in range(checked)):
            stats['rejected']+=1;continue
        digest=_hash_terms(offset,tuple(observed))
        db.execute('''INSERT INTO certified_recurrence_ogfs VALUES (?,?,?,?,?,?,?,?,?,?)''',
                   (fid,sid,offset,json.dumps([str(x) for x in canonical['P']]),
                    json.dumps([str(x) for x in canonical['Q']]),
                    json.dumps(canonical['coefficients']),json.dumps(canonical['initial']),
                    checked,digest,'rational_ogf_of_supplied_recurrence'))
        records.append((fid,sid,canonical,digest,checked))
        stats['certified_ogf_formulas']+=1
    for fid,sid,defn,digest,checked1 in records:
        for fid2,sid2,defn2,digest2,checked2 in records:
            if sid==sid2:continue
            # Store only same-kernel projections. Other exact OGF filters are
            # computed on demand to avoid O(S^2) materialized edges.
            projection=same_kernel_projection(defn,defn2)
            if projection is None:continue
            db.execute('''INSERT INTO certified_recurrence_projections VALUES (?,?,?,?,?,?,?,?)''',
                       (fid,fid2,sid,sid2,json.dumps(projection['coefficients']),
                        min(checked1,checked2),json.dumps({sid:digest,sid2:digest2},sort_keys=True),
                        'same_linear_recurrence_initial_value_proof'))
            stats['certified_shared_state_projections']+=1
    db.commit()
    return dict(stats,scope='Exact theorems for supplied recurrence definitions; external OEIS identification is not globally established')


def load_filter(db,source_id,target_id):
    rows={}
    for sid in (source_id,target_id):
        data=db.execute('''SELECT numerator_json,denominator_json,coefficients_json,initial_json
            FROM certified_recurrence_ogfs WHERE oeis_id=? LIMIT 1''',(sid,)).fetchone()
        if data is None:return None
        p,q,c,v=(json.loads(x) for x in data)
        rows[sid]={'P':[Q(x) for x in p],'Q':[Q(x) for x in q],
                   'coefficients':c,'initial':v}
    return rational_ogf_filter(rows[source_id],rows[target_id])


def materialize_projections(db):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='certified_recurrence_projections'").fetchone():return 0
    from sequence_transfer_graph import _edge
    count=0
    for fid,sid,tid,did,c_raw,checked,d_raw,scope in db.execute('SELECT * FROM certified_recurrence_projections'):
        # Database column order source_formula,target_formula,source_oeis,target_oeis.
        hashes=json.loads(d_raw)
        good=True
        for seq in (tid,did):
            row=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(seq,)).fetchone()
            if row is None or _hash_terms(row[0],tuple(int(x) for x in json.loads(row[1])))!=hashes[seq]:
                good=False;break
        if not good:continue
        coeff=json.loads(c_raw)
        rhs=' + '.join(f'({a})*a(n+{j})' for j,a in enumerate(coeff) if Q(a))
        _edge(db,'FORMULA:'+fid,'FORMULA:'+sid,'shared_recurrence_projection',
              'formula_algebra',f'b(n)={rhs}; n>=0 relative to stored initial offsets',
              'Proof: equal constant-coefficient recurrence and d matching initial values for the declared evaluators; '
              'no independent proof of infinite OEIS identification',checked,
              'O(d) arithmetic given source shifted terms',f'https://oeis.org/{did}',{'coefficients':coeff})
        count+=1
    return count


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--from-id');p.add_argument('--to-id')
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        if args.from_id or args.to_id:
            if not args.from_id or not args.to_id:p.error('both --from-id and --to-id required')
            print(json.dumps(load_filter(db,args.from_id,args.to_id),indent=2))
        else:print(json.dumps(certify(db),indent=2))


if __name__=='__main__':main()
