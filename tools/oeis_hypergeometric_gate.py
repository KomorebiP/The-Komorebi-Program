#!/usr/bin/env python3
"""Exact conditional first-order P-recursive and hypergeometric transfer certificates.

Author: Komorebi P.

No OEIS text is executed. Every all-index result is conditional on an explicitly
captured OEIS formula statement and an observed initial value (the latter must be
independently established to identify a named OEIS sequence). Certificates are
replayed from source byte hashes and rational-polynomial identities.

Scope is FIRST-ORDER recurrences Q(n)a(n+1)=P(n)a(n) only, with exact
rational-polynomial coefficients, proved nonvanishing Q on the indexed tail,
and a single anchored initial value. No general higher-order P-recursive claim.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import re

from oeis_gap_automation import Rational, parse_safe_rhs, divmod_poly, trim, write_json
from oeis_identification_proofs import OEISRecord, parse_record, poly_shift, ff, MAX_TERMS

MAX_DEGREE = 8
MAX_ROOT = 48
MAX_ROOT_DEN = 16
MAX_CHECK_TERMS = 40
MAX_GAUGE_DEGREE = 2
MAX_PAIRS = 5000
TERM = re.compile(r'\ba\(\s*n\s*(?P<shift>[+-]\s*\d+)?\s*\)',re.I)
LHS = re.compile(r'\ba\(\s*n\s*(?P<shift>[+-]\s*\d+)?\s*\)\s*=',re.I)


def evaluate(p: tuple[Q,...], n: int) -> Q:
    z = Q(0)
    for x in reversed(p):z=z*n+x
    return z


def ratio_evaluate(r: Rational, n: int) -> Q:
    denom=evaluate(r.den,n)
    if not denom:raise ZeroDivisionError('Rational expression undefined at indexed n')
    return evaluate(r.num,n)/denom


def shift(r: Rational, step:int) -> Rational:
    if abs(step)>1000:raise ValueError('Shift cap')
    return Rational(poly_shift(r.num,step),poly_shift(r.den,step)).reduce()


def sign_certificate(polynomial: tuple[Q,...], base: int) -> dict|None:
    """Q(n) is uniformly nonzero for all integer n>=base.

    Coefficients of Q(t+base) have a strict constant sign and non-strict
    identical higher signs. This is a sufficient, exact polynomial proof.
    """
    v=poly_shift(polynomial,base)
    if v[0]>0 and all(x>=0 for x in v):sgn='strict_positive'
    elif v[0]<0 and all(x<=0 for x in v):sgn='strict_negative'
    else:return None
    return {'method':'shifted_coefficient_sign', 'index_from':base,'sign':sgn,
            'shifted_coefficients':[ff(x) for x in v]}


def raw_denominator_signs(tree,term_names,base,shift_index=0):
    """Guard denominators in the written expression, before cancellations."""
    guards=[]
    for node in ast.walk(tree):
        if not isinstance(node,ast.BinOp) or not isinstance(node.op,ast.Div):continue
        if any(isinstance(v,ast.Name) and v.id in term_names for v in ast.walk(node.right)):
            return None
        try:r=parse_safe_rhs(ast.unparse(node.right))
        except (ValueError,ZeroDivisionError,SyntaxError,OverflowError):return None
        for p in (r.num,r.den):
            g=sign_certificate(poly_shift(p,shift_index),base)
            if g is None:return None
            guards.append(g)
    return guards


def _ratio_ast_safe(source:str) -> Rational|None:
    """Extract the coefficient of one first-order a(n+shift) by syntax.

    Never treats a product involving two copies of a(.) as linear, and never
    treats a sequence term in a denominator or nontrivial exponent as linear.
    """
    found=list(TERM.finditer(source))
    if len(found)!=1:return None
    source=TERM.sub('__seq_term',source)
    try:tree=ast.parse(source.replace('^','**'),mode='eval')
    except SyntaxError:return None
    count=0
    def validate(node:ast.AST,forbidden:bool=False)->None:
        nonlocal count
        if isinstance(node,ast.Name) and node.id=='__seq_term':
            count+=1
            if forbidden:raise ValueError('Nonlinear sequence operation')
        elif isinstance(node,ast.BinOp):
            validate(node.left,forbidden)
            validate(node.right,forbidden or isinstance(node.op,(ast.Pow,ast.Div)))
            # A divisor is permitted only when its denominator has no term.
            if isinstance(node.op,ast.Div):
                if any(isinstance(v,ast.Name) and v.id=='__seq_term' for v in ast.walk(node.right)):
                    raise ValueError('Sequence term in denominator')
            if isinstance(node.op,ast.Pow) and any(isinstance(v,ast.Name) and v.id=='__seq_term' for v in ast.walk(node)):
                raise ValueError('Sequence term in power')
        elif isinstance(node,ast.UnaryOp):validate(node.operand,forbidden)
        elif isinstance(node,ast.Call):
            if any(isinstance(v,ast.Name) and v.id=='__seq_term' for v in ast.walk(node)):
                raise ValueError('Sequence term in function')
        elif isinstance(node,(ast.Constant,ast.Name)):pass
        else:raise ValueError('Unsupported AST node')
    try:
        validate(tree.body)
        if count!=1:return None
        s=source.replace('__seq_term','1')
        zero=source.replace('__seq_term','0')
        r=parse_safe_rhs(s)
        if not parse_safe_rhs(zero).is_zero():return None
        return r
    except (ValueError,ZeroDivisionError,SyntaxError,OverflowError):return None


def parse_first_order(raw:str, *, offset:int) -> dict|None:
    """Recognize a conservatively delimited OEIS first-order recurrence.

    For a(n+1)=R(n)a(n), valid for n>=b. For a(n)=S(n)a(n-1),
    replace n by n+1. A lower bound on the originally written n is
    preserved; an absent bound gets the minimal possible OEIS tail guard.
    """
    if len(raw)>1200 or not -1000<=offset<=1000:return None
    text=raw.strip()
    # One source statement at a time. Attribution and unrelated subsequent
    # sentences may not supply terms of this recurrence.
    text=re.split(r'\.\s+(?=[A-Za-z_(])',text,maxsplit=1)[0]
    m=LHS.search(text)
    if not m:return None
    before=text[:m.start()].strip()
    if before and not re.fullmatch(r'(?:D-finite\s+with\s+)?[Rr]ecurrence\s*:',before):
        return None
    lhs=int(re.sub(r'\s+','',m.group('shift') or '0'))
    if lhs not in (0,1):return None
    tail=text[m.end():].strip().rstrip('.')
    if not tail:return None
    # Only the FIRST explicitly claimed equality is extracted, never infer
    # anything from unrelated later equations in the same OEIS entry.
    tail=re.split(r'\s+=\s+(?=Product|Sum|A\d{6}|[a-zA-Z_])',tail,maxsplit=1)[0]
    tail=re.split(r'\s+with\s+a\(\s*\d+\s*\)\s*=',tail,maxsplit=1)[0]
    bound=None
    condition=re.search(r',\s*(?:for\s+)?n\s*>=\s*(\d+)\s*$',tail)
    if condition:
        bound=int(condition.group(1));tail=tail[:condition.start()].strip()
    if ',' in tail or ';' in tail or '=' in tail or any(ch in tail for ch in '{}[]'):
        return None
    terms=list(TERM.finditer(tail))
    if len(terms)!=1:return None
    rhs_shift=int(re.sub(r'\s+','',terms[0].group('shift') or '0'))
    if rhs_shift!=lhs-1:return None
    r=_ratio_ast_safe(tail)
    if r is None or len(r.num)>MAX_DEGREE+1 or len(r.den)>MAX_DEGREE+1:return None
    # LHS=1 means variable n is the transition index; LHS=0 means it
    # describes a(n) from a(n-1), so transition index is n-1.
    base=max(offset,bound-(1-lhs) if bound is not None else offset)
    if base>1000 or base<offset:return None
    if lhs==0:r=shift(r,1)
    cert=sign_certificate(r.den,base)
    if not cert:return None
    tree=ast.parse(TERM.sub('__seq_term',tail).replace('^','**'),mode='eval')
    original=raw_denominator_signs(tree,{'__seq_term'},base,1-lhs)
    if original is None:return None
    return {'ratio':r,'base_index':base,'denominator_nonzero':cert,
            'source_statement':text[:260], 'source_bound':bound, 'raw_denominator_nonzero':original,
            'guard':'n >= '+str(base)}


def terms_from_ratio(r: Rational,base:int,initial:Q,length:int) -> list[Q]:
    if not 1<=length<=MAX_CHECK_TERMS:raise ValueError('Term budget')
    result=[Q(initial)]
    for n in range(base,base+length-1):
        result.append(result[-1]*ratio_evaluate(r,n))
    return result


def root_decomposition(poly: tuple[Q,...]) -> tuple[Q,list[Q]]|None:
    """Finite exact rational-linear factor decomposition, otherwise reject."""
    if poly==(Q(0),):return None
    f=trim(poly)
    leading=f[-1];roots=[]
    while len(f)>1:
        root=None
        for den in range(1,MAX_ROOT_DEN+1):
            for num in range(-MAX_ROOT*den,MAX_ROOT*den+1):
                if gcd(abs(num),den)>1:continue
                candidate=Q(num,den)
                if evaluate(f,candidate)==0:
                    root=candidate;break
            if root is not None:break
        if root is None:return None
        f,rem=divmod_poly(f,(-root,Q(1)))
        if rem!=(Q(0),):raise AssertionError('Rational root not a factor')
        roots.append(root)
    if f!=(leading,):raise AssertionError('Lost leading coefficient')
    return leading,sorted(roots)


def pochhammer_certificate(r: Rational,base:int) -> dict|None:
    """a(base+k)=a(base)*c^k * Prod (alpha)_k/Prod (beta)_k."""
    p=root_decomposition(r.num)
    q=root_decomposition(r.den)
    if p is None or q is None:return None
    cp,rp=p;cq,rq=q
    alpha=sorted((Q(base)-x for x in rp))
    beta=sorted((Q(base)-x for x in rq))
    out={'base_index':base,'geometric_factor':ff(cp/cq),
         'numerator_parameters':[ff(v) for v in alpha],
         'denominator_parameters':[ff(v) for v in beta],
         'statement':'a(base+k) = a(base)*c^k*product((alpha)_k)/product((beta)_k), k>=0',
         'proof':'Exactly factored rational consecutive-term ratio; termwise product identity by induction',
         'evidence':'conditional_on_pinned_first_order_recurrence_and_initial_value'}
    # Independent reconstruction in Q(n) rather than trusting factor list.
    numerator=Rational.constant(Q(cp/cq))
    for v in alpha:numerator=numerator.times(Rational((Q(v),Q(1)),(Q(1),)))
    for v in beta:numerator=numerator.over(Rational((Q(v),Q(1)),(Q(1),)))
    if not numerator.minus(shift(r,base)).is_zero():raise AssertionError('Pochhammer certificate algebra failed')
    return out


def profile(rec:OEISRecord) -> dict:
    out={'oeis_id':rec.oeis_id,'source_sha256':rec.source_sha256,
         'source_path':rec.source_path,'offset':rec.offset,
         'source_url':f'https://oeis.org/{rec.oeis_id}',
         'status':'no_supported_first_order_recurrence','quarantine':[],'definition':None}
    if rec.offset is None or not rec.terms or not -1000<=rec.offset<=1000:
        out['status']='unsupported_offset_or_missing_initial_terms'
        return out
    valid=[]
    for lineno,raw in rec.formulas:
        parsed=parse_first_order(raw,offset=rec.offset)
        if parsed is None:continue
        b=parsed['base_index']; pos=b-rec.offset
        if pos>=len(rec.terms):continue
        if len(rec.terms)-pos<2:continue
        ratio=parsed['ratio']
        try:calculated=terms_from_ratio(ratio,b,Q(rec.terms[pos]), min(len(rec.terms)-pos,MAX_CHECK_TERMS))
        except (ValueError,ZeroDivisionError):continue
        wrong=next((i for i,v in enumerate(calculated) if v!=rec.terms[pos+i]),None)
        if wrong is not None:
            out['quarantine'].append({'formula_line':lineno,'first_mismatch_index':b+wrong,
                                      'reason':'recurrence_disagrees_with_reported_terms'})
            continue
        valid.append({'method':'first_order_p_recursive','formula_line':lineno,
                      'ratio':{'num':[ff(x) for x in ratio.num],'den':[ff(x) for x in ratio.den]},
                      'initial':ff(Q(rec.terms[pos])),'base_index':b,
                      'matched_source_terms':len(calculated),
                      'denominator_nonzero':parsed['denominator_nonzero'],
                      'raw_denominator_nonzero':parsed['raw_denominator_nonzero'],
                      'source_statement':parsed['source_statement'],
                      'premise_status':'external_oeis_formula_and_source_initial_are_assumed',
                      'proof_status':'conditional_all_index_recurrence_uniqueness',
                      'pochhammer':pochhammer_certificate(ratio,b)})
    if out['quarantine']:
        out['status']='quarantined_inconsistent_source_recurrence'
        return out
    if not valid:return out
    unique={(v['base_index'],tuple(v['ratio']['num']),tuple(v['ratio']['den']),v['initial']) for v in valid}
    if len(unique)>1:
        out['status']='manual_equivalence_of_distinct_recurrences_required'
        out['candidate_count']=len(valid)
        return out
    out['definition']=valid[0]
    out['source_formula_lines']=[v['formula_line'] for v in valid]
    out['status']='conditional_first_order_definition'
    return out


def _rref_nullspace(rows:list[list[Q]], variables:int) -> list[Q]|None:
    if not rows or any(len(row)!=variables for row in rows):raise ValueError('Bad linear system')
    a=[[Q(v) for v in row] for row in rows]
    pivots=[];r=0
    for j in range(variables):
        at=next((i for i in range(r,len(a)) if a[i][j]!=0),None)
        if at is None:continue
        a[r],a[at]=a[at],a[r]
        k=a[r][j];a[r]=[x/k for x in a[r]]
        for i in range(len(a)):
            if i==r:continue
            k=a[i][j]
            if k:a[i]=[x-k*y for x,y in zip(a[i],a[r])]
        pivots.append(j);r+=1
        if r==variables:break
    free=[j for j in range(variables) if j not in pivots]
    if len(free)!=1:return None
    v=[Q(0)]*variables
    v[free[0]]=Q(1)
    for i,j in enumerate(pivots):v[j]=-a[i][free[0]]
    return v


def _profile_ratio(d:dict)->Rational:
    return Rational(tuple(Q(x) for x in d['ratio']['num']),tuple(Q(x) for x in d['ratio']['den'])).reduce()


def _at(d:dict,n:int)->Q:
    return terms_from_ratio(_profile_ratio(d),d['base_index'],Q(d['initial']),n-d['base_index']+1)[-1]


def discover_gauge(source:dict,target:dict)->dict|None:
    if any(p['status']!='conditional_first_order_definition' for p in (source,target)):return None
    a,b=source['definition'],target['definition']
    base=max(a['base_index'],b['base_index'])
    rA=_profile_ratio(a);rB=_profile_ratio(b)
    if base-max(a['base_index'],b['base_index'])>20:return None
    if base-a['base_index']>=MAX_CHECK_TERMS or base-b['base_index']>=MAX_CHECK_TERMS:return None
    # An exact finite probe generates candidates; the proof below is symbolic.
    try:
        aa=terms_from_ratio(rA,base,_at(a,base),MAX_CHECK_TERMS-1)
        bb=terms_from_ratio(rB,base,_at(b,base),MAX_CHECK_TERMS-1)
    except (ValueError,ZeroDivisionError):return None
    samples=[(base+i,v,w) for i,(v,w) in enumerate(zip(aa[:15],bb[:15])) if v!=0]
    if len(samples)<9:return None
    for complexity in range(0,2*MAX_GAUGE_DEGREE+1):
        for dp in range(MAX_GAUGE_DEGREE+1):
            dq=complexity-dp
            if not 0<=dq<=MAX_GAUGE_DEGREE:continue
            variables=dp+dq+2
            rows=[]
            for n,A,B in samples:
                z=B/A
                rows.append([Q(n)**j for j in range(dp+1)]+[-z*Q(n)**j for j in range(dq+1)])
            kernel=_rref_nullspace(rows,variables)
            if kernel is None:continue
            den=tuple(kernel[dp+1:]);num=tuple(kernel[:dp+1])
            if all(x==0 for x in den):continue
            try:g=Rational(trim(num),trim(den)).reduce()
            except (ValueError,ZeroDivisionError):continue
            sign=sign_certificate(g.den,base)
            if sign is None:continue
            if any(ratio_evaluate(g,n)*A!=B for n,A,B in samples):continue
            identity=shift(g,1).times(rA).minus(rB.times(g))
            if not identity.is_zero():continue
            if _at(b,base)!=ratio_evaluate(g,base)*_at(a,base):continue
            return {'source':source['oeis_id'],'target':target['oeis_id'],
                'source_sha256':source['source_sha256'],'target_sha256':target['source_sha256'],
                'source_formula_line':a['formula_line'],'target_formula_line':b['formula_line'],
                'base_index':base,'evidence':'conditional_exact_hypergeometric_gauge',
                'gauge':{'num':[ff(x) for x in g.num],'den':[ff(x) for x in g.den]},
                'gauge_denominator_nonzero':sign,
                'statement':'target(n)=g(n)*source(n), n>=base',
                'proof':'g(n+1)*R_source(n)=R_target(n)*g(n) exactly in Q(n), matching base seed, induction',
                'identification':'conditional_on_both_pinned_OEIS_first_order_recurrence_and_initial_premises',
                'admission':'conditional_overlay_only'}
    return None


def verify_gauge_cert(edge:dict,profiles:dict[str,dict])->bool:
    try:
        a=profiles[edge['source']];b=profiles[edge['target']]
        return discover_gauge(a,b)==edge
    except (KeyError,TypeError,ValueError,ZeroDivisionError,OverflowError):return False


def build_overlay(profiles:list[dict],max_pairs:int=MAX_PAIRS)->dict:
    valid=[x for x in profiles if x['status']=='conditional_first_order_definition']
    out=[];tried=0
    for a in valid:
        for b in valid:
            if a['oeis_id']==b['oeis_id']:continue
            tried+=1
            if tried>max_pairs:raise ValueError('Candidate budget exhausted; supply selected ID batches')
            e=discover_gauge(a,b)
            if e is not None:out.append(e)
    return {'schema':1,'conditional_edge_count':len(out),
            'candidate_pairs_examined':tried,'source_record_count':len(profiles),
            'conditional_first_order_records':len(valid),
            'not_unconditional_OEIS_identifications':True,
            'edges':sorted(out,key=lambda e:(e['source'],e['target']))}


def audit(root:Path,*,ids:set[str]|None=None,limit:int|None=None,max_pairs:int=MAX_PAIRS)->dict:
    paths=sorted(root.glob('seq/A[0-9][0-9][0-9]/A[0-9][0-9][0-9][0-9][0-9][0-9].seq'))
    if ids is not None:paths=[p for p in paths if p.stem in ids]
    if limit is not None:paths=paths[:limit]
    if not paths:raise ValueError('No matching OEIS data')
    profiles=[];failures=[]
    for p in paths:
        try:profiles.append(profile(parse_record(p,root)))
        except (ValueError,UnicodeDecodeError,OverflowError) as e:
            failures.append({'id':p.stem,'error':str(e)[:200]})
    ov=build_overlay(profiles,max_pairs=max_pairs)
    return {'summary':{'schema':1,'source':'local pinned oeisdata checkout',
        'author':'Komorebi P.','source_records_seen':len(paths),'parsed_records':len(profiles),
        'status_counts':dict(Counter(p['status'] for p in profiles)),
        'conditional_gauge_edges':ov['conditional_edge_count'],
        'Pochhammer_normal_forms':sum(p['definition'] is not None and p['definition']['pochhammer'] is not None for p in profiles),
        'independently_established_OEIS_identifications':0},
        'profiles':profiles,'overlay':ov,'quarantine':failures}


def report_files(data:dict)->dict[str,dict]:
    return {'hypergeom_summary.json':data['summary'],'hypergeom_profiles.json':data['profiles'],
            'conditional_hypergeom_gauges.json':data['overlay'],'hypergeom_quarantine.json':data['quarantine']}


def verify_report(root:Path,directory:Path, *, ids:set[str]|None=None)->dict:
    names=['hypergeom_summary.json','hypergeom_profiles.json','conditional_hypergeom_gauges.json','hypergeom_quarantine.json']
    stored={k:json.loads((directory/k).read_text('utf-8')) for k in names}
    # Externally pin the selection: never derive completeness from a possibly
    # truncated or forged report. No --ids means ALL source files.
    expected=report_files(audit(root,ids=ids))
    if stored!=expected:raise ValueError('Exact source-bound hypergeometric proof replay failed')
    return {'status':'passed','records_rechecked':len(expected['hypergeom_profiles.json']),
            'conditional_gauges_reproved':expected['conditional_hypergeom_gauges.json']['conditional_edge_count'],
            'independent_OEIS_identifications':0}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--oeis-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--ids',default='')
    p.add_argument('--limit',type=int)
    p.add_argument('--max-pairs',type=int,default=MAX_PAIRS)
    p.add_argument('--verify-report',action='store_true')
    v=p.parse_args()
    ids={s.strip() for s in v.ids.split(',') if s.strip()} or None
    if ids is not None and any(not re.fullmatch(r'A\d{6}',i) for i in ids):p.error('Invalid OEIS ID')
    if v.verify_report:print(json.dumps(verify_report(v.oeis_root,v.output,ids=ids),indent=2));return
    data=audit(v.oeis_root,ids=ids,limit=v.limit,max_pairs=v.max_pairs)
    for name,obj in report_files(data).items():write_json(v.output/name,obj)
    print(json.dumps(data['summary'],indent=2))

if __name__=='__main__':main()
