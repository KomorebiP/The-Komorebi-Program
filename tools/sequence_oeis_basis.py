"""Exact shared basis for OEIS exponential-polynomial formula expressions.

Author: Komorebi P.

Computes Q-linear row rank and reproducible basis projections over the
coordinate functions n**j * lambda**n. These functions are linearly independent
for distinct nonzero lambda and nonnegative j in characteristic zero.

A projection is a theorem about the admitted EXACT FORMULAS for every local
n>=0. The map from raw OEIS term excerpts to the source formula is, separately,
finite-checked and not certified globally by this calculation.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sqlite3

from sequence_oeis_symbolic_network import load_formulas,formal_eval


def _nonzero(v):return {k:Q(x) for k,x in v.items() if x}


def _difference(a,b,k):
    out=dict(a)
    for axis,val in b.items():
        x=out.get(axis,Q(0))-k*val
        if x:out[axis]=x
        else:out.pop(axis,None)
    return out


def complexity(row):
    e=row['expression']
    return (len(e),sum(len(p) for p in e.values()),
            sum(len(str(v)) for p in e.values() for v in p),row['oeis_id'])


def coordinate_vectors(records):
    axes=sorted({(int(rate),j) for x in records.values()
                 for rate,p in x['expression'].items() for j,coef in enumerate(p) if coef})
    index={axis:i for i,axis in enumerate(axes)}
    vectors={}
    for sid,record in records.items():
        vectors[sid]={index[int(rate),j]:Q(x)
                      for rate,p in record['expression'].items()
                      for j,x in enumerate(p) if x}
    return axes,vectors


def shared_basis(records):
    axes,vectors=coordinate_vectors(records)
    pivots={};basis=[]
    for rec in sorted(records.values(),key=complexity):
        sid=rec['oeis_id']; vec=dict(vectors[sid]); lift={sid:Q(1)}
        for pivot,(normalized,expression) in sorted(pivots.items()):
            if pivot in vec:
                coefficient=vec[pivot]
                vec=_difference(vec,normalized,coefficient)
                lift=_difference(lift,expression,coefficient)
        if vec:
            pivot=min(vec);scale=vec[pivot]
            pivots[pivot]=({k:x/scale for k,x in vec.items()},
                           {k:x/scale for k,x in lift.items() if x})
            basis.append(sid)
    projections={}
    for sid,original in sorted(vectors.items()):
        residual=dict(original);projection={}
        for pivot,(normalized,expression) in sorted(pivots.items()):
            if pivot in residual:
                a=residual[pivot]
                residual=_difference(residual,normalized,a)
                projection=_difference(projection,expression,-a)
        if residual:raise ArithmeticError('basis does not span admitted exact formula '+sid)
        if any(base not in basis for base in projection):
            raise ArithmeticError('nonbasis expression in linear projection')
        recon={}
        for base,a in projection.items():
            recon=_difference(recon,vectors[base],-a)
        if recon!=original:raise ArithmeticError('basis reconstruction not exact for '+sid)
        projections[sid]=projection
    return axes,vectors,basis,projections


def build(db,*,output=None,basis_output=None):
    records,conflicts=load_formulas(db)
    axes,vectors,basis,proj=shared_basis(records)
    file_hash=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
    report=[];size=Counter()
    for sid,combination in proj.items():
        src=records[sid]
        # Independent functional controls, not a replacement for symbolic proof.
        for n in (0,1,2,7,13,31):
            left=formal_eval(src['expression'],n)
            right=sum(a*formal_eval(records[b]['expression'],n) for b,a in combination.items())
            if left!=right:raise ArithmeticError('functional control disagrees with exact projection')
        size[len(combination)]+=1
        report.append({'target':sid,'target_formula_id':src['formula_id'],
                      'source_sha256':src['record_sha256'],
                      'terms_checked':src['checked_terms'],
                      'linear_combination':[{'source':s,'coefficient':str(a),
                          'source_formula_id':records[s]['formula_id'],
                          'source_sha256':records[s]['record_sha256']}
                          for s,a in sorted(combination.items())],
                      'scope':'all-index Q-linear formula identity at local index n>=0; OEIS infinite identification finite-checked'})
    report.sort(key=lambda x:x['target'])
    meta={'source_count':len(records),'independent_coordinate_axes':len(axes),
          'basis_rank':len(basis),'basis_sequences':basis,
          'compression_source_count_per_basis':str(Q(len(records),len(basis))) if basis else None,
          'projection_support_histogram':dict(sorted(size.items())),
          'formulas_with_conflicts':conflicts,
          'proof':'Sparse rational Gaussian elimination with exact independent coordinate vectors n^j*lambda^n; every reported target linear combination was reconstructed identically in Q and checked at six additional indices',
          'scope':'Conditional all-index formula identities, not global OEIS sequence equality or measured runtime improvement'}
    if output:
        output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
        with output.open('w',encoding='utf-8') as fh:
            for row in report:fh.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
    if basis_output:
        basis_output=Path(basis_output);basis_output.parent.mkdir(parents=True,exist_ok=True)
        basis_output.write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return meta


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--basis-output',type=Path,required=True)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        result=build(db,output=args.output,basis_output=args.basis_output)
    print(json.dumps({key:val for key,val in result.items() if key!='basis_sequences'},indent=2))

if __name__=='__main__':main()
