"""Exact symbolic transfer discovery across OEIS's finite-checked formula DSL.

Author: Komorebi P.

Every admitted expression is a finite exponential polynomial
    sum_{rate != 0} P_rate(n) rate**n, P_rate in Q[n].
Candidate links are found by hashing *the entire symbolic normal form*, not
by matching OEIS prefixes. Thus the identities hold for every local n>=0,
conditional on the source/target extracted formula expressions being correct.

OEIS source formulas are only finitely cross-checked. This tool NEVER claims
that two official OEIS entries have thereby been globally identified.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import sqlite3

from sequence_linear_identity_compiler import normalized, key, shifted, scaled, p_shift
from sequence_exponential_polynomial import p_add, p_scale, p_mul, ep_add


def peval(poly,n):return sum(Q(a)*n**j for j,a in enumerate(poly))


def paffine(poly,m,r):
    if type(m) is not int or m<1 or type(r) is not int or r<0:
        raise ValueError('invalid affine phase')
    out=[Q(0)]*len(poly)
    for degree,coef in enumerate(poly):
        for j in range(degree+1):out[j]+=Q(coef)*comb(degree,j)*m**j*r**(degree-j)
    while len(out)>1 and out[-1]==0:out.pop()
    return out


def phase(expr,m,r):
    result={}
    for rate,poly in expr.items():
        new_rate=rate**m
        new_poly=p_scale(paffine(poly,m,r),Q(rate)**r)
        result=ep_add(result,{new_rate:new_poly})
    return result


def adjacent(expr):return ep_add(shifted(expr,1),scaled(expr,-1))


def falling_poly(j,offset=0):
    out=[Q(1)]
    for k in range(j):
        new=[Q(0)]*(len(out)+1)
        for i,v in enumerate(out):
            new[i]+=v*Q(offset-k)
            new[i+1]+=v
        out=new
    return out


def _newton_coefficients(poly):
    """P(n)=sum_j Delta^j(P(0))/j! * n^underline(j)."""
    d=len(poly)-1
    return [sum((-1)**(j-i)*comb(j,i)*peval(poly,i)
                for i in range(j+1))/factorial(j) for j in range(d+1)]


def binomial(expr,inverse=False):
    """Exact binomial transform in the exponential-polynomial ring.

    Singular rates produce finitely-supported sequences, not represented in
    this ring. Return None and leave these cases to the C-finite verifier.
    """
    out={}
    for rate,poly in expr.items():
        new_rate=rate-1 if inverse else rate+1
        if not new_rate:return None
        coeff=[Q(0)]
        for j,alpha in enumerate(_newton_coefficients(poly)):
            if alpha:
                coeff=p_add(coeff,p_scale(falling_poly(j),alpha*(Q(rate,new_rate)**j)))
        out=ep_add(out,{new_rate:coeff})
    return out


def prefix_sum(expr):
    """Exact partial sums for all integer-rate exponential-polynomial terms.

    Each nonunit rate is antidifferenced by triangular polynomial division;
    rate 1 uses the Newton binomial basis summation identity.
    """
    out={}
    for rate,poly in expr.items():
        if rate==1:
            total=[Q(0)]
            for j,alpha in enumerate(_newton_coefficients(poly)):
                if alpha:total=p_add(total,p_scale(falling_poly(j+1,1),alpha/Q(j+1)))
            out=ep_add(out,{1:total})
        else:
            d=len(poly)-1;q=[Q(0)]*(d+1)
            for j in range(d,-1,-1):
                correction=sum(q[k]*comb(k,j)*(-1)**(k-j) for k in range(j+1,d+1))
                q[j]=(Q(rate)*poly[j]+correction)/Q(rate-1)
            # Verify the antidifference polynomial coefficient by coefficient.
            for j in range(d+1):
                lhs=Q(rate)*q[j]-sum(q[k]*comb(k,j)*(-1)**(k-j) for k in range(j,d+1))
                if lhs!=Q(rate)*poly[j]:raise ArithmeticError('antidifference polynomial mismatch')
            out=ep_add(out,{rate:q})
            constant=peval(poly,0)-peval(q,0)
            if constant:out=ep_add(out,{1:[constant]})
    return out


def formal_eval(expr,n):
    return sum(peval(p,n)*Q(rate)**n for rate,p in expr.items())


def transform(expr,op,params):
    if op=='shift':return shifted(expr,params['shift'])
    if op=='polyphase':return phase(expr,params['modulus'],params['residue'])
    if op=='add_constant':return ep_add(expr,{1:[Q(params['constant'])]})
    if op=='multiply_constant':return scaled(expr,params['constant'])
    if op=='adjacent_difference':return adjacent(expr)
    if op=='prefix_sum':return prefix_sum(expr)
    if op=='binomial_transform':return binomial(expr)
    if op=='inverse_binomial_transform':return binomial(expr,inverse=True)
    if op=='identity':return expr
    raise ValueError('unsupported symbolic transfer')


def load_formulas(db):
    records=defaultdict(list)
    for sid,fid,raw,off,source_sha,checked in db.execute('''
       SELECT f.oeis_id,f.formula_id,f.evaluator_json,s.offset,s.source_sha256,f.checked_terms
       FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
       WHERE f.origin='oeis_normalized' AND f.verification='finite_checked'
       ORDER BY f.oeis_id,f.formula_id'''):
        try:
            expr=normalized(json.loads(raw),off)
            if expr is None:continue
            records[sid].append({'oeis_id':sid,'formula_id':fid,
                 'record_sha256':source_sha,'offset':off,'checked_terms':checked,
                 'expression':expr,'key':key(expr)})
        except (ValueError,TypeError,ArithmeticError,OverflowError):continue
    valid={};conflicts=[]
    for sid,entries in records.items():
        if any(e['key']!=entries[0]['key'] for e in entries[1:]):
            conflicts.append(sid)
        else:
            valid[sid]=min(entries,key=lambda e:(len(e['key']),e['formula_id']))
    return valid,conflicts


def candidates(expr,*,max_shift=6,max_modulus=10,max_constant=8,max_multiplier=6):
    for s in range(1,max_shift+1):yield 'shift',{'shift':s},shifted(expr,s)
    for m in range(2,max_modulus+1):
        for r in range(m):yield 'polyphase',{'modulus':m,'residue':r},phase(expr,m,r)
    for k in range(-max_constant,max_constant+1):
        if k:yield 'add_constant',{'constant':k},ep_add(expr,{1:[Q(k)]})
    for k in range(-max_multiplier,max_multiplier+1):
        if k not in (0,1,-1):yield 'multiply_constant',{'constant':k},scaled(expr,k)
    yield 'adjacent_difference',{},adjacent(expr)
    yield 'prefix_sum',{},prefix_sum(expr)
    for inv,op in ((False,'binomial_transform'),(True,'inverse_binomial_transform')):
        value=binomial(expr,inverse=inv)
        if value is not None:yield op,{},value


def discover(db,*,max_shift=6,max_modulus=10,max_constant=8,max_multiplier=6,
             export=None,exclude_existing_candidates=False):
    records,conflicts=load_formulas(db)
    lookup=defaultdict(list)
    for sid,record in records.items():lookup[record['key']].append(sid)
    existing=set()
    for out,raw_inputs,op,params in db.execute('SELECT output_id,inputs_json,operator,parameters_json FROM transfer_candidates'):
        ids=json.loads(raw_inputs)
        if len(ids)==1:existing.add((ids[0],out,op,params))
    counts=Counter();edges=[];seen=set()
    for source_id,record in sorted(records.items()):
        counts['sources_scanned']+=1
        for op,params,calculated in candidates(record['expression'],max_shift=max_shift,
                                                max_modulus=max_modulus,max_constant=max_constant,
                                                max_multiplier=max_multiplier):
            if calculated is None:continue
            matches=lookup.get(key(calculated),())
            for target_id in matches:
                if source_id==target_id:continue
                signature=(source_id,target_id,op,json.dumps(params,sort_keys=True))
                if signature in seen:continue
                seen.add(signature)
                if key(records[target_id]['expression'])!=key(calculated):
                    raise AssertionError('symbolic matching index mismatch')
                was_mined=(source_id,target_id,op,json.dumps(params,sort_keys=True)) in existing
                if exclude_existing_candidates and was_mined:continue
                target=records[target_id]
                edges.append({'source':source_id,'target':target_id,'operator':op,
                     'parameters':params,'status':'all_index_formula_identity',
                     'was_finite_mined':was_mined,
                     'source_formula_id':record['formula_id'],
                     'target_formula_id':target['formula_id'],
                     'source_sha256':record['record_sha256'],
                     'target_sha256':target['record_sha256'],
                     'source_offset':record['offset'],'target_offset':target['offset'],
                     'proof_method':'exact equality of canonical exponential-polynomial coefficients over Q',
                     'scope':'supplied formula identities for all local indices; OEIS global identification unassessed'})
                counts['symbolic_edges']+=1
                counts['by_'+op]+=1
                counts['previously_finite_mined' if was_mined else 'new_beyond_prefix_miner']+=1
        if counts['sources_scanned']%250==0:pass
    if export:
        export=Path(export);export.parent.mkdir(parents=True,exist_ok=True)
        with export.open('w',encoding='utf-8') as stream:
            for edge in edges:stream.write(json.dumps(edge,ensure_ascii=False,separators=(',',':'))+'\n')
    return {'formula_sequence_nodes':len(records),'formula_source_conflicts':conflicts,
            'sources_examined':counts['sources_scanned'],
            'exact_formal_edges':counts['symbolic_edges'],
            'previously_finite_mined':counts['previously_finite_mined'],
            'new_beyond_prefix_miner':counts['new_beyond_prefix_miner'],
            'by_operator':{k[3:]:v for k,v in counts.items() if k.startswith('by_')},
            'domain':'all n>=0 of supplied source and target formulas; OEIS infinite identification remains finite-checked'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--export',type=Path,required=True)
    p.add_argument('--summary',type=Path)
    p.add_argument('--max-modulus',type=int,default=10)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        stats=discover(db,export=args.export,max_modulus=args.max_modulus)
    if args.summary:
        args.summary.parent.mkdir(parents=True,exist_ok=True)
        args.summary.write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n')
    print(json.dumps(stats,indent=2,sort_keys=True))

if __name__=='__main__':main()
