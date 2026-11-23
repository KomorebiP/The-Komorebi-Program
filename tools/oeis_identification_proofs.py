#!/usr/bin/env python3
"""Conservative OEIS identification and exact transfer proof gate.

Author: Komorebi P.

Rules:
  * OEIS text is data and never executed.
  * Polynomial and ordinary generating-function identities are proved as
    implications of pinned source statements, not as independent OEIS facts.
  * Reported initial terms only detect contradictions. They cannot prove an
    infinite identification.
  * Certified conditional edges live in an ADDITIVE overlay, separate from the
    curated source transfer graph and its all-index OEIS proof assertions.

Nonzero-offset polynomial definitions are normalized to their stated indices.
Generating functions with unspecified offset conventions remain unsupported.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import re

from oeis_gap_automation import Rational, parse_safe_rhs, parse_term_formula, add, mul, neg
from oeis_cfinite_bridge import exact_linear_solve

OEIS_ID = re.compile(r"A\d{6}\Z")
FIELD = re.compile(r"^%([A-Z])\s+(A\d{6})\s*(.*)$")
GF_START = re.compile(r"^\s*G\.f\.\s*:\s*(.+)$",re.I)
TERM_START = re.compile(r"^\s*a\s*\(\s*n\s*\)\s*=",re.I)
REC_START = re.compile(r"^\s*a\s*\(\s*n\s*(?P<shift>[+-]\s*\d+)?\s*\)\s*=\s*(?P<rhs>.+)$",re.I)
A_TERM = re.compile(r"\ba\s*\(\s*n\s*(?P<shift>[+-]\s*\d+)?\s*\)",re.I)
N_BOUND = re.compile(r"(?:^|[,;]\s*)(?:for\s+)?n\s*>=\s*(\d+)\b",re.I)
MAX_RECORD_BYTES=900_000
MAX_TERMS=512
MAX_FORMULAS=1500
MAX_ORDER=8


def ff(x: Q|int|str) -> str:
    return str(Q(x))


def polys(p: tuple[Q,...]) -> list[str]:
    return [ff(v) for v in p]


def poly_shift(p: tuple[Q,...], shift: int) -> tuple[Q,...]:
    """Exact polynomial p(n+shift), using the binomial theorem."""
    out = [Q(0)]*len(p)
    for k,v in enumerate(p):
        for j in range(k+1):
            out[j]+=v*comb(k,j)*Q(shift)**(k-j)
    while len(out)>1 and out[-1]==0:out.pop()
    return tuple(out)


def series(num: tuple[Q,...],den: tuple[Q,...], n: int) -> list[Q]:
    if not 1<=n<=2000 or den[0]==0:
        raise ValueError('Non-power-series OGF or unsupported length')
    a=[]
    for k in range(n):
        r=(num[k] if k<len(num) else Q(0))
        for j in range(1,min(k,len(den)-1)+1):
            r-=den[j]*a[k-j]
        a.append(r/den[0])
    return a


def recurrence_terms(c: list[Q],initial: list[Q], n: int) -> list[Q]:
    if not 1<=len(c)<=MAX_ORDER or len(initial)!=len(c):
        raise ValueError('Invalid recurrence seed')
    a=list(initial)
    while len(a)<n:
        a.append(sum((c[j-1]*a[-j] for j in range(1,len(c)+1)), Q(0)))
    return a[:n]


def strip_end_annotation(raw: str) -> str:
    # OEIS often adds an attribution at the end of the same %F line.
    return re.split(r"\.\s+-\s+(?=[A-Z_])",raw,maxsplit=1)[0].strip().rstrip('.').strip()


def gf_parse(formula: str) -> Rational|None:
    m=GF_START.match(strip_end_annotation(formula))
    if not m:return None
    s=m.group(1).strip()
    if ';' in s or ',' in s or '=' in s or '[' in s or ']' in s:
        return None
    # The earlier exact arithmetic kernel is intentionally one-symbol-only.
    s=re.sub(r'\bx\b','n',s)
    try:
        rf=parse_safe_rhs(s)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        return None
    if rf.den[0]==0:
        return None
    return rf


def _lin_ast(node:ast.AST,var_offsets: dict[str,int],depth:int=0) -> tuple[dict[int,Q],Q]:
    if depth>25:raise ValueError('AST too deep')
    if isinstance(node,ast.Constant) and type(node.value) is int and abs(node.value)<10**15:
        return {},Q(node.value)
    if isinstance(node,ast.Name) and node.id in var_offsets:
        return {var_offsets[node.id]:Q(1)},Q(0)
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
        a,b=_lin_ast(node.operand,var_offsets,depth+1)
        if isinstance(node.op,ast.USub):return {k:-v for k,v in a.items()},-b
        return a,b
    if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
        a,c=_lin_ast(node.left,var_offsets,depth+1)
        b,d=_lin_ast(node.right,var_offsets,depth+1)
        if isinstance(node.op,(ast.Add,ast.Sub)):
            z=1 if isinstance(node.op,ast.Add) else -1
            out=a.copy()
            for k,v in b.items():out[k]=out.get(k,Q(0))+z*v
            return out,c+z*d
        if isinstance(node.op,ast.Mult):
            if a and b:raise ValueError('Nonlinear recurrence')
            if a:return {k:v*d for k,v in a.items()},c*d
            if b:return {k:v*c for k,v in b.items()},c*d
            return {},c*d
        if b or d==0:raise ValueError('Nonconstant/zero denominator')
        return {k:v/d for k,v in a.items()},c/d
    raise ValueError('Unsupported expression node')


def recurrence_parse(text: str) -> tuple[list[Q],int]|None:
    m=REC_START.match(strip_end_annotation(text))
    if not m:return None
    lhs=int(re.sub(r'\s+','',m.group('shift') or '0'))
    if lhs<0 or lhs>MAX_ORDER:return None
    rhs=m.group('rhs')
    # Commas may introduce annotations, but only a recognized lower bound is
    # accepted. Other conditions would silently change the theorem domain.
    tail=''
    for sep in (',',';'):
        if sep in rhs:
            rhs,tail=rhs.split(sep,1)
            break
    tail=tail.strip()
    if tail and not N_BOUND.search(','+tail):
        return None
    if len(rhs)>240 or not A_TERM.search(rhs):return None
    var_offsets={}
    def replace(mt:re.Match) -> str:
        sh=int(re.sub(r'\s+','',mt.group('shift') or '0'))
        name='__term_'+('m'+str(-sh) if sh<0 else 'p'+str(sh))
        var_offsets[name]=sh
        return name
    expr=A_TERM.sub(replace,rhs)
    try:
        tree=ast.parse(expr,mode='eval')
        a,constant=_lin_ast(tree.body,var_offsets)
    except (SyntaxError,ValueError,OverflowError,ZeroDivisionError):
        return None
    if constant!=0 or not a:return None
    offsets={lhs - sh:v for sh,v in a.items() if v}
    if not offsets or min(offsets)<1 or max(offsets)>MAX_ORDER:
        return None
    d=max(offsets)
    c=[offsets.get(j,Q(0)) for j in range(1,d+1)]
    explicit=[int(x) for x in N_BOUND.findall(','+tail)]
    threshold=max(d,lhs,max(explicit,default=0)+lhs)
    return c,threshold


@dataclass(frozen=True)
class OEISRecord:
    oeis_id: str
    source_sha256: str
    name: str
    offset: int|None
    terms: tuple[int,...]
    formulas: tuple[tuple[int,str],...]
    source_path: str


def parse_record(path: Path, root: Path|None=None) -> OEISRecord:
    raw=path.read_bytes()
    if len(raw)>MAX_RECORD_BYTES:raise ValueError('Record exceeds parser limit')
    key=path.stem
    if not OEIS_ID.fullmatch(key):raise ValueError('Invalid source file name')
    fields=[]
    for lineno,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        m=FIELD.match(line)
        if not m:continue
        if m.group(2)!=key:raise ValueError('Mixed OEIS IDs')
        fields.append((lineno,m.group(1),m.group(3)))
    if not fields:raise ValueError('Missing OEIS fields')
    by=defaultdict(list)
    for ln,k,v in fields:by[k].append((ln,v))
    offset=None
    if by['O']:
        try:offset=int(by['O'][0][1].split(',')[0].strip())
        except ValueError:offset=None
    seq=[]
    for tag in 'STU':
        for _,value in by[tag]:
            value=value.strip().strip(',')
            if not re.fullmatch(r'[\d,\-+\s]*',value):
                raise ValueError('Unsupported term list syntax')
            for token in value.split(','):
                token=token.strip()
                if not token:continue
                if len(token)>250 or len(seq)>=MAX_TERMS:raise ValueError('Term parser limit')
                seq.append(int(token))
    name=by['N'][0][1] if by['N'] else ''
    fs=tuple(by['F'][:MAX_FORMULAS])
    if root:
        try:rel=path.relative_to(root).as_posix()
        except ValueError:rel=path.name
    else:rel=path.name
    return OEISRecord(key,sha256(raw).hexdigest(),name,offset,tuple(seq),fs,rel)


def _verified_profile_for_gf(rec:OEISRecord,line:int,gf:Rational) -> dict|None:
    d=len(gf.den)-1
    if not 1<=d<=MAX_ORDER:return None
    if gf.den[0]==0:return None
    c=[-gf.den[j]/gf.den[0] for j in range(1,d+1)]
    start=max(d,len(gf.num))  # Degree numerator + 1
    base=start-d
    if len(rec.terms)<base+d:return None
    calc=series(gf.num,gf.den,max(len(rec.terms),base+d))
    checked=min(len(rec.terms),len(calc))
    if any(calc[i]!=rec.terms[i] for i in range(checked)):
        return {'quarantine':'gf_disagrees_with_reported_terms','formula_line':line,'checked_terms':checked}
    return {'method':'rational_ogf', 'formula_line':line,
            'rational_ogf':{'numerator':polys(gf.num),'denominator':polys(gf.den)},
            'coefficients':[ff(v) for v in c],
            'base_index':base, 'initial':[ff(v) for v in calc[base:base+d]],
            'recurrence_valid_from':start,
            'matched_source_terms':checked,
            'proof':'Q(x)A(x)=P(x) implies the coefficient recurrence for all n>deg(P).',
            'premise_status':'oeis_source_formula_is_assumed_not_independently_proved',
            'verification_status':'exact_formal_power_series_implication'}


def _polynomial_profile(rec:OEISRecord,line:int,text:str) -> dict|None:
    try:
        p,_=parse_term_formula(strip_end_annotation(text))
    except (ValueError,SyntaxError,ZeroDivisionError,OverflowError):
        return None
    if p.den!=(Q(1),):return None
    if rec.offset is None:return None
    deg=len(p.num)-1;d=deg+1
    if not 1<=d<=MAX_ORDER or len(rec.terms)<d:return None
    if any(sum((p.num[j]*(rec.offset+i)**j for j in range(len(p.num))),Q(0))!=v for i,v in enumerate(rec.terms)):
        return {'quarantine':'polynomial_disagrees_with_reported_terms','formula_line':line}
    c=[Q((-1)**(j+1)*comb(d,j)) for j in range(1,d+1)]
    # Difference operator (E-1)^d annihilates Q[n] of degree < d.
    identity=p.num
    for j,v in enumerate(c,1):
        identity=add(identity,neg(mul((v,),poly_shift(p.num,-j))))
    if any(identity):raise AssertionError('Exact polynomial recurrence derivation failed')
    return {'method':'polynomial_formula','formula_line':line,'polynomial':polys(p.num),
            'coefficients':[ff(v) for v in c], 'base_index':rec.offset,
            'initial':[ff(v) for v in rec.terms[:d]],
            'recurrence_valid_from':rec.offset+d,'matched_source_terms':len(rec.terms),
            'proof':f'Exact polynomial identity (1-E^-1)^{d} p(n)=0 for n>={d}.',
            'premise_status':'oeis_source_formula_is_assumed_not_independently_proved',
            'verification_status':'exact_polynomial_identity'}


def _polynomial_ogf(p: tuple[Q,...]) -> Rational:
    """Derive Sum_{n>=0} p(n)x^n exactly using finite differences."""
    d=len(p)
    if not 1<=d<=MAX_ORDER:raise ValueError('Polynomial degree cap')
    den=tuple(Q((-1)**k*comb(d,k)) for k in range(d+1))
    values=[sum((v*Q(n)**j for j,v in enumerate(p)), Q(0)) for n in range(d)]
    num=tuple(sum((den[j]*values[k-j] for j in range(k+1)), Q(0)) for k in range(d))
    return Rational(num,den).reduce()


def _name_recurrence_ogf(coeff:list[Q], initials:list[Q]) -> Rational:
    """OGF uniquely determined by a complete constant-recurrence seed."""
    d=len(coeff)
    if len(initials)!=d or not 1<=d<=MAX_ORDER:raise ValueError('Incomplete recurrence seeds')
    den=tuple([Q(1)]+[-v for v in coeff])
    num=tuple(initials[n]-sum((coeff[j-1]*initials[n-j] for j in range(1,n+1)),Q(0))
              for n in range(d))
    return Rational(num,den).reduce()


def _check_name_definition(rec:OEISRecord, definition:dict) -> dict|None:
    """Restricted %N-to-%F exact formal-series equivalence with contradiction quarantine.

    Parsing a complete named definition proves a conditional mathematical
    equivalence of source premises, not independently established OEIS facts.
    """
    text=rec.name
    namepoly=re.search(r'\ba\(\s*n\s*\)\s*=\s*([^=;.]+)',text)
    if namepoly:
        source=namepoly.group(1).strip()
        try:
            p=parse_safe_rhs(source)
            if p.den==(Q(1),):
                if definition['method']=='polynomial_formula':
                    matched=p.num==tuple(Q(v) for v in definition['polynomial'])
                elif definition['method']=='rational_ogf' and rec.offset==0:
                    gf=definition['rational_ogf']
                    reported=Rational(tuple(Q(v) for v in gf['numerator']),tuple(Q(v) for v in gf['denominator']))
                    matched=_polynomial_ogf(p.num).minus(reported).is_zero()
                else:return None
                if matched:
                    return {'type':'name_polynomial','name_expression':source,
                            'proof':'Exact rational-OGF or polynomial equality; the named expression is a source premise.'}
                return {'type':'name_definition_conflict',
                        'reason':'explicit_name_polynomial_does_not_equal_source_formula'}
        except (SyntaxError,ValueError,ZeroDivisionError,OverflowError):pass

    m=re.search(r'\b([A-Za-z])\(n\)\s*=\s*(.*?)(?:\s+with\s+|,\s*(?=[A-Za-z]\(\d+\)\s*=))',text)
    if not m:return None
    variable=m.group(1)
    if variable=='a':return None
    rhs=m.group(2).strip()
    if not re.fullmatch(r'[A-Za-z0-9+*() /\-]+',rhs):return None
    changed=re.sub(r'\b'+re.escape(variable)+r'\s*\(', 'a(',rhs)
    parsed=recurrence_parse('a(n)='+changed)
    if parsed is None:return None
    coeff,threshold=parsed
    d=len(coeff)
    if rec.offset!=0 or definition['base_index']!=0 or threshold>d:return None
    seeds={}
    for idx,v in re.findall(r'\b'+re.escape(variable)+r'\((\d+)\)\s*=\s*([+-]?\d+)\b',text):
        if int(idx) in seeds and seeds[int(idx)]!=Q(int(v)):
            return {'type':'name_definition_conflict','reason':'contradictory_named_seeds'}
        seeds[int(idx)]=Q(int(v))
    if any(j not in seeds for j in range(d)):return None
    if definition['method']=='rational_ogf':
        gf=definition['rational_ogf']
        reported=Rational(tuple(Q(v) for v in gf['numerator']),tuple(Q(v) for v in gf['denominator']))
        matched=_name_recurrence_ogf(coeff,[seeds[j] for j in range(d)]).minus(reported).is_zero()
    elif definition['method']=='polynomial_formula':
        matched=_name_recurrence_ogf(coeff,[seeds[j] for j in range(d)]).minus(
            _polynomial_ogf(tuple(Q(v) for v in definition['polynomial']))).is_zero()
    else:return None
    if not matched:
        return {'type':'name_definition_conflict','reason':'named_recurrence_OGF_differs_from_source_formula'}
    return {'type':'name_recurrence','name_symbol':variable,
            'name_seeds':{str(x):ff(v) for x,v in sorted(seeds.items())},
            'proof':'Exact formal generating-function equality and complete recurrence seeds; uniqueness by induction.'}


def profile_record(rec:OEISRecord) -> dict:
    base={'oeis_id':rec.oeis_id,'source_sha256':rec.source_sha256,
          'source_path':rec.source_path,'oeis_source_url':f'https://oeis.org/{rec.oeis_id}',
          'offset':rec.offset,'reported_term_count':len(rec.terms),
          'status':'unresolved','definitions':[],'quarantined':[]}
    if rec.offset is None:
        base['status']='unsupported_nonzero_or_missing_offset'
        return base
    if not rec.terms:
        base['status']='no_reported_initial_terms'
        return base
    gfdefs=[];polydefs=[];recurrences=[]
    for ln,raw in rec.formulas:
        # Without an explicit OGF shift convention, exponent 0 is not
        # automatically OEIS index 0 when the record starts at another index.
        gf=gf_parse(raw) if rec.offset==0 else None
        if gf is not None:
            proof=_verified_profile_for_gf(rec,ln,gf)
            if proof:
                if 'quarantine' in proof:base['quarantined'].append(proof)
                else:gfdefs.append(proof)
        if TERM_START.match(raw):
            pf=_polynomial_profile(rec,ln,raw)
            if pf:
                if 'quarantine' in pf:base['quarantined'].append(pf)
                else:polydefs.append(pf)
        rp=recurrence_parse(raw)
        if rp:
            c,start=rp;d=len(c)
            if len(rec.terms)+rec.offset>=start:
                # Terms can be checked for the stated range. Never infer the
                # recurrence merely because the sampled terms fit it.
                mismatch=next((n for n in range(max(start,rec.offset+d),rec.offset+len(rec.terms))
                               if Q(rec.terms[n-rec.offset])!=sum((c[j-1]*rec.terms[n-j-rec.offset] for j in range(1,d+1)),Q(0))),None)
                if mismatch is not None:
                    base['quarantined'].append({'quarantine':'recurrence_disagrees_with_reported_terms',
                        'formula_line':ln,'first_disagreement_n':mismatch})
                    continue
            if rec.offset+len(rec.terms)>=start:
                recurrences.append({'coefficients':[ff(v) for v in c],
                                    'recurrence_valid_from':start,'formula_line':ln,
                                    'matched_source_terms':max(0,rec.offset+len(rec.terms)-max(start,rec.offset+d))})
    # Fail closed when a source's unqualified OGF or recurrence claim
    # contradicts its reported prefix. No conditional edge is admitted.
    if any(q['quarantine'] in ('gf_disagrees_with_reported_terms',
                              'polynomial_disagrees_with_reported_terms',
                              'recurrence_disagrees_with_reported_terms')
           for q in base['quarantined']):
        base['status']='quarantined_inconsistent_source_premises'
        return base
    all_defs=gfdefs+polydefs
    # GF and polynomial source premises may provide multiple incompatible
    # definitions. Reject conflicts rather than picking the first formula.
    selected=[]
    for d in all_defs:
        sign=(tuple(d['coefficients']),d['base_index'],tuple(d['initial']))
        if sign not in {(tuple(v['coefficients']),v['base_index'],tuple(v['initial'])) for v in selected}:
            selected.append(d)
    if len(selected)>1:
        # Different valid higher-order recurrences can represent the same
        # series. Compare exact generating functions whenever available; if
        # formal equivalence is unavailable, quarantine the ambiguity.
        for a,b in combinations(selected,2):
            if a['method']==b['method']=='rational_ogf':
                ra,rb=a['rational_ogf'],b['rational_ogf']
                A=Rational(tuple(Q(v) for v in ra['numerator']),tuple(Q(v) for v in ra['denominator']))
                B=Rational(tuple(Q(v) for v in rb['numerator']),tuple(Q(v) for v in rb['denominator']))
                if not A.minus(B).is_zero():
                    base['status']='quarantined_conflicting_source_formulas';base['quarantined'].append({'quarantine':'different_rational_ogfs'});return base
            else:
                base['status']='manual_cross_formula_equivalence_required'
                base['quarantined'].append({'quarantine':'multiple_unproven_equivalent_presentations'})
                return base
    # Prefer the verified generating function over redundant polynomial form.
    if selected:
        best=next((x for x in selected if x['method']=='rational_ogf'),selected[0])
        # GF-to-recurrence exact check: (1 - sum c_j x^j) A(x) is a
        # polynomial of degree less than recurrence_valid_from.
        agreeing=[]
        for rs in recurrences:
            c=[Q(v) for v in rs['coefficients']]
            gf=best.get('rational_ogf')
            if not gf:continue
            A=Rational(tuple(Q(v) for v in gf['numerator']),tuple(Q(v) for v in gf['denominator']))
            D=Rational(tuple([Q(1)]+[-v for v in c]),(Q(1),))
            R=A.times(D).reduce()
            if R.den==(Q(1),) and len(R.num)<=rs['recurrence_valid_from']:
                agreeing.append(rs['formula_line'])
            else:
                base['quarantined'].append({'quarantine':'stated_recurrence_not_implied_by_GF',
                                            'formula_line':rs['formula_line']})
        best['consistent_recurrence_lines']=agreeing
        name_check=_check_name_definition(rec,best)
        if name_check is not None and name_check['type']=='name_definition_conflict':
            base['quarantined'].append({'quarantine':'explicit_name_definition_disagrees_with_formula',**name_check})
            base['status']='quarantined_name_definition_conflict'
            return base
        if name_check is not None:
            best['name_definition_checked']=name_check
            base['status']='oeis_name_definition_equivalence_proved'
        else:
            base['status']='source_premise_exactly_rederived'
        base['definitions']=[best]
    elif recurrences:
        base['status']='finite_consistency_only'
        base['recurrence_claims']=recurrences
    if rec.offset!=0 and base['status']=='unresolved':
        base['status']='unsupported_nonzero_or_missing_offset'
        base['quarantined'].append({'quarantine':'ambiguous_generating_function_offset_convention'})
    return base


def _seed_terms(d:dict,n:int) -> list[Q]:
    return recurrence_terms([Q(v) for v in d['coefficients']],
                            [Q(v) for v in d['initial']],n)


def transfer(source:dict,target:dict)->dict|None:
    """All-index shifted transfer from proved recurrences with SAME tail base."""
    a,b=source['definitions'][0],target['definitions'][0]
    if a['coefficients']!=b['coefficients'] or a['base_index']!=b['base_index']:
        return None
    d=len(a['coefficients'])
    if not 1<=d<=MAX_ORDER:return None
    v=_seed_terms(a,2*d)
    M=[[v[i+j] for j in range(d)] for i in range(d)]
    out=exact_linear_solve(M,[Q(x) for x in b['initial']])
    if out is None:return None
    sol,rank=out
    # Recheck both initial and the recurrence interface, not only the solver.
    if any(sum((M[i][j]*sol[j] for j in range(d)),Q(0))!=Q(b['initial'][i]) for i in range(d)):
        raise AssertionError('Inconsistent linear system')
    return {'source':source['oeis_id'],'target':target['oeis_id'],
            'source_sha256':source['source_sha256'],'target_sha256':target['source_sha256'],
            'evidence':'conditional_exact_recurrence_transfer',
            'domain':f"n >= {a['base_index']}",
            'formula':'target(n) = sum_{j=0}^{d-1} c[j]*source(n+j)',
            'shift_coefficients':[ff(v) for v in sol],
            'basis_matrix':[[ff(v) for v in row] for row in M],
            'target_initial':b['initial'],
            'characteristic_recurrence':a['coefficients'],
            'recurrence_order':d,'source_shift_rank':rank,
            'proof':'exact rational shift-orbit solve plus recurrence induction',
            'identification':'conditional_on_both_pinned_oeis_source_formula_premises',
            'admission':'conditional_overlay_only'}


def verify_transfer_cert(edge:dict,profiles_by_id:dict[str,dict])->bool:
    try:
        s=profiles_by_id[edge['source']];t=profiles_by_id[edge['target']]
        if any(e['status'] not in ('source_premise_exactly_rederived','oeis_name_definition_equivalence_proved') for e in (s,t)):return False
        if edge['source_sha256']!=s['source_sha256'] or edge['target_sha256']!=t['source_sha256']:return False
        ref=transfer(s,t)
        return ref==edge
    except (KeyError,ValueError,AssertionError,TypeError,IndexError,ZeroDivisionError):
        return False


def build_overlay(profiles:list[dict], *, max_pairs:int=20000)->dict:
    verified=[p for p in profiles if p['status'] in ('source_premise_exactly_rederived','oeis_name_definition_equivalence_proved')]
    groups=defaultdict(list)
    for p in verified:
        d=p['definitions'][0]
        groups[(tuple(d['coefficients']),d['base_index'])].append(p)
    edges=[];candidate_pairs=0
    for group in groups.values():
        for s in group:
            for t in group:
                if s['oeis_id']==t['oeis_id']:continue
                candidate_pairs+=1
                if candidate_pairs>max_pairs:raise ValueError('Candidate pair budget exceeded')
                e=transfer(s,t)
                if e is not None and verify_transfer_cert(e,{s['oeis_id']:s,t['oeis_id']:t}):
                    edges.append(e)
    return {'schema':1,'author':'Komorebi P.','scope':'conditional proof overlay, not OEIS identifications',
            'source_record_count':len(profiles),'exact_source_premise_count':len(verified),
            'conditional_edge_count':len(edges),'not_unconditional_oeis_identifications':True,
            'edges':sorted(edges,key=lambda v:(v['source'],v['target']))}


def audit(root:Path, *, ids:set[str]|None=None,limit:int|None=None,max_pairs:int=20000)->dict:
    paths=sorted(root.glob('seq/A[0-9][0-9][0-9]/A[0-9][0-9][0-9][0-9][0-9][0-9].seq'))
    if ids is not None:paths=[p for p in paths if p.stem in ids]
    if limit is not None:paths=paths[:limit]
    if not paths:raise ValueError('No OEIS .seq records found')
    profiles=[];parse_failures=[]
    for p in paths:
        try:profiles.append(profile_record(parse_record(p,root)))
        except (UnicodeDecodeError,ValueError,OverflowError) as ex:
            parse_failures.append({'id':p.stem,'error':str(ex)[:200]})
    overlay=build_overlay(profiles,max_pairs=max_pairs)
    summary={'schema':1,'author':'Komorebi P.','source':'local oeis/oeisdata checkout',
        'source_records_seen':len(paths),'records_parsed':len(profiles),'parse_failures':len(parse_failures),
        'status_counts':dict(Counter(p['status'] for p in profiles)),
        'proof_gated_conditional_edges':overlay['conditional_edge_count'],
        'unconditional_oeis_identifications':0,
        'limitation':'OEIS source statements are external premises. Finite matches are not infinite identification proofs.'}
    return {'summary':summary,'profiles':profiles,'quarantine':parse_failures,'overlay':overlay}


def verify_report(root:Path, report_dir:Path, *, ids:set[str]|None=None)->dict:
    """Recompute whole report from pinned OEIS sources and reject all tampering.

    Fail closed if any source record was modified since receipt generation.
    No external code, formulas, or JSON expressions are executed.
    """
    files=['identification_report.json','sequence_profiles.json',
           'conditional_transfer_overlay.json','quarantine.json']
    stored=[]
    for f in files:
        stored.append(json.loads((report_dir/f).read_text(encoding='utf-8')))
    # External caller pins the selection, never a possibly truncated report.
    computed=audit(root,ids=ids)
    for actual,expect,name in zip(
       [computed['summary'],computed['profiles'],computed['overlay'],computed['quarantine']],
       stored,files):
        if actual!=expect:
            raise ValueError(f'Failed exact source-bound proof replay: {name}')
    return {'status':'passed','pinned_source_records_rechecked':len(computed['profiles']),
            'conditional_edges_reproved':len(computed['overlay']['edges']),
            'unconditional_oeis_identifications':0}


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--oeis-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--ids',default='',help='Optional comma-separated pinned IDs')
    parser.add_argument('--limit',type=int)
    parser.add_argument('--max-pairs',type=int,default=20000)
    parser.add_argument('--verify-report',action='store_true',help='Replay pinned source and every certificate')
    args=parser.parse_args()
    ids=set(x.strip() for x in args.ids.split(',') if x.strip()) or None
    if ids and any(not OEIS_ID.fullmatch(x) for x in ids):parser.error('Invalid OEIS ID')
    if args.verify_report:
        print(json.dumps(verify_report(args.oeis_root,args.output,ids=ids),indent=2))
        return
    report=audit(args.oeis_root,ids=ids,limit=args.limit,max_pairs=args.max_pairs)
    for name,body in [('identification_report.json',report['summary']),
                      ('sequence_profiles.json',report['profiles']),
                      ('conditional_transfer_overlay.json',report['overlay']),
                      ('quarantine.json',report['quarantine'])]:
        (args.output/name).parent.mkdir(parents=True,exist_ok=True)
        (args.output/name).write_text(json.dumps(body,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report['summary'],indent=2))

if __name__=='__main__':main()
