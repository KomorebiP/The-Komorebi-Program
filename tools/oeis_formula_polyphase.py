"""Exact polyphase/multisection lifts from verified OEIS term formulas.

Author: Komorebi P.

These are parametrized subsequences of existing OEIS records, not claims of
new or distinct OEIS sequences. Every lift is conditional on the base formula.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from oeis_formula_database import connect, evaluate


def lift(spec, offset, modulus, residue):
    """Build P_{m,r}(n)=a(offset+m*n+r) as a safe evaluator JSON tree."""
    if not isinstance(offset,int) or not isinstance(modulus,int) or not isinstance(residue,int):
        raise TypeError('offset, modulus, and residue must be integers')
    if modulus < 1 or not 0 <= residue < modulus:
        raise ValueError('require m>=1 and 0<=r<m')
    return {'op':'at', 'index': {'op':'add', 'args': [offset,residue,
           {'op':'mul', 'args':[modulus, {'op':'n'}]}]}, 'body':spec}


def formula_info(db, oeis_id):
    row = db.execute('''SELECT s.offset,s.name,s.terms_json,f.formula_id,
      f.evaluator_json,f.proof_status,f.checked_terms FROM sequences s
      JOIN formulas f ON f.oeis_id=s.oeis_id
      WHERE s.oeis_id=? AND f.verification='finite_checked'
      ORDER BY CASE WHEN f.origin='komorebi_curated' THEN 0 ELSE 1 END,
        f.checked_terms DESC, f.ordinal LIMIT 1''',(oeis_id,)).fetchone()
    if row is None:
        raise ValueError('no finitely checked exact evaluator for this OEIS ID')
    offset,name,terms,fid,raw,proof_status,checked = row
    return dict(oeis_id=oeis_id,offset=offset,name=name,terms=json.loads(terms),
                formula_id=fid,evaluator=json.loads(raw),
                proof_status=proof_status,checked_terms=checked)


def compute(db,oeis_id,m,r,n):
    info=formula_info(db,oeis_id)
    if not isinstance(n,int) or n<0:
        raise ValueError('n must be nonnegative')
    compiled=lift(info['evaluator'],info['offset'],m,r)
    result=evaluate(compiled,n)
    reference_index=m*n+r
    reference=(info['terms'][reference_index] if reference_index<len(info['terms']) else None)
    if reference is not None and str(result)!=reference:
        raise ValueError('derived value disagrees with recorded OEIS reference')
    return {'oeis_id':oeis_id,'modulus':m,'residue':r,'index':n,
            'source_index':info['offset']+m*n+r,'exact_value':str(result),
            'reference_checked':reference is not None,
            'base_proof_status':info['proof_status'],
            'transformation':'a(offset + m*n + r) via exact substitution',
            'provenance':f'https://oeis.org/{oeis_id}'}


def build_catalogue(db,outfile,moduli=(2,3,4),sample_size=6):
    rows=db.execute('''SELECT DISTINCT oeis_id FROM formulas
      WHERE verification='finite_checked' AND evaluator_json IS NOT NULL
      AND oeis_id IS NOT NULL ORDER BY oeis_id''').fetchall()
    counts={'source_sequences':0,'parameterized_families':0,
            'preview_cases_checked':0, 'source_value_mismatches':0}
    out=Path(outfile)
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',encoding='utf-8',newline='\n') as handle:
        for (sid,) in rows:
            info=formula_info(db,sid)
            families=[]
            for m in moduli:
                for r in range(m):
                    sample=[]
                    for n in range(sample_size):
                        index=m*n+r
                        if index>=len(info['terms']):
                            break
                        value=evaluate(lift(info['evaluator'],info['offset'],m,r),n)
                        counts['preview_cases_checked']+=1
                        if str(value)!=info['terms'][index]:
                            counts['source_value_mismatches']+=1
                            raise ValueError(f'{sid} failed sample m={m},r={r},n={n}')
                        sample.append(str(value))
                    families.append(dict(m=m,r=r,reference_sample=sample))
            item={k:info[k] for k in ('oeis_id','name','offset','formula_id','proof_status','checked_terms')}
            item.update(meaning='a(offset + m*n + r), 0<=r<m and n>=0',
                        status='exact conditional substitution, not a new OEIS identity',
                        provenance=f'https://oeis.org/{sid}',
                        examples=families)
            handle.write(json.dumps(item,ensure_ascii=False)+'\n')
            counts['source_sequences']+=1
            counts['parameterized_families']+=1
    return dict(**counts,output=str(out),moduli=list(moduli))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    commands=p.add_subparsers(dest='command',required=True)
    calc=commands.add_parser('calculate')
    calc.add_argument('--id',required=True)
    calc.add_argument('--m',type=int,required=True)
    calc.add_argument('--r',type=int,required=True)
    calc.add_argument('--n',type=int,required=True)
    export=commands.add_parser('export')
    export.add_argument('--output',type=Path,required=True)
    export.add_argument('--moduli',type=int,nargs='+',default=[2,3,4])
    args=p.parse_args(argv)
    with connect(args.db) as db:
        if args.command=='calculate':
            result=compute(db,args.id,args.m,args.r,args.n)
        else:
            result=build_catalogue(db,args.output,tuple(args.moduli))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
