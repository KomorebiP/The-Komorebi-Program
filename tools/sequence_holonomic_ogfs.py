"""Certified formal D-finite OGF operators from P-recursive formula certificates.

Author: Komorebi P.

For G(x)=sum_{n>=0}a_(n0+n)x^n and sum_j p_j(n)a_(n0+n+j)=0,
    sum_j x^(d-j) p_j(theta-j)(G(x)-sum_(i<j)a_(n0+i)x^i)=0,
where theta=x*d/dx, as an identity of formal power series over Q.
No analytic convergence is assumed. The OEIS association is still only
finite checked, and the original imported database is never modified.
"""
from __future__ import annotations
import argparse,json,sqlite3
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from sequence_holonomic_compiler import pshift,peval, fraction_eval


def construct(cert,ast,check=10):
    coeff=[tuple(F(v) for v in poly) for poly in cert['operator_coefficients']]
    d=len(coeff)-1
    n0=cert['mathematical_start']
    if d<1:raise ValueError('requires positive recurrence order')
    seed=[fraction_eval(ast,n0+j) for j in range(d)]
    operators=[{'x_power':d-j,
                'theta_polynomial':[str(c) for c in pshift(poly,-j)],
                'prefix_subtracted':[str(c) for c in seed[:j]]}
               for j,poly in enumerate(coeff)]
    for n in range(check):
        lhs=sum(peval(poly,n)*fraction_eval(ast,n0+n+j)
                for j,poly in enumerate(coeff))
        if lhs:raise AssertionError('formal OGF equation coefficient mismatch')
    return {'formula_id':cert['formula_id'],'oeis_id':cert['oeis_id'],
            'source_sha256':cert['source_sha256'],
            'evaluator_sha256':cert['evaluator_sha256'],
            'mathematical_start':n0,'order':d,
            'tail_initial_values':[str(x) for x in seed],
            'operator_theta_terms':operators,
            'identity':"sum_j x^(d-j) p_j(theta-j) (G(x)-sum_(i<j) g_i x^i)=0; theta=x*d/dx",
            'verification':'exact derivation from polynomial recurrence; sampled coefficient recheck',
            'scope':'formal OGF of supplied formula tail; not independent OEIS infinite identification'}


def compile_ogfs(db,certificates,output,summary=None):
    stats=Counter()
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8') as stream:
        for raw in Path(certificates).open(encoding='utf8'):
            if not raw.strip():continue
            cert=json.loads(raw);stats['attempted']+=1
            row=db.execute('SELECT evaluator_json FROM formulas WHERE formula_id=?',
                           (cert['formula_id'],)).fetchone()
            if not row:stats['unavailable_external_formula']+=1;continue
            ast=json.loads(row[0])
            rec=construct(cert,ast)
            stream.write(json.dumps(rec,separators=(',',':'))+'\n');stats['compiled']+=1
    result={'status':'certified_formal_ogf_operators',**stats,
            'scope':'All-index formal generating-function identities conditional on exact formula expression'}
    if summary:Path(summary).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,required=True)
    p.add_argument('--certificates',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--summary',type=Path)
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:report=compile_ogfs(db,a.certificates,a.output,a.summary)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
