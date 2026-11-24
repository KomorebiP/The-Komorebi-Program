#!/usr/bin/env python3
"""Exact higher-order P-recursive gauge certificates with singularity guards.

Author: Komorebi P.

For d<=4, verify conditional relations T(n)=g(n) S(n) from two pinned
P-recursive source statements. A finite candidate is *never* a proof: require
an exact polynomial/rational identity for every recurrence coefficient and
all d initial values. No general D-finite or OEIS identification is claimed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction as Q
import json
from pathlib import Path
import re

from oeis_gap_automation import Rational, parse_safe_rhs, trim, write_json
from oeis_identification_proofs import OEISRecord, parse_record, ff, poly_shift
from oeis_hypergeometric_gate import evaluate, sign_certificate, shift, ratio_evaluate, _rref_nullspace, raw_denominator_signs

TERM=re.compile(r'\ba\(\s*n\s*(?P<delta>[+-]\s*\d+)?\s*\)', re.I)
LHS=re.compile(r'\ba\(\s*n\s*\+\s*(?P<order>\d+)\s*\)\s*=',re.I)
MAX_ORDER=4
MAX_CHECK=35
MAX_EXP_LENGTH=320


def _is_zero(r:Rational)->bool:return r.is_zero()


def _linear_ast(node:ast.AST,terms:dict[str,int],depth:int=0)->tuple[dict[int,Rational],Rational]:
    if depth>32:raise ValueError('AST recursion exceeded')
    if isinstance(node,ast.Name) and node.id in terms:
        return {terms[node.id]:Rational.constant(Q(1))},Rational.constant(Q(0))
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
        c,z=_linear_ast(node.operand,terms,depth+1)
        if isinstance(node.op,ast.USub):
            minus=Rational.constant(Q(-1))
            return {k:minus.times(v) for k,v in c.items()},minus.times(z)
        return c,z
    if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
        a,u=_linear_ast(node.left,terms,depth+1)
        b,v=_linear_ast(node.right,terms,depth+1)
        if isinstance(node.op,(ast.Add,ast.Sub)):
            mul=Rational.constant(Q(-1) if isinstance(node.op,ast.Sub) else Q(1))
            out=a.copy()
            for k,w in b.items():out[k]=out.get(k,Rational.constant(Q(0))).plus(mul.times(w))
            return out,u.plus(mul.times(v))
        if isinstance(node.op,ast.Mult):
            if a and b:raise ValueError('Nonlinear recurrence')
            out={k:w.times(v) for k,w in a.items()}
            for k,w in b.items():out[k]=out.get(k,Rational.constant(Q(0))).plus(w.times(u))
            return out,u.times(v)
        if b or v.is_zero():raise ValueError('Sequence term in denominator')
        return {k:w.over(v) for k,w in a.items()},u.over(v)
    # Only a term-free exact rational expression is acceptable here, including
    # powers and binomial(n,k) with bounded, fixed k.
    if any(isinstance(x,ast.Name) and x.id in terms for x in ast.walk(node)):
        raise ValueError('Unsupported sequence occurrence')
    return {},parse_safe_rhs(ast.unparse(node))


def parse_operator(text:str,*,offset:int)->dict|None:
    """Parse a(n+d)=sum_{j<d} R_j(n)*a(n+j) over Q(n)."""
    if len(text)>1400 or not -1000<=offset<=1000:return None
    s=text.strip()
    s=re.split(r'\.\s+(?=[A-Za-z_(])',s,maxsplit=1)[0]
    m=LHS.search(s)
    if not m:return None
    pre=s[:m.start()].strip()
    if pre and not re.fullmatch(r'(?:D-finite\s+with\s+)?[Rr]ecurrence\s*:',pre):return None
    d=int(m.group('order'))
    if d not in (2,3,4):return None
    tail=s[m.end():].strip().rstrip('.')
    if not tail or len(tail)>MAX_EXP_LENGTH:return None
    condition=re.search(r',\s*(?:for\s+)?n\s*>=\s*(\d+)\s*$',tail)
    bound=None
    if condition:
        bound=int(condition.group(1));tail=tail[:condition.start()].strip()
    if any(z in tail for z in (';', '[',']','{','}')):return None
    vars={};seen=[]
    def replace(mt:re.Match)->str:
        sh=int(re.sub(r'\s+','',mt.group('delta') or '0'))
        if sh<0 or sh>=d:raise ValueError('Outside forward recurrence window')
        symbol='__s'+str(sh)
        vars[symbol]=sh;seen.append(sh)
        return symbol
    try:
        expr=TERM.sub(replace,tail)
        if not seen:return None
        parsed=ast.parse(expr.replace('^','**'),mode='eval')
        coeff,const=_linear_ast(parsed.body,vars)
        if not const.is_zero():return None
        base=max(offset,bound if bound is not None else offset)
        if base>1000:return None
        coeff=[coeff.get(j,Rational.constant(Q(0))).reduce() for j in range(d)]
        if all(_is_zero(c) for c in coeff):return None
        guards=[sign_certificate(c.den,base) for c in coeff]
        if any(g is None for g in guards):return None
        original=raw_denominator_signs(parsed,vars,base)
        if original is None:return None
        return {'order':d,'base_index':base,'coefficients':coeff,
            'denominator_nonzero':guards,'raw_denominator_nonzero':original,'source_statement':s[:260]}
    except (SyntaxError,ValueError,OverflowError,ZeroDivisionError):return None


def term_values(operator:dict,initial:list[Q], count:int)->list[Q]:
    d=operator['order'];base=operator['base_index']
    if not 2<=d<=MAX_ORDER or len(initial)!=d or count<d or count>MAX_CHECK:
        raise ValueError('P-recurrence order or term cap')
    terms=list(initial)
    while len(terms)<count:
        n=base+len(terms)-d
        c=operator['coefficients']
        terms.append(sum((ratio_evaluate(c[j],n)*terms[-d+j] for j in range(d)),Q(0)))
    return terms


def encode_rat(r:Rational)->dict:return {'num':[ff(x) for x in r.num],'den':[ff(x) for x in r.den]}


def decode_rat(v:dict)->Rational:
    return Rational(tuple(Q(x) for x in v['num']),tuple(Q(x) for x in v['den'])).reduce()


def profile(rec:OEISRecord)->dict:
    out={'oeis_id':rec.oeis_id,'source_sha256':rec.source_sha256,
         'source_path':rec.source_path,'offset':rec.offset,'source_url':f'https://oeis.org/{rec.oeis_id}',
         'status':'no_supported_P_recurrence','definition':None,'quarantine':[]}
    if rec.offset is None or not rec.terms or not -1000<=rec.offset<=1000:
        out['status']='unsupported_offset_or_missing_terms';return out
    admissible=[]
    for line,formula in rec.formulas:
        op=parse_operator(formula,offset=rec.offset)
        if op is None:continue
        base=op['base_index'];d=op['order'];pos=base-rec.offset
        if pos<0 or len(rec.terms)-pos<d+1:continue
        sample=rec.terms[pos:pos+MAX_CHECK]
        init=[Q(x) for x in sample[:d]]
        try:calculated=term_values(op,init,len(sample))
        except (ValueError,ZeroDivisionError):continue
        failed=next((k for k,v in enumerate(calculated) if v!=sample[k]),None)
        if failed is not None:
            out['quarantine'].append({'formula_line':line,'first_disagreement_index':base+failed,
                                      'reason':'source_recurrence_disagrees_with_reported_terms'})
            continue
        admissible.append({'method':'order_d_P_recursive','formula_line':line,
             'order':d,'base_index':base,'initial':[ff(x) for x in init],
             'coefficients':[encode_rat(c) for c in op['coefficients']],
             'denominator_nonzero':op['denominator_nonzero'],
             'raw_denominator_nonzero':op['raw_denominator_nonzero'],
             'matched_source_terms':len(calculated),'source_statement':op['source_statement'],
             'premise_status':'OEIS_formula_and_initial_terms_not_independently_proved'})
    if out['quarantine']:
        out['status']='quarantined_inconsistent_source_operator';return out
    if not admissible:return out
    signatures={(v['order'],v['base_index'],tuple(v['initial']),
                 tuple((tuple(c['num']),tuple(c['den'])) for c in v['coefficients'])) for v in admissible}
    if len(signatures)!=1:
        out['status']='manual_operator_equivalence_required';return out
    out['status']='conditional_higher_order_definition';out['definition']=admissible[0]
    out['source_formula_lines']=[x['formula_line'] for x in admissible]
    return out


def _defs_operator(p:dict)->dict:
    d=p['definition']
    return {'order':d['order'],'base_index':d['base_index'],
            'coefficients':[decode_rat(c) for c in d['coefficients']]}


def _at(d:dict,n:int)->Q:
    if not 0<=n-d['base_index']<MAX_CHECK:raise ValueError('Outside certificate term bound')
    op={'order':d['order'],'base_index':d['base_index'],
        'coefficients':[decode_rat(c) for c in d['coefficients']]}
    return term_values(op,[Q(x) for x in d['initial']], max(d['order'], n-d['base_index']+1))[n-d['base_index']]


def candidate_ratios(source:dict,target:dict,base:int):
    """Small rational candidate search by exact interpolation; no proof by fit."""
    a,b=source['definition'],target['definition']
    try:
        aa=[_at(a,base+k) for k in range(12)]
        bb=[_at(b,base+k) for k in range(12)]
    except (ValueError,ZeroDivisionError):return
    samples=[(base+i,A,B) for i,(A,B) in enumerate(zip(aa,bb)) if A!=0]
    if len(samples)<9:return
    for total in range(5):
        for p in range(3):
            q=total-p
            if not 0<=q<=2:continue
            if len(samples)<p+q+3:continue
            rows=[]
            for n,A,B in samples:
                z=B/A
                rows.append([Q(n)**j for j in range(p+1)]+[-z*Q(n)**j for j in range(q+1)])
            v=_rref_nullspace(rows,p+q+2)
            if v is None:continue
            num=trim(v[:p+1]);den=trim(v[p+1:])
            if den==(Q(0),):continue
            try:g=Rational(num,den).reduce()
            except (ValueError,ZeroDivisionError):continue
            if sign_certificate(g.den,base) is None:continue
            if all(ratio_evaluate(g,n)*A==B for n,A,B in samples):yield g


def prove_gauge(source:dict,target:dict)->dict|None:
    if source['status']!='conditional_higher_order_definition' or target['status']!='conditional_higher_order_definition':return None
    a,b=source['definition'],target['definition']
    d=a['order']
    if d!=b['order']:return None
    base=max(a['base_index'],b['base_index'])
    if base-a['base_index']+d+13>MAX_CHECK or base-b['base_index']+d+13>MAX_CHECK:return None
    S=_defs_operator(source);T=_defs_operator(target)
    for g in candidate_ratios(source,target,base):
        # Identity: T(n+d) = g(n+d) S(n+d) and recurrence coefficients
        # d_j(n) g(n+j) = g(n+d) c_j(n), for every j and n>=base.
        if any(not T['coefficients'][j].times(shift(g,j)).minus(
            shift(g,d).times(S['coefficients'][j])).is_zero() for j in range(d)):
            continue
        if any(_at(b,base+k)!=ratio_evaluate(g,base+k)*_at(a,base+k) for k in range(d)):
            continue
        return {'source':source['oeis_id'],'target':target['oeis_id'],
            'source_sha256':source['source_sha256'],'target_sha256':target['source_sha256'],
            'source_formula_line':a['formula_line'],'target_formula_line':b['formula_line'],
            'base_index':base,'order':d,'gauge':encode_rat(g),
            'gauge_denominator_nonzero':sign_certificate(g.den,base),
            'evidence':'conditional_exact_higher_order_P_recurrence_gauge',
            'proof':'exact rational Ore-gauge coefficient conjugacy for all shifts and d initial seeds; induction',
            'identification':'conditional_on_both_pinned_source_operator_and_initial_premises',
            'admission':'conditional_overlay_only'}
    return None


def verify_edge(edge:dict,by_id:dict[str,dict])->bool:
    try:return prove_gauge(by_id[edge['source']],by_id[edge['target']])==edge
    except (ValueError,KeyError,TypeError,ZeroDivisionError):return False


def audit(root:Path,*,ids:set[str]|None=None,limit:int|None=None,max_pairs:int=3000)->dict:
    paths=sorted(root.glob('seq/A[0-9][0-9][0-9]/A[0-9][0-9][0-9][0-9][0-9][0-9].seq'))
    if ids:paths=[p for p in paths if p.stem in ids]
    if limit is not None:paths=paths[:limit]
    if not paths:raise ValueError('No OEIS source records')
    profiles=[];fail=[]
    for p in paths:
        try:profiles.append(profile(parse_record(p,root)))
        except (ValueError,UnicodeDecodeError,OverflowError) as ex:
            fail.append({'id':p.stem,'error':str(ex)[:200]})
    valid=[x for x in profiles if x['status']=='conditional_higher_order_definition']
    edges=[];tried=0
    for s in valid:
        for t in valid:
            if s['oeis_id']==t['oeis_id']:continue
            tried+=1
            if tried>max_pairs:raise ValueError('P-recursive candidate budget exhausted')
            e=prove_gauge(s,t)
            if e is not None:edges.append(e)
    ov={'schema':1,'source_record_count':len(profiles),'candidate_pairs':tried,
        'conditional_edge_count':len(edges),'not_unconditional_OEIS_proofs':True,
        'edges':sorted(edges,key=lambda e:(e['source'],e['target']))}
    summary={'schema':1,'author':'Komorebi P.','source':'local OEIS source excerpts or pinned full checkout',
        'record_count':len(paths),'status_counts':dict(Counter(x['status'] for x in profiles)),
        'conditional_higher_order_gauges':len(edges),'unconditional_OEIS_identifications':0}
    return {'summary':summary,'profiles':profiles,'overlay':ov,'quarantine':fail}


def report_files(d:dict)->dict:
    return {'precursive_summary.json':d['summary'],'precursive_profiles.json':d['profiles'],
            'conditional_P_recursive_gauges.json':d['overlay'],'precursive_quarantine.json':d['quarantine']}


def verify_report(root:Path,directory:Path, *, ids:set[str]|None=None)->dict:
    saved={n:json.loads((directory/n).read_text()) for n in report_files({'summary':None,'profiles':None,'overlay':None,'quarantine':None})}
    # Caller pins explicit subset; absent --ids, require a complete root scan.
    actual=report_files(audit(root,ids=ids))
    if saved!=actual:raise ValueError('P-recursive source-bound proof replay failed')
    return {'status':'passed','record_count':len(actual['precursive_profiles.json']),'gauges_reproved':actual['conditional_P_recursive_gauges.json']['conditional_edge_count']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--oeis-root',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--ids',default='')
    p.add_argument('--limit',type=int)
    p.add_argument('--max-pairs',type=int,default=3000)
    p.add_argument('--verify-report',action='store_true')
    args=p.parse_args()
    ids={x.strip() for x in args.ids.split(',') if x.strip()} or None
    if ids and any(not re.fullmatch(r'A\d{6}',i) for i in ids):p.error('Invalid OEIS ID')
    if args.verify_report:print(json.dumps(verify_report(args.oeis_root,args.output,ids=ids),indent=2));return
    d=audit(args.oeis_root,ids=ids,limit=args.limit,max_pairs=args.max_pairs)
    for name,v in report_files(d).items():write_json(args.output/name,v)
    print(json.dumps(d['summary'],indent=2))

if __name__=='__main__':main()
