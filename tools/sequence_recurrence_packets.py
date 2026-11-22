"""Exact universal C-finite packet and polyphase compiler.

Author: Komorebi P.

For a_n with a_(n+d)=sum_(j=1)^d c_j*a_(n+d-j), put
    P(X)=X^d - c_1 X^(d-1) - ... - c_d.
Then X^n mod P(X) = sum_j k_j(n) X^j, and
    a_n=sum_j k_j(n)*a_j  (all n >= 0).

The packet is computed by modular exponentiation, O(d^2 log(n+1))
integer ring operations. Multiple sequences with the SAME recurrence share
exactly the same packet, differing only in their initial-state dot product.

For each phase b_n=a_(m*n+r), T is multiplication by X mod P,
    T_m=T^m, w=T^r*1, b_n=L T_m^n w.
Cayley-Hamilton proves a recurrence from det(z I-T_m). A second
observability certificate can lower its order, without guessing from a finite
OEIS prefix: the first d annihilator residuals are zero and the residual
itself obeys the original d-dimensional state recurrence.

Neither theorem establishes that an OEIS entry equals its curated evaluator
for all indices. OEIS equality is presently checked on available terms only.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sqlite3

from oeis_formula_database import fingerprint
from sequence_exponential_polynomial import infer
from sequence_transfer_miner import _hash_terms


def _check(coefficients, initial=None):
    if not isinstance(coefficients, (list, tuple)) or not coefficients:
        raise ValueError('nonempty recurrence coefficient vector required')
    if any(type(x) is not int for x in coefficients):
        raise ValueError('recurrence coefficients must be integers')
    if initial is not None and (len(initial)!=len(coefficients) or any(type(x) is not int for x in initial)):
        raise ValueError('invalid initial vector')
    if len(coefficients)>48:
        raise ValueError('order exceeds supported packet limit')


def multiply_mod(a,b,c):
    """Multiply two reduced polynomials modulo the monic recurrence polynomial."""
    _check(c)
    d=len(c)
    if len(a)!=d or len(b)!=d:raise ValueError('packet dimension mismatch')
    out=[0]*(2*d-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i+j]+=x*y
    for k in range(2*d-2,d-1,-1):
        x=out[k]
        if x:
            for j,v in enumerate(c,1):out[k-j]+=x*v
    return out[:d]


def x_packet(n,coefficients):
    """X^n mod P(X), integer coefficients, O(d^2 log n)."""
    _check(coefficients)
    if type(n) is not int or n<0:raise ValueError('index must be nonnegative')
    d=len(coefficients)
    out=[1]+[0]*(d-1)
    power=([coefficients[0]] if d==1 else [0,1]+[0]*(d-2))
    while n:
        if n&1:out=multiply_mod(out,power,coefficients)
        n>>=1
        if n:power=multiply_mod(power,power,coefficients)
    return out


def nth_term(initial,coefficients,n):
    _check(coefficients,initial)
    if type(n) is not int or n<0:raise ValueError('index must be nonnegative')
    if n<len(initial):return initial[n]
    return sum(x*y for x,y in zip(x_packet(n,coefficients),initial))


def batch_term(sequences, n):
    """Return exact terms, sharing one packet for each identical recurrence."""
    if type(n) is not int or n<0:raise ValueError('index must be nonnegative')
    groups=defaultdict(list)
    for sid,(initial,coefficients) in sequences.items():
        _check(coefficients,initial)
        groups[tuple(coefficients)].append((sid,initial))
    result={};counts={'recurrence_kernels':len(groups),'packet_exponentiations':0,'outputs':len(sequences)}
    for c,rows in groups.items():
        k=x_packet(n,list(c))
        counts['packet_exponentiations']+=1
        for sid,initial in rows:
            result[sid]=sum(x*y for x,y in zip(k,initial))
    return result,counts


def mat_identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]


def mat_mul(a,b):
    n=len(a)
    if len(b)!=n or any(len(row)!=n for row in a+b):raise ValueError('square matrices required')
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            u=a[i][k]
            if u:
                for j in range(n):
                    if b[k][j]:out[i][j]+=u*b[k][j]
    return out


def mat_pow(a,n):
    if type(n) is not int or n<0:raise ValueError('negative matrix exponent')
    out=mat_identity(len(a))
    while n:
        if n&1:out=mat_mul(out,a)
        n//=2
        if n:a=mat_mul(a,a)
    return out


def mat_vec(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]


def companion(coefficients):
    """Multiplication by X in Q[X]/(P), basis 1,X,...,X^(d-1)."""
    _check(coefficients)
    d=len(coefficients)
    out=[[0]*d for _ in range(d)]
    for j in range(d-1):out[j+1][j]=1
    for j,v in enumerate(reversed(coefficients)):out[j][-1]=v
    return out


def characteristic(a):
    """Return monic characteristic polynomial [1,k1,...,kd] (descending)."""
    n=len(a)
    if not n or any(len(row)!=n for row in a):raise ValueError('square matrix required')
    B=mat_identity(n)
    result=[1]
    for k in range(1,n+1):
        C=mat_mul(a,B)
        t=sum(C[i][i] for i in range(n))
        if t%k:raise ArithmeticError('integer characteristic coefficient failed')
        coeff=-t//k
        result.append(coeff)
        for i in range(n):C[i][i]+=coeff
        B=C
    if any(any(v for v in row) for row in B):
        raise ArithmeticError('Cayley-Hamilton witness failed')
    return result


def _solve(rows, y, dims):
    """Overdetermined exact rational linear system; free variables set to zero."""
    a=[[Fraction(x) for x in row]+[Fraction(v)] for row,v in zip(rows,y)]
    n=len(a);piv=[];position=0
    for col in range(dims):
        k=next((i for i in range(position,n) if a[i][col]),None)
        if k is None:continue
        a[k],a[position]=a[position],a[k]
        q=a[position][col];a[position]=[v/q for v in a[position]]
        for i in range(n):
            if i!=position and a[i][col]:
                q=a[i][col]
                a[i]=[u-q*v for u,v in zip(a[i],a[position])]
        piv.append(col);position+=1
    if any(not any(row[:dims]) and row[dims] for row in a):return None
    result=[Fraction(0)]*dims
    for rowindex,col in enumerate(piv):result[col]=a[rowindex][dims]
    return result


def minimal_scalar_phase(initial,coefficients,m,residue,phase_matrix=None):
    """Minimal scalar recurrence certified by observability, not extrapolation.

    If G(z) has state dimension d, every difference sequence generated from
    its d-dimensional state satisfies the characteristic recurrence of T^m.
    Hence d consecutive zero residuals certify equality for all n.
    """
    _check(coefficients,initial)
    d=len(coefficients)
    if type(m) is not int or m<1 or type(residue) is not int or not 0<=residue<m:
        raise ValueError('invalid polyphase parameters')
    Tm=phase_matrix if phase_matrix is not None else mat_pow(companion(coefficients),m)
    # Sequence values are exact evaluations of the supplied recurrence, not OEIS interpolation.
    b=[nth_term(initial,coefficients,m*n+residue) for n in range(2*d+1)]
    if all(v==0 for v in b[:d]):
        cert=[]
        if any(b):raise AssertionError('zero sequence observation contradicts state recurrence')
        return {'order':0,'coefficients':[],'initial':[],'checks':d,
                'proof':'First d zero observations and Cayley-Hamilton on the d-dimensional phase state'}
    for order in range(1,d+1):
        rows=[[b[n+j] for j in range(order)] for n in range(d)]
        targets=[b[n+order] for n in range(d)]
        sol=_solve(rows,targets,order)
        if sol is None:continue
        if any(q.denominator!=1 for q in sol):
            # Monic minimal polynomial of an integer transition matrix has integer coefficients.
            raise ArithmeticError('nonintegral minimal scalar recurrence')
        ascending=[int(q) for q in sol]
        # Direct residual check over the observability window and extra controls.
        if any(b[n+order]!=sum(ascending[j]*b[n+j] for j in range(order))
               for n in range(2*d-order+1)):
            raise ArithmeticError('minimal recurrence witness failed')
        # From the exact state, check (T_m^order - sum_j c_j*T_m^j)w is unobservable.
        w=x_packet(residue,coefficients)
        orbit=[w]
        for _ in range(order):orbit.append(mat_vec(Tm,orbit[-1]))
        residual=[orbit[order][i]-sum(ascending[j]*orbit[j][i] for j in range(order))
                  for i in range(d)]
        for n in range(d):
            if sum(initial[i]*residual[i] for i in range(d)):
                raise ArithmeticError('observable state residual is nonzero')
            residual=mat_vec(Tm,residual)
        return {'order':order,'coefficients':ascending[::-1],
                'initial':b[:order], 'checks':d,
                'proof':'State observability: d exact zero residuals plus Cayley-Hamilton imply all n'}
    raise AssertionError('Cayley-Hamilton did not yield an order-d scalar recurrence')


def phase_certificate(initial, coefficients, m, residue):
    _check(coefficients,initial)
    if type(m) is not int or m<1 or type(residue) is not int or not 0<=residue<m:
        raise ValueError('invalid polyphase parameters')
    T=companion(coefficients)
    Tm=mat_pow(T,m)
    poly=characteristic(Tm)
    general_coeff=[-v for v in poly[1:]]
    minimal=minimal_scalar_phase(initial,coefficients,m,residue,Tm)
    return {'modulus':m,'residue':residue,'original_order':len(coefficients),
            'phase_characteristic':poly,'general_recurrence':general_coeff,
            'minimal':minimal,'scope':'exact identity for supplied recurrence and all n>=0'}


def ensure_schema(db):
    # Derived certificate tables are safely rebuilt when a previous prototype
    # used an incompatible column layout; source formula tables are untouched.
    expected={'recurrence_packet_kernels':5,'recurrence_packet_sources':10,
              'recurrence_packet_phases':13}
    for table,ncols in expected.items():
        columns=db.execute(f'PRAGMA table_info({table})').fetchall()
        if columns and len(columns)!=ncols:
            db.execute(f'DROP TABLE {table}')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS recurrence_packet_kernels(
      kernel_id TEXT PRIMARY KEY, recurrence_json TEXT NOT NULL,
      order_k INTEGER NOT NULL, linked_oeis_ids_json TEXT NOT NULL,
      proof_rule TEXT NOT NULL CHECK(proof_rule='quotient_ring_shift_packet')
    );
    CREATE TABLE IF NOT EXISTS recurrence_packet_sources(
      formula_id TEXT PRIMARY KEY, oeis_id TEXT NOT NULL, kernel_id TEXT NOT NULL,
      offset INTEGER NOT NULL, initial_json TEXT NOT NULL, source_hash TEXT NOT NULL,
      evaluator_hash TEXT NOT NULL, checked_terms INTEGER NOT NULL,
      derivation_json TEXT NOT NULL,
      scope TEXT NOT NULL CHECK(scope='supplied_recurrence_definition_plus_finite_OEIS_check')
    );
    CREATE TABLE IF NOT EXISTS recurrence_packet_phases(
      phase_id TEXT PRIMARY KEY, formula_id TEXT NOT NULL,
      oeis_id TEXT NOT NULL, modulus INTEGER NOT NULL, residue INTEGER NOT NULL,
      characteristic_json TEXT NOT NULL, general_recurrence_json TEXT NOT NULL,
      minimal_recurrence_json TEXT NOT NULL, minimal_initial_json TEXT NOT NULL,
      minimal_order INTEGER NOT NULL, observed_terms INTEGER NOT NULL,
      source_hash TEXT NOT NULL,
      proof_scope TEXT NOT NULL CHECK(proof_scope='Cayley_Hamilton_and_state_observability')
    );
    CREATE INDEX IF NOT EXISTS recurrence_packet_phase_by_source
        ON recurrence_packet_phases(oeis_id,modulus,residue);
    ''')


def compile_db(db,*,max_modulus=8,max_checks=32):
    if type(max_modulus) is not int or not 2<=max_modulus<=48:
        raise ValueError('max_modulus must be in 2..48')
    ensure_schema(db)
    db.execute('DELETE FROM recurrence_packet_phases')
    db.execute('DELETE FROM recurrence_packet_sources')
    db.execute('DELETE FROM recurrence_packet_kernels')
    rows=db.execute('''SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,f.verification
        FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE f.origin='komorebi_curated' AND f.evaluator_json IS NOT NULL
        ORDER BY f.oeis_id,f.formula_id''').fetchall()
    classes=defaultdict(list)
    counts=Counter()
    chosen={}
    for fid,sid,raw,offset,observed,status in rows:
        if status!='finite_checked':continue
        spec=json.loads(raw)
        candidate=infer(spec,offset)
        if candidate is None:continue
        initials=candidate['initial'];c=candidate['coefficients']
        terms=[int(x) for x in json.loads(observed)]
        ncheck=min(max_checks,len(terms))
        if ncheck<8 or any(nth_term(initials,c,n)!=terms[n] for n in range(ncheck)):
            counts['rejected']+=1;continue
        counts['verified_symbolic_evaluators']+=1
        current=chosen.get(sid)
        if current is None or (len(c),len(raw),fid)<(len(current[2]['coefficients']),len(current[3]),current[0]):
            chosen[sid]=(fid,sid,candidate,raw,offset,terms,ncheck)
    cache={}
    for fid,sid,candidate,raw,offset,terms,ncheck in chosen.values():
        initials=candidate['initial'];c=candidate['coefficients']
        kernel_id=fingerprint('packet-kernel',c)
        classes[kernel_id].append(sid)
        sha=_hash_terms(offset,tuple(terms))
        db.execute('INSERT INTO recurrence_packet_sources VALUES (?,?,?,?,?,?,?,?,?,?)',
                   (fid,sid,kernel_id,offset,json.dumps(initials),sha,
                    hashlib.sha256(raw.encode()).hexdigest(),ncheck,
                    json.dumps({'method':candidate['method'],'proof':candidate['proof']}),
                    'supplied_recurrence_definition_plus_finite_OEIS_check'))
        counts['verified_sequence_definitions']+=1
        for m in range(2,max_modulus+1):
            cache_id=(kernel_id,m)
            if cache_id not in cache:
                Tm=mat_pow(companion(c),m)
                char=characteristic(Tm)
                cache[cache_id]=(Tm,char)
            Tm,char=cache[cache_id]
            for residue in range(m):
                minimal=minimal_scalar_phase(initials,c,m,residue,Tm)
                kept=len(range(residue,len(terms),m))
                for j in range(kept):
                    if nth_term(initials,c,m*j+residue)!=terms[m*j+residue]:
                        raise ArithmeticError('curated recurrence changed during polyphase verification')
                pid=fingerprint('recurrence-phase',fid,m,residue)
                db.execute('INSERT INTO recurrence_packet_phases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           (pid,fid,sid,m,residue,json.dumps(char),
                            json.dumps([-v for v in char[1:]]),
                            json.dumps(minimal['coefficients']),json.dumps(minimal['initial']),
                            minimal['order'],kept,sha,'Cayley_Hamilton_and_state_observability'))
                counts['certified_polyphase_formulas']+=1
                if minimal['order']<len(c):counts['order_reductions']+=1
    for kernel_id,sids in classes.items():
        sid=sids[0]
        c=chosen[sid][2]['coefficients']
        db.execute('INSERT INTO recurrence_packet_kernels VALUES (?,?,?,?,?)',
                   (kernel_id,json.dumps(c),len(c),json.dumps(sorted(sids)),
                    'quotient_ring_shift_packet'))
    db.commit()
    counts['shared_kernels']=len(classes)
    counts['derived_non_declared_sequences']=sum(candidate[2]['method']!='declared_linear_recurrence' for candidate in chosen.values())
    counts['reused_recursions']=sum(len(v)-1 for v in classes.values())
    counts['scanned_formula_records']=len(rows)
    counts['proof_scope']='all-index identities of curated recurrence definitions; OEIS matches only finite'
    return dict(counts)


def load_sources(db,oeis_ids):
    data={}
    for sid in oeis_ids:
        row=db.execute('''SELECT p.initial_json,k.recurrence_json,s.offset,s.terms_json,f.evaluator_json,f.verification
            FROM recurrence_packet_sources AS p JOIN recurrence_packet_kernels AS k ON p.kernel_id=k.kernel_id
            JOIN sequences s ON s.oeis_id=p.oeis_id JOIN formulas f ON f.formula_id=p.formula_id
            WHERE p.oeis_id=?''',(sid,)).fetchone()
        if row is None:raise ValueError('not a verified recurrence definition: '+sid)
        ini,c,offset,terms,raw,status=row
        term_digest=_hash_terms(offset,tuple(int(x) for x in json.loads(terms)))
        receipt=db.execute('SELECT source_hash,evaluator_hash FROM recurrence_packet_sources WHERE oeis_id=?',(sid,)).fetchone()
        if status!='finite_checked' or term_digest!=receipt[0] or hashlib.sha256(raw.encode()).hexdigest()!=receipt[1]:
            raise ValueError('stale recurrence receipt for '+sid)
        data[sid]=(json.loads(ini),json.loads(c))
    return data


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    build=sub.add_parser('compile');build.add_argument('--max-modulus',type=int,default=8)
    query=sub.add_parser('term');query.add_argument('--ids',nargs='+',required=True)
    query.add_argument('--n',type=int,required=True);query.add_argument('--summary',action='store_true')
    report=sub.add_parser('phase');report.add_argument('--id',required=True)
    report.add_argument('--modulus',type=int,required=True);report.add_argument('--residue',type=int,required=True)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        if args.command=='compile':out=compile_db(db,max_modulus=args.max_modulus)
        elif args.command=='term':
            values,stats=batch_term(load_sources(db,args.ids),args.n)
            out={'stats':stats,'n':args.n,'values':({k:{'digits':len(str(v)),
                'sha256':hashlib.sha256(str(v).encode()).hexdigest(),
                'leading':str(v)[:20],'trailing':str(v)[-20:]} for k,v in values.items()}
                if args.summary else {k:str(v) for k,v in values.items()})}
        else:
            row=db.execute('''SELECT characteristic_json,general_recurrence_json,
                minimal_recurrence_json,minimal_initial_json,minimal_order,observed_terms,proof_scope
                FROM recurrence_packet_phases WHERE oeis_id=? AND modulus=? AND residue=?''',
                (args.id,args.modulus,args.residue)).fetchone()
            if row is None:raise ValueError('phase not compiled')
            out={'id':args.id,'modulus':args.modulus,'residue':args.residue,
                 'characteristic':json.loads(row[0]),'global_recurrence':json.loads(row[1]),
                 'minimal_recurrence':json.loads(row[2]),'minimal_initial':json.loads(row[3]),
                 'minimal_order':row[4],'finite_overlap':row[5],'proof_scope':row[6]}
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
