"""Exact symbolic transfer links between curated hypergeometric term formulas.

Author: Komorebi P.

We normalize factorial shifts to a common kernel:
    (a*n+b)! = (a*n)! * polynomial_factor(n)
(valid on the stated nonnegative factorial domain). The remainder contains
rational affine factors and an exponential q**n. Thus formulas with the same
factorial skeleton admit a closed symbolic quotient without interpolation.

Proof scope is ALWAYS identity of the two supplied evaluator expressions.
It is not an independently established infinite identity of OEIS entries.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import json
import math
import sqlite3
from pathlib import Path

from oeis_formula_database import evaluate
from sequence_ratio_certificates import affine
from sequence_transfer_miner import _hash_terms


class TermForm:
    def __init__(self):
        self.scalar=Q(1)
        self.rate=Q(1)
        self.linear=Counter()
        self.factorial=Counter()

    def apply(self,other,power=1):
        self.scalar*=other.scalar**power
        self.rate*=other.rate**power
        for f,e in other.linear.items():self.linear[f]+=e*power
        for f,e in other.factorial.items():self.factorial[f]+=e*power
        return self

    def factor(self,a,b,power=1):
        if not power:return
        if a==0:
            if b==0:raise ValueError('zero scalar term')
            self.scalar*=Q(b)**power
            return
        if a<0:
            a,b=-a,-b
            self.scalar*=Q(-1)**power
        g=math.gcd(a,b)
        self.scalar*=Q(g)**power
        self.linear[(a//g,b//g)]+=power

    def fact(self,a,b,power,start):
        if a<0 or a*start+b<0:
            raise ValueError('factorial domain not certified for all future indices')
        if not a:
            self.scalar*=Q(math.factorial(b))**power
            return
        self.factorial[a]+=power
        # Canonical base (a*n)!; shift with an exact finite product.
        if b>0:
            for j in range(1,b+1):self.factor(a,j,power)
        elif b<0:
            for j in range(b+1,1):self.factor(a,j,-power)

    def valid(self,start):
        return self.scalar!=0 and self.rate!=0 and all(
            not exp or a*start+b>0 for (a,b),exp in self.linear.items())

    def signature(self):
        return tuple(sorted((a,v) for a,v in self.factorial.items() if v))

    def quotient(self,other):
        return TermForm().apply(self).apply(other,-1)

    def simplified(self):
        return {'scalar':str(self.scalar),'rate':str(self.rate),
                'factors':[{'a':a,'b':b,'power':p} for (a,b),p in sorted(self.linear.items()) if p],
                'factorial_skeleton':[{'slope':a,'power':p} for a,p in self.signature()]}

    def value(self,n):
        out=self.scalar*self.rate**n
        for (a,b),e in self.linear.items():
            if e:out*=Q(a*n+b)**e
        for a,e in self.factorial.items():
            if e:out*=Q(math.factorial(a*n))**e
        return out

    def complexity(self):
        return sum(abs(p) for p in self.linear.values()) + 2*sum(abs(p) for p in self.factorial.values()) + int(self.rate!=1)


def term_form(ast,start,tr=(1,0)):
    """Normalize the restricted exact multiplicative grammar, or return None."""
    lin=affine(ast,tr)
    if lin is not None:
        a,b=lin
        try:
            result=TermForm();result.factor(a,b)
            return result if result.valid(start) else None
        except ValueError:return None
    if not isinstance(ast,dict):return None
    op=ast.get('op')
    if op in ('mul','exact_div'):
        parts=[(p,1) for p in ast['args']] if op=='mul' else [(ast['num'],1),(ast['den'],-1)]
        out=TermForm()
        for expr,power in parts:
            item=term_form(expr,start,tr)
            if item is None:return None
            out.apply(item,power)
        return out if out.valid(start) else None
    if op=='pow':
        base=affine(ast['base'],tr);exp=affine(ast['exp'],tr)
        if base is None or exp is None:return None
        if exp[0]==0 and exp[1]>=0:
            result=term_form(ast['base'],start,tr)
            if result is None:return None
            return TermForm().apply(result,exp[1])
        if base[0]==0 and base[1] and exp[0]>=0 and exp[0]*start+exp[1]>=0:
            out=TermForm()
            out.scalar=Q(base[1])**exp[1]
            out.rate=Q(base[1])**exp[0]
            return out
        return None
    if op=='factorial':
        arg=affine(ast['arg'],tr)
        if arg is None:return None
        try:
            result=TermForm();result.fact(*arg,1,start)
            return result if result.valid(start) else None
        except ValueError:return None
    if op=='binomial':
        top=affine(ast['n'],tr);bottom=affine(ast['k'],tr)
        if top is None or bottom is None:return None
        rest=(top[0]-bottom[0],top[1]-bottom[1])
        try:
            out=TermForm()
            for (a,b),p in ((top,1),(bottom,-1),(rest,-1)):
                out.fact(a,b,p,start)
            return out if out.valid(start) else None
        except ValueError:return None
    if op=='at':
        newtr=affine(ast['index'],tr)
        return term_form(ast['body'],start,newtr) if newtr else None
    return None


def ensure_schema(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS certified_formula_transfers (
        transfer_id TEXT PRIMARY KEY,
        source_formula TEXT NOT NULL,
        target_formula TEXT NOT NULL,
        source_oeis_id TEXT NOT NULL,
        target_oeis_id TEXT NOT NULL,
        mathematical_start INTEGER NOT NULL,
        quotient_json TEXT NOT NULL,
        exact_checks INTEGER NOT NULL,
        source_digests_json TEXT NOT NULL,
        scope TEXT NOT NULL CHECK(scope='symbolic_quotient_of_curated_evaluators')
    );
    CREATE INDEX IF NOT EXISTS idx_certified_source ON certified_formula_transfers(source_oeis_id);
    CREATE INDEX IF NOT EXISTS idx_certified_target ON certified_formula_transfers(target_oeis_id);
    ''')


def discover(db,*,max_factor_complexity=4,max_exact_checks=16,include_exponential=False):
    """Emit small exact quotients, sharing kernel groups rather than N^2 guesses.

    For each kernel signature, retain a low-complexity hub and generate
    directional transfers only from that hub. Formulas are checked independently
    against the seed terms; checks are not the proof argument.
    """
    ensure_schema(db)
    db.execute('DELETE FROM certified_formula_transfers')
    groups=defaultdict(list)
    counts=Counter()
    for fid,sid,raw_spec,offset,raw_terms,status in db.execute('''
        SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,
               f.verification FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE f.origin='komorebi_curated' AND f.evaluator_json IS NOT NULL
        ORDER BY f.oeis_id,f.formula_id'''):
        if status!='finite_checked':continue
        terms=[int(x) for x in json.loads(raw_terms)]
        nonzero=next((i for i,t in enumerate(terms) if t),None)
        if nonzero is None:continue
        start=offset+nonzero
        try:spec=json.loads(raw_spec)
        except ValueError:continue
        form=term_form(spec,start)
        counts['attempted']+=1
        if form is None:
            counts['unsupported_or_singular']+=1
            continue
        # Domain starts at this n, not necessarily the entry's OEIS offset.
        key=(form.signature(),form.rate if not include_exponential else None)
        groups[key].append({'sid':sid,'fid':fid,'spec':spec,'offset':offset,
                            'terms':terms,'form':form,'start':start,
                            'digest':_hash_terms(offset,tuple(terms))})
        counts['normalized_formulas']+=1
    from hashlib import sha256
    for key,entries in groups.items():
        if len(entries)<2:continue
        # Prefer a simple NONCONSTANT source kernel. A hub a(n)=1 would
        # merely restate each polynomial as a factor times 1 and conceal
        # useful quotient relations such as n -> n**3.
        entries.sort(key=lambda x:(x['form'].complexity()==0,x['form'].complexity(),x['sid'],x['fid']))
        hub=entries[0]
        for other in entries[1:]:
            if hub['sid']==other['sid']:continue
            start=max(hub['start'],other['start'])
            quotient=other['form'].quotient(hub['form'])
            if quotient.signature() or not quotient.valid(start):continue
            if quotient.complexity()>max_factor_complexity:continue
            # Check the normalized expression and stored terms on a fresh
            # overlapping segment, without converting a finite check to proof.
            until=min(hub['offset']+len(hub['terms']),other['offset']+len(other['terms']),
                      start+max_exact_checks)
            checked=0
            try:
                for n in range(start,until):
                    a=evaluate(hub['spec'],n)
                    b=evaluate(other['spec'],n)
                    if a==0 or Q(b,a)!=quotient.value(n):raise ValueError('quotient mismatch')
                    if hub['terms'][n-hub['offset']]!=a or other['terms'][n-other['offset']]!=b:
                        raise ValueError('observed OEIS prefix differs')
                    checked+=1
            except (ValueError,ZeroDivisionError,OverflowError,KeyError,TypeError):
                counts['rejected_checks']+=1;continue
            if checked<8:continue
            target=other['sid'];source=hub['sid']
            data=quotient.simplified()
            doc=f'{source}->{target}:{hub["fid"]}->{other["fid"]}'
            tid=sha256(doc.encode()).hexdigest()[:24]
            db.execute('''INSERT INTO certified_formula_transfers VALUES (?,?,?,?,?,?,?,?,?,?)''',
                       (tid,hub['fid'],other['fid'],source,target,start,
                        json.dumps(data,sort_keys=True),checked,
                        json.dumps({source:hub['digest'],target:other['digest']},sort_keys=True),
                        'symbolic_quotient_of_curated_evaluators'))
            counts['symbolic_transfers']+=1
    db.commit()
    return dict(counts,groups=len(groups),scope='proved for supplied evaluator expressions; OEIS identification remains finite')


def materialize_transfers(db):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='certified_formula_transfers'").fetchone():
        return 0
    from sequence_transfer_graph import _edge, _node
    from sequence_transfer_miner import _hash_terms
    count=0
    for tid,fid1,fid2,sid1,sid2,start,qraw,checked,draw,scope in db.execute(
        'SELECT * FROM certified_formula_transfers'):
        digest=json.loads(draw)
        valid=True
        for sid in (sid1,sid2):
            item=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
            if not item or digest[sid]!=_hash_terms(item[0],tuple(int(x) for x in json.loads(item[1]))):
                valid=False;break
        if not valid:continue
        factor=json.loads(qraw)
        expr=' * '.join([factor['scalar'],f"({factor['rate']})^n"]+
             [f"({p['a']}n+{p['b']})^{p['power']}" for p in factor['factors']])
        _edge(db,'FORMULA:'+fid1,'FORMULA:'+fid2,
              'symbolic_kernel_quotient','formula_algebra',
              f'For n>={start}: evaluator({sid2},n) = ({expr}) * evaluator({sid1},n)',
              'Proved by factorial-shift normalization on the two supplied formula trees. '
              'OEIS equality is not globally established by finite matching.',
              checked,'not benchmarked',f'https://oeis.org/{sid2}',{'start':start,'transfer_id':tid})
        count+=1
    return count


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--allow-exponential',action='store_true')
    p.add_argument('--export',type=Path)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        result=discover(db,include_exponential=args.allow_exponential)
        if args.export:
            args.export.parent.mkdir(parents=True,exist_ok=True)
            with args.export.open('w',encoding='utf-8') as f:
                for tid,a,b,ida,idb,start,q,checked,hashes,scope in db.execute('SELECT * FROM certified_formula_transfers ORDER BY transfer_id'):
                    f.write(json.dumps({'id':tid,'source':ida,'target':idb,'source_formula':a,
                          'target_formula':b,'start':start,'quotient':json.loads(q),
                          'checked_terms':checked,'source_digests':json.loads(hashes),
                          'scope':scope},sort_keys=True)+'\n')
            result['export']=str(args.export)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
