"""Exact polyphase hypergeometric and Pochhammer lifts.

Author: Komorebi P. Works on finite-checked evaluator expressions, not
arbitrary OEIS prose. Every result is an exact algebraic identity between
specified formulas, valid from the recorded non-singular tail.
"""
from __future__ import annotations
import argparse,json,sqlite3
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from sequence_ratio_certificates import Ratio,derive_ratio,ratio_polynomials
from sequence_holonomic_compiler import normalize_operator, peval, fraction_eval


def phase_ratio(r,start,modulus,residue):
    if type(modulus) is not int or modulus<1 or not 0<=residue<modulus:
        raise ValueError('invalid polyphase parameters')
    out=Ratio();out.scalar=r.scalar**modulus
    for j in range(modulus):
        for (a,b),power in r.factors.items():
            if power:out.factor(a*modulus,a*(start+residue+j)+b,power)
    if not out.certified(0):raise ArithmeticError('phase has nonpositive ratio factor')
    return out


def reduce_hypergeo(poch):
    """A_n=b0 lambda^n * prod(upper)_n/prod(lower)_n.

    Its OGF is b0 * pFq(upper plus 1; lower; lambda*x).
    Cancel matching parameters without changing exact coefficients.
    """
    u=[F(1)]+[F(x) for x in poch['upper']]
    l=[F(x) for x in poch['lower']]
    for x in list(u):
        if x in l:
            u.remove(x);l.remove(x)
    return {'numerator_parameters':[str(x) for x in sorted(u)],
            'denominator_parameters':[str(x) for x in sorted(l)],
            'argument_scale':poch['multiplier'],
            'meaning':'ordinary formal power series; no positive radius of convergence asserted'}


def lift(spec,source_sha,formula_id,oeis_id,start,modulus,residue,checks=4):
    base=fraction_eval(spec,start+residue)
    if not base:raise ValueError('phase base is zero')
    ratio=derive_ratio(spec,start)
    if ratio is None:raise ValueError('source has no exact hypergeometric ratio')
    phase=phase_ratio(ratio,start,modulus,residue)
    p,q=ratio_polynomials(phase)
    operator=normalize_operator([[-v for v in p],q])
    for t in range(checks):
        x=fraction_eval(spec,start+modulus*t+residue)
        y=fraction_eval(spec,start+modulus*(t+1)+residue)
        if peval(operator[0],t)*x+peval(operator[1],t)*y:
            raise AssertionError('polyphase recurrence does not hold')
    poch=phase.pochhammer(0)
    return {'formula_id':formula_id,'oeis_id':oeis_id,'source_sha256':source_sha,
            'mathematical_source_start':start,
            'modulus':modulus,'residue':residue,
            'base_value':str(base),'pochhammer':poch,
            'hypergeometric_ogf':reduce_hypergeo(poch),
            'polynomial_recurrence':[[str(v) for v in a] for a in operator],
            'proof_method':'multiply m successive exact factorial/binomial ratio identities and split each affine factor into Pochhammer products',
            'scope':'All-index formal identity for the supplied formula subsequence; OEIS identification finite-checked only'}


def compile_phases(db,holonomic,output,summary=None,moduli=(2,3,5)):
    counts=Counter();seen=set()
    path=Path(output);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8') as stream:
        for raw in Path(holonomic).open(encoding='utf8'):
            if not raw.strip():continue
            cert=json.loads(raw)
            if cert['unique_ratio_components']!=1 or cert['component_count']!=1:continue
            fid=cert['formula_id'];counts['eligible_formulas']+=1
            row=db.execute('SELECT evaluator_json FROM formulas WHERE formula_id=?',(fid,)).fetchone()
            if not row:continue
            spec=json.loads(row[0]);start=cert['mathematical_start']
            for m in moduli:
                for r in range(m):
                    counts['attempted_phases']+=1
                    try:x=lift(spec,cert['source_sha256'],fid,cert['oeis_id'],start,m,r)
                    except (ValueError,OverflowError,ArithmeticError):
                        counts['skipped']+=1;continue
                    stream.write(json.dumps(x,separators=(',',':'))+'\n')
                    counts['certified']+=1
                    seen.add(cert['oeis_id'])
    report={'status':'formal_polyphase_pochhammer_identity','eligible_formula_records':counts['eligible_formulas'],
            'attempted_phases':counts['attempted_phases'],'certified_phases':counts['certified'],
            'skipped_phases':counts['skipped'],'distinct_sequences':len(seen),
            'moduli':list(moduli),
            'scope':'All-index formal hypergeometric forms from evaluated formula definitions; OEIS global identity not certified'}
    if summary:Path(summary).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--db',type=Path,required=True)
    p.add_argument('--holonomic',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--summary',type=Path);a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:stats=compile_phases(db,a.holonomic,a.output,a.summary)
    print(json.dumps(stats,indent=2))
if __name__=='__main__':main()
