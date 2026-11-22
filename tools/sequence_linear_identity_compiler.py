"""Automatic all-index cross-sequence arithmetic identities, without fitting.

Author: Komorebi P.

Canonicalize admitted formula DSL expressions into a finite exponential-
polynomial algebra with basis n^j * rate^n. Then compare exact rational
coefficients to prove products, sums, scalar multiples and shifted finite
differences. All identities hold for the supplied normalized evaluators for
all local n>=0. A finite OEIS prefix match is NOT an infinite OEIS proof.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path
import sqlite3

from sequence_exponential_polynomial import symbolic,p_add,p_scale,p_mul,ep_add,ep_mul
from sequence_transfer_miner import _hash_terms


def p_shift(p,k):
    if type(k) is not int or k<0:raise ValueError('nonnegative shift required')
    result=[Q(0)]*len(p)
    for j,a in enumerate(p):
        for i in range(j+1):result[i]+=a*comb(j,i)*k**(j-i)
    while len(result)>1 and result[-1]==0:result.pop()
    return result


def normalized(spec,offset):
    if type(offset) is not int or offset<0:return None
    e=symbolic(spec,offset)
    if e is None:return None
    return {rate:p_scale(p_shift(poly,offset),Q(rate)**offset) for rate,poly in e.items()}


def shifted(expr,k):
    return {rate:p_scale(p_shift(p,k),Q(rate)**k) for rate,p in expr.items()}


def scaled(expr,k):return {rate:p_scale(p,Q(k)) for rate,p in expr.items()}


def neg(expr):return scaled(expr,-1)


def key(expr):
    return tuple(sorted((int(rate),tuple(str(x) for x in poly))
                  for rate,poly in expr.items() if any(poly)))


def fprint(*items):return hashlib.sha256(json.dumps(items,sort_keys=True).encode()).hexdigest()[:32]



def _basis_vector(expr,coordinate):
    return [expr.get(rate,[Q(0)])[degree] if degree<len(expr.get(rate,[Q(0)])) else Q(0)
            for rate,degree in coordinate]


def _exact_solve(columns,y):
    """Solve A*x=y over Q for a tall matrix with exact Gaussian elimination."""
    d=len(columns)
    if d==0:return [] if not any(y) else None
    table=[[Q(columns[k][j]) for k in range(d)]+[Q(y[j])] for j in range(len(y))]
    pivot=[];nrow=0
    for col in range(d):
        ix=next((i for i in range(nrow,len(table)) if table[i][col]),None)
        if ix is None:continue
        table[ix],table[nrow]=table[nrow],table[ix]
        scale=table[nrow][col]
        table[nrow]=[u/scale for u in table[nrow]]
        for ix in range(len(table)):
            if ix!=nrow and table[ix][col]:
                v=table[ix][col]
                table[ix]=[u-v*w for u,w in zip(table[ix],table[nrow])]
        pivot.append(col);nrow+=1
    if any(not any(row[:d]) and row[d] for row in table):return None
    answer=[Q(0)]*d
    for j,col in enumerate(pivot):answer[col]=table[j][-1]
    return answer


def independent_transfer_basis(accepted):
    """Find a sparse exact source basis and all projections, no sample fitting."""
    coordinates=sorted({(int(rate),j) for row in accepted.values()
                        for rate,poly in row['expression'].items() for j in range(len(poly))})
    vect={sid:_basis_vector(record['expression'],coordinates) for sid,record in accepted.items()}
    # Prefer sparse, structurally simple source expressions; no runtime optimality claim.
    def complexity(sid):
        e=accepted[sid]['expression']
        return (sum(v!=0 for row in e.values() for v in row)+
                max(len(p)-1 for p in e.values())+
                2*(len(e)-1),sid)
    sources=sorted(accepted,key=complexity)
    basis=[]
    for sid in sources:
        if _exact_solve([vect[x] for x in basis],vect[sid]) is None:
            basis.append(sid)
    projections=[]
    for sid in sorted(accepted):
        coeff=_exact_solve([vect[x] for x in basis],vect[sid])
        if coeff is None:raise ArithmeticError('the reported basis did not span the source')
        if any(sum(coeff[j]*vect[x][i] for j,x in enumerate(basis))!=vect[sid][i]
               for i in range(len(coordinates))):
            raise ArithmeticError('basis projection failed exact algebra check')
        projections.append({'target':sid,'coefficients':
                            [{'source':source,'weight':str(c)}
                             for source,c in zip(basis,coeff) if c]})
    return {'sequences_with_symbolic_forms':len(accepted),'basis_size':len(basis),
            'basis':basis,'basis_coordinates':len(coordinates),
            'projections':projections,
            'source_hashes':{sid:accepted[sid]['terms_digest'] for sid in accepted},
            'scope':'all-index identities among curated, offset-aligned evaluator expressions'}

def discover(db,max_coefficient=3,max_shift=3):
    if max_coefficient<1 or max_coefficient>8 or max_shift<1 or max_shift>12:
        raise ValueError('coefficient/shift bounds exceeded')
    all_found=[]
    seen=set()
    accepted={}
    for fid,sid,raw_spec,offset,terms_raw,status in db.execute('''
        SELECT f.formula_id,f.oeis_id,f.evaluator_json,s.offset,s.terms_json,f.verification
        FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id
        WHERE f.origin='komorebi_curated' AND f.evaluator_json IS NOT NULL ORDER BY s.oeis_id'''):
        if status!='finite_checked':continue
        expr=normalized(json.loads(raw_spec),offset)
        if expr is None or not key(expr):continue
        values=[int(x) for x in json.loads(terms_raw)]
        record={'oeis_id':sid,'formula_id':fid,'expression':expr,
                'terms_digest':_hash_terms(offset,tuple(values)),
                'mathematical_offset':offset,'checked_terms':len(values)}
        # Keep the simplest admitted expression per OEIS ID.
        if sid not in accepted or len(str(expr))<len(str(accepted[sid]['expression'])):
            accepted[sid]=record
    inverse={}
    for sid,record in accepted.items():inverse.setdefault(key(record['expression']),[]).append(sid)
    ids=sorted(accepted)
    def add(operator,sources,target,parameters,statement):
        if target in sources:return
        label=(operator,tuple(sources),target,json.dumps(parameters,sort_keys=True))
        if label in seen:return
        seen.add(label)
        evidence={sid:accepted[sid]['terms_digest'] for sid in {*sources,target}}
        all_found.append({'id':fprint(label),'operator':operator,'sources':sources,
              'target':target,'parameters':parameters,'statement':statement,
              'formula_ids':{sid:accepted[sid]['formula_id'] for sid in {*sources,target}},
              'checked_terms':min(accepted[sid]['checked_terms'] for sid in {*sources,target}),
              'evidence':evidence,'proof':'exact canonical exponential-polynomial coefficient identity',
              'scope':'all n>=0 of curated formula evaluators; OEIS equality only finite checked'})
    # Difference / shift, including x(n+s)-x(n) = y(n), a theorem at all n.
    for src in ids:
        expr=accepted[src]['expression']
        for k in range(1,max_shift+1):
            target_expr=ep_add(shifted(expr,k),neg(expr))
            for tid in inverse.get(key(target_expr),[]):
                add('shift_difference',[src],tid,{'shift':k},f'b(n)=a(n+{k})-a(n)')
    # Exact pointwise products.
    for i,src in enumerate(ids):
        for second in ids[i:]:
            try:product=ep_mul(accepted[src]['expression'],accepted[second]['expression'])
            except ValueError:continue
            for tid in inverse.get(key(product),[]):
                add('pointwise_product',[src,second],tid,{},'c(n)=a(n)*b(n)')
    # Small signed integer linear combinations: this is a true hyperedge.
    choices=[i for i in range(-max_coefficient,max_coefficient+1) if i]
    for ix,src in enumerate(ids):
        for second in ids[ix+1:]:
            left,right=accepted[src]['expression'],accepted[second]['expression']
            for a in choices:
                for b in choices:
                    combination=ep_add(scaled(left,a),scaled(right,b))
                    for tid in inverse.get(key(combination),[]):
                        add('integer_linear_combination',[src,second],tid,
                            {'left':a,'right':b},f'c(n)={a}a(n)+({b})b(n)')
    # Avoid flooding with equivalent scalar multiples of exactly the same family.
    return {'source_expressions':len(ids),'exact_identities':len(all_found),
            'by_operator':dict(Counter(x['operator'] for x in all_found)),
            'basis':independent_transfer_basis(accepted), 'links':all_found}



def validate_identity_record(db, record):
    """Refuse stale source data and independently recheck the symbolic identity."""
    entries={}
    for sid in set(record['sources']+[record['target']]):
        fid=record['formula_ids'][sid]
        row=db.execute('''SELECT f.evaluator_json,f.verification,s.offset,s.terms_json
            FROM formulas f JOIN sequences s ON f.oeis_id=s.oeis_id
            WHERE f.formula_id=? AND s.oeis_id=?''',(fid,sid)).fetchone()
        if row is None or row[1]!='finite_checked':return False
        expr,status,offset,raw=row
        digest=_hash_terms(offset,tuple(int(x) for x in json.loads(raw)))
        if digest!=record['evidence'][sid]:return False
        normalized_expr=normalized(json.loads(expr),offset)
        if normalized_expr is None:return False
        entries[sid]=normalized_expr
    target=entries[record['target']]
    operator=record['operator'];src=record['sources']
    if operator=='shift_difference':
        expected=ep_add(shifted(entries[src[0]],record['parameters']['shift']),neg(entries[src[0]]))
    elif operator=='pointwise_product':
        expected=ep_mul(entries[src[0]],entries[src[1]])
    elif operator=='integer_linear_combination':
        p=record['parameters']
        expected=ep_add(scaled(entries[src[0]],p['left']),scaled(entries[src[1]],p['right']))
    else:return False
    return key(expected)==key(target)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--export',type=Path,required=True)
    p.add_argument('--basis-export',type=Path)
    p.add_argument('--max-coefficient',type=int,default=3)
    p.add_argument('--max-shift',type=int,default=3)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        r=discover(db,args.max_coefficient,args.max_shift)
    args.export.parent.mkdir(parents=True,exist_ok=True)
    args.export.write_text(''.join(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n' for x in r['links']),encoding='utf-8')
    if args.basis_export:
        args.basis_export.parent.mkdir(parents=True,exist_ok=True)
        args.basis_export.write_text(json.dumps(r['basis'],indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in r.items() if k not in ('links','basis')},indent=2))
    print(json.dumps({'basis_size':r['basis']['basis_size'],'basis':r['basis']['basis']},indent=2))


if __name__=='__main__':main()
