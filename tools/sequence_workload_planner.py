"""Proof-gated, shared-workload optimizer for exact OEIS formula gauges.

Author: Komorebi P.

Finite matches are *never* accepted as transfer edges. Every edge is
re-derived from the current evaluator formulas using a rational-function
certificate and a base-value check. Invertible, nonsingular all-index gauges
are modeled as undirected edges. A virtual root represents direct evaluation;
Dreyfus-Wagner subset DP returns a minimum-weight shared computation tree for
up to six requested output prefixes, under the *declared* additive work model.

This is not a globally fastest algorithm or a proof of OEIS identities. The
certificates are identities between the admitted formula expressions.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from fractions import Fraction
import heapq
import hashlib
import math
import json
import sqlite3
import statistics
import time
from pathlib import Path
from typing import Any

from sequence_hypergeometric_gauges import load_models, certify_pair
from sequence_v10_path_compiler import oriented_edge, gauge_value
from sequence_holonomic_compiler import fraction_eval

ROOT = '__DIRECT_EVALUATION_ROOT__'


def safe_formula_fingerprint(model: dict) -> str:
    return hashlib.sha256(json.dumps(model['ast'],sort_keys=True,separators=(',',':')).encode()).hexdigest()


def verified_gauges(models: dict, ledger: Path, *, strict=True):
    """Return current source-bound, re-proved, nonsingular gauge edges.

    The original ledger is never a sufficient proof by itself. We recompute
    the certificate from the admitted source and target exact formulas.
    """
    counts=Counter();out=[]
    with Path(ledger).open(encoding='utf-8') as stream:
      for raw in stream:
          if not raw.strip():continue
          row=json.loads(raw);counts['read']+=1
          u,v=row['source'],row['target']
          if u not in models or v not in models:
              counts['missing_formula']+=1
              if strict:raise ValueError('ledger source or target model missing: '+u+' -> '+v)
              continue
          src,dst=models[u],models[v]
          for name,expect in (('source_formula',src['formula_id']),('target_formula',dst['formula_id']),
                              ('source_sha256',src['source_sha256']),('target_sha256',dst['source_sha256']),
                              ('source_evaluator_sha256',safe_formula_fingerprint(src)),
                              ('target_evaluator_sha256',safe_formula_fingerprint(dst)),
                              ('source_offset',src['offset']),('target_offset',dst['offset'])):
              if row.get(name)!=expect:
                  counts['stale']+=1
                  if strict:raise ValueError(f'stale or forged certificate {u}->{v}: {name}')
                  break
          else:
              if row['tail_start_local']!=0 or src['tail']!=0 or dst['tail']!=0:
                  counts['nonzero_tail']+=1
                  continue
              # Re-derive the rational factor shift-coboundary, and re-check
              # the normalization. All factors must stay nonzero on n>=0.
              fresh=certify_pair(src,dst,max_support=max(4,row['support']))
              if fresh is None:
                  counts['uncertified']+=1
                  if strict:raise ValueError(f'certification failed for {u}->{v}')
                  continue
              for field in ('tail_start_local','base_ratio','exponential_factor','gauge_linear_factors','support'):
                  if row.get(field)!=fresh[field]:
                      counts['tampered']+=1
                      if strict:raise ValueError(f'tampered gauge for {u}->{v}: {field}')
                      break
              else:
                  # Zero at any n>=0 is forbidden, so inverse orientation is
                  # an exact all-index formula transfer as well.
                  if not all(f['a']>0 and f['b']>0 for f in row['gauge_linear_factors']):
                      counts['singular']+=1
                      continue
                  out.append(row);counts['accepted']+=1
    return out,dict(counts)


def ast_weight(expr, end_index):
    """Transparent approximate arithmetic-operation count for a prefix.

    These are not wall-time predictions: they rank routes before timings.
    Binomials / factorials are penalized for independently recomputing them
    at each n; integer size is not modeled.
    """
    if type(expr) is int:return 1
    if not isinstance(expr,dict):return 1000000000
    op=expr.get('op')
    if op in ('n','var'):return 1
    if op in ('add','sub','mul'):
        return 1+sum(ast_weight(e,end_index) for e in expr['args'])
    if op=='pow':return 2+ast_weight(expr['base'],end_index)+ast_weight(expr['exp'],end_index)+max(1,end_index.bit_length())
    if op=='factorial':return 1+ast_weight(expr['arg'],end_index)+5*max(1,end_index)
    if op=='binomial':return 1+ast_weight(expr['n'],end_index)+ast_weight(expr['k'],end_index)+7*max(1,end_index)
    if op=='exact_div':return 3+ast_weight(expr['num'],end_index)+ast_weight(expr['den'],end_index)
    if op=='at':return ast_weight(expr['index'],end_index)+ast_weight(expr['body'],end_index)
    return 10**9


def direct_choice(model: dict, nmax: int):
    if nmax<0:raise ValueError('index bound must be nonnegative')
    # Each sum score is in "abstract ring-operation units", not seconds.
    # A random-access direct call is only charged for a single index when
    # nmax=0. Every other query is a *whole-prefix* query 0..nmax.
    count=nmax+1
    # All values are recomputed, so ordinary binomial formulas grow costly.
    ast_score=max(1,ast_weight(model['ast'],nmax+model['offset']))*count
    ratio=model['ratio']
    factors=sum(abs(p) for p in ratio.factors.values() if p)
    ratio_score=50+count*(4+3*factors) if model['tail']==0 else 10**15
    if ast_score<=ratio_score:
        return int(ast_score),'direct_ast'
    return int(ratio_score),'direct_ratio'


def gauge_score(edge: dict,nmax:int):
    support=sum(abs(f['power']) for f in edge['gauge_linear_factors'])
    return 6+(nmax+1)*(2+3*support+(2 if Fraction(edge['exponential_factor'])!=1 else 0))


@dataclass(frozen=True)
class WorkEdge:
    u: str
    v: str
    cost: int
    kind: str
    record: dict | None
    method: str | None = None


def minimum_work_tree(vertices, links, direct_costs, terminals, *, max_terminals=6):
    """Exact minimum Steiner tree for this finite undirected work graph.

    Models direct computation as a virtual-root edge to *every* eligible
    formula. The selected root-connected tree may share intermediates.
    Complexity is exponential in the number of requested targets, not in the
    size of the OEIS corpus. Recovered edges carry their proof references.
    """
    terminals=tuple(dict.fromkeys(terminals))
    if not terminals or len(terminals)>max_terminals:
        raise ValueError(f'query must have 1..{max_terminals} distinct output targets')
    available=set(vertices)
    if not set(terminals)<=available:raise ValueError('one or more requested outputs have no admissible exact formula')
    names=sorted(available|{ROOT});position={n:i for i,n in enumerate(names)}
    edges=[]
    for u,(cost,method) in sorted(direct_costs.items()):
        if u not in available or cost<0:continue
        edges.append(WorkEdge(ROOT,u,int(cost),'direct',None,method))
    for row in links:
        if row.u not in available or row.v not in available:continue
        if row.cost<=0:raise ValueError('nonpositive transfer edge cost')
        if row.u!=row.v:edges.append(row)
    adj=[[] for _ in names]
    for eid,e in enumerate(edges):
        u=position[e.u];v=position[e.v]
        adj[u].append((v,e.cost,eid));adj[v].append((u,e.cost,eid))
    for row in adj:row.sort(key=lambda item:(item[1], names[item[0]],item[2]))
    k=len(terminals);n=len(names);full=(1<<k)-1
    INF=10**100
    best=[[INF]*n for _ in range(1<<k)]
    back=[[None]*n for _ in range(1<<k)]
    for i,target in enumerate(terminals):
        node=position[target];best[1<<i][node]=0;back[1<<i][node]=('terminal',i)
    for mask in range(1,full+1):
        # Combine two nonempty submasks at one shared intermediate vertex.
        if mask & (mask-1):
            sub=(mask-1)&mask
            while sub:
                other=mask^sub
                if sub<other:
                    a,b=best[sub],best[other];now=best[mask]
                    for v in range(n):
                        candidate=a[v]+b[v]
                        if candidate<now[v]:
                            now[v]=candidate;back[mask][v]=('merge',sub,other)
                sub=(sub-1)&mask
        heap=[(cost,v) for v,cost in enumerate(best[mask]) if cost<INF]
        heapq.heapify(heap)
        while heap:
            cost,u=heapq.heappop(heap)
            if cost!=best[mask][u]:continue
            for v,weight,eid in adj[u]:
                new=cost+weight
                if new<best[mask][v]:
                    best[mask][v]=new;back[mask][v]=('edge',u,eid)
                    heapq.heappush(heap,(new,v))
    root=position[ROOT]
    if best[full][root]>=INF:raise ValueError('no certified computation for the requested targets')
    chosen=set()
    def recover(mask,v):
        mark=back[mask][v]
        if mark is None:raise AssertionError('lost DP reconstruction')
        if mark[0]=='terminal':return
        if mark[0]=='merge':
            recover(mark[1],v);recover(mark[2],v)
        elif mark[0]=='edge':
            chosen.add(mark[2]);recover(mask,mark[1])
        else:raise AssertionError('unknown DP step')
    recover(full,root)
    subadj=defaultdict(list)
    for eid in chosen:
        edge=edges[eid]
        subadj[edge.u].append((edge.v,eid))
        subadj[edge.v].append((edge.u,eid))
    parents={ROOT:None};order=[];queue=deque([ROOT])
    while queue:
        u=queue.popleft()
        for v,eid in sorted(subadj[u]):
            if v in parents:continue
            parents[v]=(u,eid);order.append((u,v,eid));queue.append(v)
    if not set(terminals)<=set(parents):raise AssertionError('DP path lacks a terminal')
    # With strictly positive costs, the union of optimal rooted subtrees is
    # acyclic (otherwise a positive-cost edge can be removed). We still check.
    if len(order)!=len(chosen):raise AssertionError('the returned edge set contains a cycle')
    cost=sum(edges[eid].cost for eid in chosen)
    if cost!=best[full][root]:raise AssertionError('work score does not match exact DP optimum')
    recipes=[]
    for u,v,eid in order:
        e=edges[eid]
        if u==ROOT:
            recipes.append(dict(node=v,method=e.method,depends_on=[],cost=e.cost))
        else:
            recipes.append(dict(node=v,method='gauge',depends_on=[u],cost=e.cost,
                transfer_source=(e.record or {}).get('source'),transfer_target=(e.record or {}).get('target'),
                certificate=e.record))
    return dict(targets=list(terminals),nmax=None,abstract_cost=cost,
        exact_within_model=True,search_algorithm='Dreyfus-Wagner exact Steiner DP',
        model='Undirected certified-gauge graph; independent source costs and symmetric additive edge costs',
        recipes=recipes,graph_nodes=len(names),admissible_edges=len(edges),
        nonclaims=['No historical novelty claim','Cost scores are not runtime measurements',
            'Formula identities do not prove global OEIS identity','Non-gauge transfers and other algorithms are outside this optimization graph'])


@dataclass(frozen=True)
class VerifiedPrefix:
    """An immutable prefix that was fully checksum-audited at admission."""
    oeis_id: str
    nmax: int
    source_sha256: str
    evaluator_sha256: str
    values_sha256: str
    values: tuple[int, ...]

    def __post_init__(self):
        if any(type(v) is not int for v in self.values) or len(self.values)!=self.nmax+1:
            raise ValueError('immutable cache must contain its complete integer prefix')
        digest=hashlib.sha256(json.dumps(self.values,separators=(',',':')).encode()).hexdigest()
        if digest!=self.values_sha256:
            raise ValueError('immutable cache prefix digest mismatch')


def freeze_cache_snapshot(model,snapshot):
    """Pay the full integrity cost once, then reuse immutable coefficients."""
    if not valid_cache_snapshot(model,snapshot,0):
        raise ValueError('cache fingerprint, contents, or source verification failed')
    return VerifiedPrefix(oeis_id=snapshot['oeis_id'],nmax=snapshot['nmax'],
        source_sha256=snapshot['source_sha256'],
        evaluator_sha256=snapshot['evaluator_sha256'],
        values_sha256=snapshot['values_sha256'],values=tuple(snapshot['values']))


def make_cache_snapshot(model,values):
    """Value cache bound to current source + exact evaluator bytes."""
    if not values or any(type(x) is not int for x in values):
        raise ValueError('only nonempty integer prefixes can be cached')
    payload=json.dumps(values,separators=(',',':'))
    return dict(oeis_id=model['oeis_id'],nmax=len(values)-1,
        source_sha256=model['source_sha256'],
        evaluator_sha256=safe_formula_fingerprint(model),
        values_sha256=hashlib.sha256(payload.encode()).hexdigest(),
        values=list(values))


def valid_cache_snapshot(model,snapshot,nmax):
    if isinstance(snapshot,VerifiedPrefix):
        # The tuple and frozen metadata cannot change after the full digest
        # was checked in freeze_cache_snapshot. Validation is O(1) in nmax.
        return (snapshot.oeis_id==model['oeis_id'] and snapshot.nmax>=nmax and
            snapshot.source_sha256==model['source_sha256'] and
            snapshot.evaluator_sha256==safe_formula_fingerprint(model) and
            len(snapshot.values)==snapshot.nmax+1)
    if not isinstance(snapshot,dict):return False
    if snapshot.get('oeis_id')!=model['oeis_id'] or snapshot.get('nmax',-1)<nmax:return False
    if snapshot.get('source_sha256')!=model['source_sha256']:return False
    if snapshot.get('evaluator_sha256')!=safe_formula_fingerprint(model):return False
    values=snapshot.get('values',[])
    if len(values)!=snapshot['nmax']+1 or any(type(x) is not int for x in values):return False
    digest=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()
    return digest==snapshot.get('values_sha256')


def plan_gauge_prefix(models,ledger,targets,nmax,*,strict=True,max_terminals=6,cache=None):
    edges,summary=verified_gauges(models,ledger,strict=strict)
    simple=[]
    for edge in edges:
        simple.append(WorkEdge(edge['source'],edge['target'],gauge_score(edge,nmax),'gauge',edge))
    direct={sid:direct_choice(m,nmax) for sid,m in models.items()}
    if cache:
        for sid,snap in cache.items():
            if sid in models and valid_cache_snapshot(models[sid],snap,nmax):direct[sid]=(0,'cached')
    result=minimum_work_tree(models,simple,direct,targets,max_terminals=max_terminals)
    result['nmax']=nmax
    result['verified_gauge_ledger']=summary
    result['direct_only_cost']=sum(direct[t][0] for t in set(targets))
    result['modeled_savings_factor']=result['direct_only_cost']/result['abstract_cost']
    return result


def _integer(x:Fraction,name,n):
    if x.denominator!=1:raise ArithmeticError(f'{name}({n}) was not an integer')
    return int(x)


def ratio_factor_parts(r, n):
    """Reduce a shift-ratio to one numerator and one denominator integer."""
    num=r.scalar.numerator;den=r.scalar.denominator
    for (a,b),power in r.factors.items():
        if not power:continue
        value=a*n+b
        if value<=0:raise ValueError('ratio factor outside certified positive tail')
        if power>0:num*=value**power
        else:den*=value**(-power)
    return num,den


def evaluate_prefix(model,nmax,method):
    from sequence_holonomic_compiler import fraction_eval
    off=model['offset']
    if method=='direct_ast':
        return [_integer(fraction_eval(model['ast'],off+t),model['oeis_id'],t) for t in range(nmax+1)]
    if method!='direct_ratio':raise ValueError('unknown direct prefix evaluator')
    if model['tail']!=0:raise ValueError('ratio prefix does not cover n=0')
    current=_integer(fraction_eval(model['ast'],off),model['oeis_id'],0)
    out=[current]
    for n in range(nmax):
        num,den=ratio_factor_parts(model['ratio'],n)
        value,mod=divmod(current*num,den)
        if mod:raise ArithmeticError(f'inexact recurrence ratio for {model["oeis_id"]} at index {n+1}')
        current=value
        out.append(current)
    return out


def apply_gauge(source,certificate,forward,nmax):
    """Stream an all-index certified gauge using exact integer arithmetic.

    K c^n L(n)/L(0) is evaluated with integral numerator/denominator
    products, not n successive Fraction allocations. Requires integer output.
    """
    e=oriented_edge(certificate,reverse=not forward)
    if e['tail_start_local']!=0:raise ValueError('only full-prefix transfer certificates are admitted')
    factors=e['gauge_linear_factors']
    scalar=Fraction(e['base_ratio'])/gauge_value(factors,0)
    c=Fraction(e['exponential_factor'])
    cn,cd=scalar.numerator,scalar.denominator
    out=[]
    for n in range(nmax+1):
        num=source[n]*cn;den=cd
        for f in factors:
            q=f['a']*n+f['b'];p=f['power']
            if q<=0:raise ValueError('singular gauge factor')
            if p>0:num*=q**p
            elif p<0:den*=q**(-p)
        value,mod=divmod(num,den)
        if mod:raise ArithmeticError(f'inexact integer gauge at index {n}')
        out.append(value)
        if n<nmax:
            cn*=c.numerator;cd*=c.denominator
            if c.denominator!=1 and c.numerator!=1:
                g=math.gcd(cn,cd)
                if g>1:cn//=g;cd//=g
    return out


def run_plan(plan,models,*,spot_check=True,cache=None):
    nmax=plan['nmax'];computed={}
    for item in plan['recipes']:
        target=item['node'];method=item['method']
        if method=='gauge':
            src=item['depends_on'][0];cert=item['certificate']
            if cert['source']==src and cert['target']==target:forward=True
            elif cert['target']==src and cert['source']==target:forward=False
            else:raise ValueError('incorrect certificate orientation')
            computed[target]=apply_gauge(computed[src],cert,forward,nmax)
        elif method=='cached':
            if not cache or target not in cache or not valid_cache_snapshot(models[target],cache[target],nmax):
                raise ValueError('cached prefix has missing or stale source-bound data')
            values=cache[target].values if isinstance(cache[target],VerifiedPrefix) else cache[target]['values']
            computed[target]=list(values[:nmax+1])
        else:
            computed[target]=evaluate_prefix(models[target],nmax,method)
        if spot_check:
            # Crucially this verifies *formula values*, not the original OEIS
            # sequence beyond its finite excerpt. Includes last requested index.
            checkpoints={0,min(1,nmax),min(4,nmax),nmax}
            for n in checkpoints:
                expected=fraction_eval(models[target]['ast'],models[target]['offset']+n)
                if computed[target][n]!=expected:
                    raise AssertionError(f'plan calculation differs from exact formula {target}({n})')
    return {sid:computed[sid] for sid in plan['targets']}


def independent_plan(models,targets,nmax):
    """Direct per-sequence methods, including all available ratio recurrences."""
    targets=list(dict.fromkeys(targets))
    result=dict(targets=targets,nmax=nmax,
        recipes=[dict(node=sid,method=direct_choice(models[sid],nmax)[1],depends_on=[],cost=direct_choice(models[sid],nmax)[0]) for sid in targets],
        model='No sequence-to-sequence transfers; independently evaluated exact formula expressions',
        exact_within_model=True)
    result['abstract_cost']=sum(x['cost'] for x in result['recipes'])
    return result


def select_measured_strategy(models,shared_plan,*,runs=5):
    """Choose the measured winner for a fixed, repeated whole-prefix workload.

    Calibration is deliberately *not free*: timings include evaluation of
    each candidate plan and must be amortized over subsequent use. The
    competing baseline is independently optimal under the same direct
    formula/ratio *model*, not a straw-man binomial sum.
    """
    if runs<1 or runs>20:raise ValueError('runs must be in 1..20')
    targets=shared_plan['targets'];nmax=shared_plan['nmax']
    direct=independent_plan(models,targets,nmax)
    a=run_plan(shared_plan,models,spot_check=True)
    b=run_plan(direct,models,spot_check=True)
    if a!=b:raise AssertionError('selected transfer route disagrees with independent exact formulas')
    timings={}
    for name,plan in (('shared_transfer',shared_plan),('independent_direct',direct)):
        observed=[]
        for _ in range(runs):
            start=time.perf_counter()
            result=run_plan(plan,models,spot_check=False)
            observed.append(time.perf_counter()-start)
            if result!=a:raise AssertionError('benchmark route changed its exact output')
        timings[name]=dict(median_seconds=statistics.median(observed),samples_seconds=observed)
    winner=min(timings,key=lambda k:timings[k]['median_seconds'])
    fingerprints={sid:dict(source_sha256=models[sid]['source_sha256'],
          evaluator_sha256=safe_formula_fingerprint(models[sid])) for sid in sorted(set(x['node'] for x in shared_plan['recipes'])|set(targets))}
    return dict(status='exact_values_agree',targets=targets,nmax=nmax,runs=runs,
        outputs_checked=len(a)*(nmax+1),winner=winner,timing=timings,
        observed_direct_to_shared_ratio=(timings['independent_direct']['median_seconds']/timings['shared_transfer']['median_seconds']),
        calibration_cost_included_in_benchmark=False,
        calibration_runs_execute_both_algorithms=True,
        source_fingerprints=fingerprints,
        caveat='Machine-specific observed timings for this same prefix workload. Not a global speedup or universally optimal algorithm; calibration itself has a cost.')


def load_project(db_path:Path,chain:Path|None):
    with sqlite3.connect(db_path) as db:
        models,info=load_models(db,chain)
    return models,dict(info)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--extra',type=Path)
    p.add_argument('--gauges',type=Path,required=True)
    p.add_argument('--targets',nargs='+',required=True)
    p.add_argument('--nmax',type=int,default=200)
    p.add_argument('--output',type=Path)
    p.add_argument('--evaluate',action='store_true')
    a=p.parse_args(argv)
    models,info=load_project(a.db,a.extra)
    plan=plan_gauge_prefix(models,a.gauges,a.targets,a.nmax)
    plan['model_load']=info
    if a.evaluate:
        values=run_plan(plan,models)
        plan['evaluation_check']={'status':'passed','target_count':len(values),
            'integers_compared':sum(len(v) for v in values.values()),
            'last_values_digits':{k:len(str(abs(v[-1]))) for k,v in values.items()}}
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in plan.items() if k not in ('recipes','nonclaims')},indent=2))

if __name__=='__main__':main()
