"""Proof-carrying composition of exact OEIS formula gauge transfers.

Author: Komorebi P.

Compose two exact hypergeometric gauge certificates through a shared
formula-defined sequence. Prove the composite by Q(t) rational identities
and one initial value, NOT by finite-prefix interpolation.

This proves relations among admitted evaluator expressions, not the global
identification of their OEIS IDs. Arbitrary imported formula text is not run.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
import sqlite3
from pathlib import Path
from sequence_hypergeometric_gauges import (
    difference_ratio, gauge_value, load_models, certify_pair,
)
from sequence_holonomic_compiler import Rat, fraction_eval
from sequence_ratio_certificates import ratio_polynomials


def oriented_edge(edge, reverse=False):
    x = dict(edge)
    if reverse:
        x['source'], x['target'] = x['target'], x['source']
        x['source_formula'], x['target_formula'] = x['target_formula'], x['source_formula']
        x['source_sha256'], x['target_sha256'] = x['target_sha256'], x['source_sha256']
        x['source_evaluator_sha256'], x['target_evaluator_sha256'] = x['target_evaluator_sha256'], x['source_evaluator_sha256']
        x['source_offset'], x['target_offset'] = x['target_offset'], x['source_offset']
        x['exponential_factor'] = str(1/F(x['exponential_factor']))
        x['base_ratio'] = str(1/F(x['base_ratio']))
        x['gauge_linear_factors'] = [dict(f, power=-f['power']) for f in x['gauge_linear_factors']]
    return x


def composite_factors(edges):
    acc=Counter()
    for edge in edges:
        for f in edge['gauge_linear_factors']:
            acc[f['a'],f['b']]+=f['power']
    return [dict(a=a,b=b,power=p) for (a,b),p in sorted(acc.items()) if p]


def gauge_rat(factors):
    L=Rat()
    for f in factors:
        z=Rat((f['b'], f['a']))
        for _ in range(abs(f['power'])):
            L=L*z if f['power']>0 else L/z
    return L


def compose(models, first, second, independent_checks=True):
    """Return an all-index exact composite only if every symbolic gate passes."""
    if first['target']!=second['source'] or first['source']==second['target']:
        raise ValueError('edges do not form a two-hop noncyclic path')
    nodes=[first['source'],first['target'],second['target']]
    a,m,b=(models.get(n) for n in nodes)
    if None in (a,m,b):raise ValueError('missing current formula models')
    for e,src,dst in ((first,a,m),(second,m,b)):
        for field,expected in (
            ('source_formula',src['formula_id']),('target_formula',dst['formula_id']),
            ('source_sha256',src['source_sha256']),('target_sha256',dst['source_sha256']),
            ('source_evaluator_sha256',src['evaluator_sha256']),
            ('target_evaluator_sha256',dst['evaluator_sha256']),
            ('source_offset',src['offset']),('target_offset',dst['offset'])):
            if e[field]!=expected:raise ValueError('stale certificate or differing intermediary formula '+field)
    # Reprove *each* incoming edge, including its normalization constant.
    # A fabricated or edited input certificate must never be used as a lemma.
    for e,src,dst in ((first,a,m),(second,m,b)):
        fresh=certify_pair(src,dst,max_support=max(4,e['support']))
        if fresh is None:
            raise ValueError('intermediary formula transfer no longer certifies')
        for field in ('tail_start_local','base_ratio','exponential_factor','gauge_linear_factors'):
            if e[field]!=fresh[field]:
                raise ValueError('tampered or stale intermediary transfer '+field)
    T=max(first['tail_start_local'],second['tail_start_local'])
    original=first['gauge_linear_factors']+second['gauge_linear_factors']
    if any(f['a']<=0 or f['a']*T+f['b']<=0 for f in original):
        raise ValueError('singular/negative affine factor at tail boundary')
    factors=composite_factors((first,second))
    L=gauge_rat(factors)
    c=F(first['exponential_factor'])*F(second['exponential_factor'])
    r=difference_ratio(a,b)
    exact=Rat(*ratio_polynomials(r))
    if exact!=Rat((c,))*L.shift(1)/L:
        raise AssertionError('composite ratio is not an identity in Q(t)')
    aval=fraction_eval(a['ast'],a['offset']+T)
    bval=fraction_eval(b['ast'],b['offset']+T)
    if not aval or not bval:raise ValueError('nonzero base evaluation required')
    K=bval/aval
    if not L.at(T):raise ValueError('gauge normalization zero')
    if independent_checks:
        for t in (T,T+1,T+3,T+9):
            actual=fraction_eval(b['ast'],b['offset']+t)
            predicted=fraction_eval(a['ast'],a['offset']+t)*K*c**(t-T)*L.at(t)/L.at(T)
            if actual!=predicted:raise AssertionError('composite formula check fails at '+str(t))
    route=[dict(source=e['source'],target=e['target'],source_formula=e['source_formula'],
                target_formula=e['target_formula'],source_sha256=e['source_sha256'],
                target_sha256=e['target_sha256'],tail_start_local=e['tail_start_local'])
           for e in (first,second)]
    receipt=dict(source=a['oeis_id'],via=m['oeis_id'],target=b['oeis_id'],
        source_formula=a['formula_id'],via_formula=m['formula_id'],target_formula=b['formula_id'],
        source_sha256=a['source_sha256'],via_sha256=m['source_sha256'],target_sha256=b['source_sha256'],
        source_evaluator_sha256=a['evaluator_sha256'],via_evaluator_sha256=m['evaluator_sha256'],
        target_evaluator_sha256=b['evaluator_sha256'],
        source_offset=a['offset'],via_offset=m['offset'],target_offset=b['offset'],
        tail_start_local=T,base_ratio=str(K),exponential_factor=str(c),
        gauge_linear_factors=factors,support=sum(abs(f['power']) for f in factors),
        path=route,
        proof_method='Two current independently certified rational-gauge identities; exact Q(t) shift ratio of composite and one nonzero base value',
        scope='All-index identity of admitted formula expressions for t>=tail_start_local, not global OEIS sequence identification')
    receipt['certificate_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return receipt


def all_oriented(ledger):
    for l in Path(ledger).open(encoding='utf8'):
        if not l.strip():continue
        e=json.loads(l)
        yield oriented_edge(e)
        yield oriented_edge(e,True)


def generate(db,ledger,extra,output,summary=None,limit=500,cap=5):
    models,_=load_models(db,extra)
    adjacency=defaultdict(list);direct=set()
    for e in all_oriented(ledger):
        adjacency[e['source']].append(e)
        direct.add((e['source'],e['target']))
    # Stable enumeration, prioritize simpler symbolic formulas, then node IDs.
    proposals=[];seen=set()
    for src in sorted(adjacency):
        for first in adjacency[src]:
            for second in adjacency[first['target']]:
                target=second['target']
                if target==src or (src,target) in direct or (src,target) in seen:continue
                fs=composite_factors((first,second))
                support=sum(abs(f['power']) for f in fs)
                if support==0 or support>cap:continue
                seen.add((src,target))
                proposals.append((support,src,target,first,second))
    proposals.sort(key=lambda e:(e[0],e[1],e[2]))
    counts=Counter();certificates=[]
    for _,src,dst,first,second in proposals:
        counts['proposed']+=1
        try:
            cert=compose(models,first,second)
        except (ArithmeticError,ValueError,OverflowError,AssertionError,KeyError) as exc:
            counts['rejected']+=1
            if counts['rejected']<=5:counts['rejected_sample_'+str(counts['rejected'])]=str(exc)
            continue
        certificates.append(cert)
        counts['certified']+=1
        if len(certificates)>=limit:break
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with Path(output).open('w',encoding='utf8') as f:
        for c in certificates:f.write(json.dumps(c,sort_keys=True,separators=(',',':'))+'\n')
    receipt=dict(status='all_index_formula_gauge_composition',input_models=len(models),
        original_edges=len(direct)//2,candidates_enumerated=len(proposals),
        **counts, max_support=cap,source=Path(ledger).name,
        scope='Exact formula-defined identities; global OEIS identification not proved')
    if summary:Path(summary).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    return receipt


def replay(db,ledger,extra,source):
    models,_=load_models(db,extra)
    originals={}
    for e in all_oriented(source):originals[e['source'],e['target']]=e
    checked=0;errors=[]
    for line in Path(ledger).open(encoding='utf8'):
        if not line.strip():continue
        c=json.loads(line);checked+=1
        try:
            route=c['path']
            first=originals[route[0]['source'],route[0]['target']]
            second=originals[route[1]['source'],route[1]['target']]
            rebuilt=compose(models,first,second)
            if rebuilt!=c:raise ValueError('composite receipt changed')
        except (KeyError,ValueError,ArithmeticError,AssertionError,OverflowError) as exc:
            if len(errors)<12:errors.append(dict(source=c.get('source'),target=c.get('target'),error=str(exc)))
    return dict(status='passed' if not errors else 'failed',checked=checked,errors=errors)


def main():
    p=argparse.ArgumentParser();p.add_argument('--db',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--extra',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path)
    p.add_argument('--limit',type=int,default=500);p.add_argument('--replay',action='store_true')
    args=p.parse_args()
    with sqlite3.connect(args.db) as db:
        result=replay(db,args.output,args.extra,args.source) if args.replay else generate(db,args.source,args.extra,args.output,args.summary,args.limit)
    print(json.dumps(result,indent=2))
    if result['status']=='failed':raise SystemExit(1)
if __name__=='__main__':main()
