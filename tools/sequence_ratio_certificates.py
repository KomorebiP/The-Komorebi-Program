"""Symbolic rational-ratio certificates for a restricted exact-formula DSL.

Author: Komorebi P.

Important scope: this proves an algebraic identity for the *curated expression*
given as a declarative evaluator. Agreement with OEIS excerpts is still only
finite numerical corroboration. It does NOT automatically prove that the OEIS
sequence is represented by that expression at every index.

No eval/exec, no external CAS dependency. Supported factors: nonzero affine
forms, affine-indexed factorials/binomials, integer powers, and products /
exact divisions of supported terms. Unsupported constructs are NOT guessed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sqlite3

from oeis_formula_database import evaluate
from sequence_transfer_miner import _hash_terms


def affine(ast, tr=(1,0)):
    """Return integer a,b such that ast evaluates to a*n+b, else None."""
    if type(ast) is int:return (0,ast)
    if not isinstance(ast,dict):return None
    op=ast.get('op')
    if op=='n':return tr
    if op=='add':
        parts=[affine(x,tr) for x in ast['args']]
        if any(x is None for x in parts):return None
        return (sum(x[0] for x in parts),sum(x[1] for x in parts))
    if op=='sub':
        x=affine(ast['args'][0],tr);y=affine(ast['args'][1],tr)
        return (x[0]-y[0],x[1]-y[1]) if x and y else None
    if op=='mul':
        product=(0,1)
        for item in ast['args']:
            x=affine(item,tr)
            if x is None or (product[0] and x[0]):return None
            product=(product[0]*x[1]+product[1]*x[0],product[1]*x[1])
        return product
    if op=='exact_div':
        x=affine(ast['num'],tr);y=affine(ast['den'],tr)
        if x is None or y is None or y[0] or y[1]==0:return None
        if x[0]%y[1] or x[1]%y[1]:return None
        return (x[0]//y[1],x[1]//y[1])
    if op=='at':
        newtr=affine(ast['index'],tr)
        return affine(ast['body'],newtr) if newtr else None
    return None


class Ratio:
    def __init__(self):
        self.scalar=Q(1)
        self.factors=Counter()

    def mul(self,other,power=1):
        self.scalar*=other.scalar**power
        for key,v in other.factors.items():
            self.factors[key]+=v*power
        return self

    def factor(self,a,b,power):
        if not power:return
        if not a and not b:raise ValueError('identically zero factor')
        if not a:
            self.scalar*=Q(b)**power
            return
        g=math.gcd(a,b)
        self.scalar*=Q(g)**power
        a//=g;b//=g
        if a<0:
            a=-a;b=-b
            self.scalar*=Q(-1)**power
        self.factors[(a,b)]+=power

    def certified(self,start):
        return all(v==0 or a*start+b>0 for (a,b),v in self.factors.items()) and self.scalar!=0

    def normalized(self):
        return {'multiplier':str(self.scalar),
                'factors':[{'a':a,'b':b,'power':p} for (a,b),p in sorted(self.factors.items()) if p]}

    def ratio_at(self,n):
        out=self.scalar
        for (a,b),p in self.factors.items():
            if p:out*=Q(a*n+b)**p
        return out

    def pochhammer(self,start):
        c=self.scalar
        up=[];down=[]
        for (a,b),power in sorted(self.factors.items()):
            if not power:continue
            c*=Q(a)**power
            v=str(Q(a*start+b,a))
            (up if power>0 else down).extend([v]*abs(power))
        return {'start':start,'multiplier':str(c),'upper':up,'lower':down,
                'formula':'a(start+t)=a(start)*multiplier^t*product((upper)_t)/product((lower)_t)'}


def derive_ratio(ast,start,tr=(1,0)):
    """Exact formal ratio E(n+1)/E(n) for the admitted structural grammar."""
    linear=affine(ast,tr)
    if linear is not None:
        a,b=linear
        if a==0 and b==0:return None
        r=Ratio()
        r.factor(a,b+a,+1)
        r.factor(a,b,-1)
        return r if r.certified(start) else None
    if not isinstance(ast,dict):return None
    op=ast.get('op')
    if op=='mul':
        r=Ratio()
        for child in ast['args']:
            x=derive_ratio(child,start,tr)
            if x is None:return None
            r.mul(x)
        return r if r.certified(start) else None
    if op=='exact_div':
        numerator=derive_ratio(ast['num'],start,tr)
        denominator=derive_ratio(ast['den'],start,tr)
        if numerator is None or denominator is None:return None
        numerator.mul(denominator,-1)
        return numerator if numerator.certified(start) else None
    if op=='pow':
        base=affine(ast['base'],tr)
        exponent=affine(ast['exp'],tr)
        if base is not None and base[0]==0 and base[1] and exponent is not None:
            slope,intercept=exponent
            if slope<0 or slope*start+intercept<0:return None
            r=Ratio();r.scalar=Q(base[1])**slope
            return r if r.certified(start) else None
        if exponent is not None and exponent[0]==0 and exponent[1]>=0:
            r=derive_ratio(ast['base'],start,tr)
            if r is None:return None
            x=Ratio().mul(r,exponent[1])
            return x if x.certified(start) else None
        return None
    if op=='factorial':
        arg=affine(ast['arg'],tr)
        if arg is None:return None
        a,b=arg
        if a<0 or a*start+b<0:return None
        r=Ratio()
        for j in range(1,a+1):r.factor(a,b+j,1)
        return r if r.certified(start) else None
    if op=='binomial':
        top=affine(ast['n'],tr);bottom=affine(ast['k'],tr)
        if top is None or bottom is None:return None
        rest=(top[0]-bottom[0],top[1]-bottom[1])
        if any(a<0 or a*start+b<0 for a,b in (top,bottom,rest)):
            return None
        r=Ratio()
        for (a,b),sgn in ((top,1),(bottom,-1),(rest,-1)):
            for j in range(1,a+1):r.factor(a,b+j,sgn)
        return r if r.certified(start) else None
    if op=='at':
        newtr=affine(ast['index'],tr)
        return derive_ratio(ast['body'],start,newtr) if newtr else None
    return None


def _conv(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def ratio_polynomials(r,start=0):
    numerator=[r.scalar];denominator=[Q(1)]
    for (a,b),p in r.factors.items():
        for _ in range(abs(p)):
            if p>0:numerator=_conv(numerator,[Q(a*start+b),Q(a)])
            elif p<0:denominator=_conv(denominator,[Q(a*start+b),Q(a)])
    return numerator,denominator


def matches_fit(db,sid,ratio,start):
    fit=db.execute('''SELECT mathematical_start,numerator_json,denominator_json
                     FROM rational_ratio_candidates WHERE oeis_id=?''',(sid,)).fetchone()
    if not fit:return None
    fit_start,praw,qraw=fit
    if fit_start!=start:return None
    p,q=ratio_polynomials(ratio,start)
    expected_p=[Q(x) for x in json.loads(praw)]
    expected_q=[Q(x) for x in json.loads(qraw)]
    def trim(x):
        while len(x)>1 and x[-1]==0:x.pop()
        return x
    return trim(_conv(p,expected_q))==trim(_conv(q,expected_p))


def ensure_schema(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS certified_formula_ratios(
        formula_id TEXT PRIMARY KEY,
        oeis_id TEXT NOT NULL,
        mathematical_start INTEGER NOT NULL,
        base_value TEXT NOT NULL,
        ratio_json TEXT NOT NULL,
        pochhammer_json TEXT NOT NULL,
        checked_terms INTEGER NOT NULL,
        matches_inferred_ratio INTEGER,
        source_digest TEXT NOT NULL,
        scope TEXT NOT NULL CHECK(scope='symbolic_identity_of_curated_evaluator')
    );
    CREATE INDEX IF NOT EXISTS certified_formula_ratio_sequence
      ON certified_formula_ratios(oeis_id);
    ''')


def certify(db,*,max_checks=25):
    """Certify supported evaluator syntax, NOT universal OEIS identification."""
    ensure_schema(db)
    db.execute('DELETE FROM certified_formula_ratios')
    counts=Counter()
    for fid,sid,raw_spec,offset,raw_terms,verified in db.execute('''
        SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,
               f.verification FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
        WHERE f.origin='komorebi_curated' AND f.evaluator_json IS NOT NULL
        ORDER BY s.oeis_id,f.formula_id'''):
        counts['attempted']+=1
        if verified!='finite_checked':
            counts['not_verified']+=1;continue
        terms=[int(x) for x in json.loads(raw_terms)]
        start_local=next((i for i,x in enumerate(terms) if x!=0),None)
        if start_local is None or start_local+2>=len(terms):
            counts['no_nondegenerate_tail']+=1;continue
        start=offset+start_local
        try:
            spec=json.loads(raw_spec)
            ratio=derive_ratio(spec,start)
            if ratio is None:
                counts['unsupported_or_singular']+=1;continue
            check=min(max_checks,len(terms)-start_local)
            if check<8:
                counts['too_few_terms']+=1;continue
            for t in range(check):
                val=evaluate(spec,start+t)
                if val!=terms[start_local+t]:
                    raise ValueError('source mismatch on tested prefix')
                if t+1<check and Q(evaluate(spec,start+t+1),val)!=ratio.ratio_at(start+t):
                    raise ValueError('derived ratio mismatches evaluator')
            # Base is a genuine exact evaluator output, not a floated estimate.
            base=str(evaluate(spec,start))
            assert int(base)!=0
            fit=matches_fit(db,sid,ratio,start)
            digest=_hash_terms(offset,tuple(terms))
            db.execute('''INSERT INTO certified_formula_ratios VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (fid,sid,start,base,json.dumps(ratio.normalized()),
                 json.dumps(ratio.pochhammer(start)),check,
                 int(fit) if fit is not None else None,digest,
                 'symbolic_identity_of_curated_evaluator'))
            counts['certified_formula_identities']+=1
            if fit is True:counts['fitted_ratios_confirmed']+=1
            elif fit is False:counts['fitted_ratios_refuted']+=1
        except (ValueError,TypeError,ZeroDivisionError,OverflowError,KeyError,AssertionError):
            counts['rejected']+=1
    db.commit()
    return dict(counts,scope='exact consequences of admitted evaluator expressions, NOT automatic OEIS global proofs')



def materialize_certificates(db):
    """Link symbolic formula algebra in the graph, never as OEIS proof routes."""
    if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='certified_formula_ratios'").fetchone():
        return 0
    from sequence_transfer_graph import _node, _edge
    total=0
    for fid,sid,start,base,r_raw,p_raw,checked,match,digest,scope in db.execute(
        'SELECT * FROM certified_formula_ratios'):
        row=db.execute('SELECT offset,terms_json FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
        if row is None or _hash_terms(row[0],tuple(int(t) for t in json.loads(row[1])))!=digest:
            continue
        prefix='CERT:'+fid
        poch=json.loads(p_raw)
        statement=(f'For the evaluator-defined sequence, a({start}+t) = {base}*'
                   f'({poch["multiplier"]})^t*prod_(u in {poch["upper"]})(u)_t/'
                   f'prod_(v in {poch["lower"]})(v)_t; domain t>=0')
        _node(db,prefix,'certified_formula_ratio','Exact ratio: '+sid,
              {'oeis_id':sid,'start':start,'formula_id':fid,'base':base,
               'pochhammer':poch,'scope':scope,'checked_terms':checked,
               'fitted_ratio_algebraically_agrees':bool(match) if match is not None else None})
        _edge(db,'FORMULA:'+fid,prefix,'exact_ratio_from_evaluator','formula_algebra',
              statement,'Proof by factorial and affine-ratio rules on the admitted expression. '
              'OEIS attribution is not established for all indices by finite matching.',
              checked,'not benchmarked',f'https://oeis.org/{sid}',{'start':start})
        total+=1
    return total


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--export',type=Path)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        result=certify(db)
        if args.export:
            args.export.parent.mkdir(parents=True,exist_ok=True)
            with args.export.open('w',encoding='utf-8') as f:
                for row in db.execute('SELECT * FROM certified_formula_ratios ORDER BY oeis_id,formula_id'):
                    fid,sid,start,base,ratio,poch,checked,match,digest,scope=row
                    data={'formula_id':fid,'oeis_id':sid,'start':start,'base':base,
                          'ratio':json.loads(ratio),'pochhammer':json.loads(poch),
                          'checked_terms':checked,'matches_finite_fit':match,
                          'source_digest':digest,'proof_scope':scope}
                    f.write(json.dumps(data,ensure_ascii=False,sort_keys=True)+'\n')
            result['export']=str(args.export)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
