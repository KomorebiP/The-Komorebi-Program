"""Proof-bound variable-horizon computation DAGs for Komorebi/OEIS.

Author: Komorebi P.

An all-index hyperedge from target-local n to source-local m*n+r pulls a
requested 0..H prefix back to 0..m*H+r. This planner records exact, separate
prefix horizons per node, and uses Dijkstra on a finite vector-of-horizons
state space. Cost optimality is relative to the explicitly enumerated horizons,
actions, and additive *full-prefix recomputation* score, not elapsed time.

The accepted identities relate extracted source formulas, not all-index OEIS
sequence identifications. OEIS text is never evaluated as program code.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import defaultdict, deque, Counter
import ast
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import heapq
import itertools
import json
import sqlite3
import statistics
import time
from pathlib import Path
import argparse

from sequence_hypergraph_workload import (
    PlanningBudgetExceeded, load_formula_models, certify_hyperedges,
    verified_compatible_gauges, choose_scope, direct_cost, hyperedge_score,
    evaluate_model, integer_exact, formula_fingerprint, cache_valid,
    required_input_horizons,
)
from sequence_workload_planner import verified_gauges, gauge_score, apply_gauge
from sequence_hypergeometric_gauges import load_models, certify_pair
from sequence_oeis_formula_dependencies import safe_parse, eval_arithmetic
from sequence_oeis_hyperedge_proofs import symbolic, affine
from sequence_linear_identity_compiler import key as formal_key
from sequence_oeis_symbolic_network import formal_eval


@dataclass(frozen=True)
class HorizonAction:
    target: str
    horizon: int
    inputs: tuple[str, ...]
    needs: tuple[int, ...]
    cost: int
    kind: str
    record: dict | None = None
    method: str | None = None

    def as_dict(self):
        return {'target':self.target,'horizon':self.horizon,
                'inputs':list(self.inputs),'required_horizons':dict(zip(self.inputs,self.needs)),
                'cost':self.cost,'kind':self.kind,'record':self.record,'method':self.method}


def _max_source_index(cert, sid, h):
    return max(m*h+r for m,r in cert['index_maps'][sid])


def candidate_horizons(scope, gauges, hyperedges, targets, requested,
                       *, depth=3, cap=10000, max_levels=16):
    """Finite backward demand closure; cap and depth are explicit search bounds.

    Each generated horizon is the smallest exact demand from an eligible edge.
    An impossible high-horizon edge is omitted rather than silently truncated.
    """
    if not isinstance(requested,int) or isinstance(requested,bool) or requested<0:
        raise ValueError('requested horizon must be a nonnegative integer')
    if not isinstance(depth,int) or depth<0 or depth>12:
        raise ValueError('depth outside 0..12')
    if not isinstance(cap,int) or cap<requested:
        raise ValueError('index cap lower than requested horizon')
    if not isinstance(max_levels,int) or max_levels<1:
        raise ValueError('max_levels must be positive')
    names=set(scope)
    if not set(targets)<=names:raise ValueError('target outside selected scope')
    incoming=defaultdict(list);neighbors=defaultdict(set)
    for c in hyperedges:
        if c['target'] in names and set(c['inputs'])<=names:
            incoming[c['target']].append(c)
    for g in gauges:
        a,b=g['source'],g['target']
        if a in names and b in names:
            neighbors[a].add(b);neighbors[b].add(a)
    demands={sid:set() for sid in scope}
    q=deque()
    for sid in dict.fromkeys(targets):
        demands[sid].add(requested);q.append((sid,requested,0))
    omitted=0
    while q:
        sid,h,d=q.popleft()
        if d>=depth:continue
        for cert in incoming[sid]:
            req=required_input_horizons(cert,h)
            if max(req.values(),default=0)>cap:
                omitted+=1;continue
            for src,k in req.items():
                if k not in demands[src]:
                    demands[src].add(k)
                    if len(demands[src])>max_levels:
                        raise PlanningBudgetExceeded('horizon tier budget exceeded; no optimality claim')
                    q.append((src,k,d+1))
        for src in neighbors[sid]:
            if h not in demands[src]:
                demands[src].add(h)
                if len(demands[src])>max_levels:
                    raise PlanningBudgetExceeded('horizon tier budget exceeded; no optimality claim')
                q.append((src,h,d+1))
    return {sid:tuple(sorted(v)) for sid,v in demands.items()}, {'omitted_over_cap':omitted,
        'horizon_search_depth':depth,'horizon_cap':cap,'max_levels':max_levels,
        'nonempty_tiers':sum(bool(x) for x in demands.values()),
        'tier_count':sum(map(len,demands.values()))}


def make_horizon_actions(models,gauges,hyperedges,tiers):
    names={sid for sid,levels in tiers.items() if levels}
    out=[];rejected=0
    def possible(src,k):
        return src in names and tiers[src][-1]>=k
    for sid in sorted(names):
        for h in tiers[sid]:
            cost,method=direct_cost(models[sid],h)
            out.append(HorizonAction(sid,h,(),(),cost,'direct',method=method))
    for gauge in gauges:
        a,b=gauge['source'],gauge['target']
        for src,tgt in ((a,b),(b,a)):
            if tgt not in names or src not in names:continue
            for h in tiers[tgt]:
                if possible(src,h):
                    out.append(HorizonAction(tgt,h,(src,),(h,),gauge_score(gauge,h),'gauge',gauge))
    for cert in hyperedges:
        t=cert['target']
        if t not in names or not set(cert['inputs'])<=names:continue
        for h in tiers[t]:
            req=required_input_horizons(cert,h)
            if all(possible(src,k) for src,k in req.items()):
                out.append(HorizonAction(t,h,tuple(cert['inputs']),tuple(req[s] for s in cert['inputs']),
                                         hyperedge_score(cert,h),'hyperedge',cert))
            else:rejected+=1
    if any(x.cost<0 for x in out):raise ValueError('negative action cost')
    out.sort(key=lambda a:(a.target,a.horizon,a.cost,a.kind,a.inputs))
    return out,{'actions':len(out),'hyperedge_actions_infeasible_horizon':rejected,
                'direct_actions':sum(a.kind=='direct' for a in out),
                'gauge_actions':sum(a.kind=='gauge' for a in out),
                'hyperedge_actions':sum(a.kind=='hyperedge' for a in out)}


def shortest_horizon_derivation(tiers,actions,targets,requested,*,cache_horizons=None,max_states=100000):
    """Dijkstra gives a precise minimum in the finite full-prefix cost model.

    A state records the highest available prefix of EACH node. Computing a
    longer prefix replaces the earlier prefix, and pays the full chosen action
    cost, including recomputation. All costs are nonnegative. No action can
    consume its own output before it has been produced (no cyclic execution).
    """
    if not 1<=len(tiers)<=18:raise ValueError('state count limit: at most 18 nodes')
    nodes=tuple(sorted(tiers));pos={s:i for i,s in enumerate(nodes)}
    cache_horizons=cache_horizons or {}
    initial=tuple(max(0,bisect_right(tiers[sid],cache_horizons.get(sid,-1))) for sid in nodes)
    wanted={sid:bisect_left(tiers[sid],requested)+1 for sid in dict.fromkeys(targets)}
    if any(s not in pos or wanted[s]>len(tiers[s]) for s in wanted):raise ValueError('no target horizon tier')
    encoded=[]
    for a in actions:
        if a.target not in pos or a.horizon not in tiers[a.target]:continue
        if any(s not in pos or not tiers[s] or tiers[s][-1]<h for s,h in zip(a.inputs,a.needs)):
            continue
        required=tuple((pos[s],bisect_left(tiers[s],h)+1) for s,h in zip(a.inputs,a.needs))
        encoded.append((pos[a.target],bisect_left(tiers[a.target],a.horizon)+1,required,a))
    if not all(s in pos for s in wanted):raise ValueError('unknown target')
    def finish(state):return all(state[pos[s]]>=level for s,level in wanted.items())
    heap=[(0,0,initial)];counter=itertools.count(1);best={initial:0};parent={};expanded=0
    while heap:
        cost,_,state=heapq.heappop(heap)
        if cost!=best[state]:continue
        if finish(state):
            steps=[];last=state
            while last!=initial:
                old,a=parent[last];steps.append(a);last=old
            steps.reverse()
            return {'score':cost,'actions':steps,'states_expanded':expanded,
                    'states_reached':len(best),'optimality':'exact_in_enumerated_horizon_state_graph'}
        expanded+=1
        if expanded>max_states:raise PlanningBudgetExceeded('state search budget exceeded; no optimality claim')
        for tindex,tlevel,req,a in encoded:
            if state[tindex]>=tlevel or any(state[ix]<lv for ix,lv in req):continue
            next_state=state[:tindex]+(tlevel,)+state[tindex+1:]
            proposed=cost+a.cost
            if proposed<best.get(next_state,10**200):
                best[next_state]=proposed;parent[next_state]=(state,a)
                heapq.heappush(heap,(proposed,next(counter),next_state))
    raise ValueError('no admissible horizon-aware computation path')


def plan_variable_horizon(models,gauges,hyperedges,targets,nmax,*,scope=None,
                          max_nodes=12,max_depth=3,cap=10000,max_levels=16,max_states=100000,
                          cache=None):
    if type(nmax) is not int or not 0<=nmax<=cap:raise ValueError('requested horizon outside allowed range')
    cache=cache or {}
    targets=tuple(dict.fromkeys(targets))
    if not targets or any(t not in models for t in targets):raise ValueError('unknown target')
    if scope is None:
        scope=choose_scope(targets,models,gauges,hyperedges,max_nodes=max_nodes,max_depth=max_depth)
    else:scope=tuple(dict.fromkeys(scope))
    if len(scope)>max_nodes or not set(targets)<=set(scope) or any(s not in models for s in scope):
        raise ValueError('scope exceeds node limit or contains missing formulas')
    tiers,tier_report=candidate_horizons(scope,gauges,hyperedges,targets,nmax,
                                          depth=max_depth,cap=cap,max_levels=max_levels)
    actions,action_report=make_horizon_actions(models,gauges,hyperedges,tiers)
    valid_cache={sid:cache[sid]['nmax'] for sid in tiers if sid in cache and cache_valid(models[sid],cache[sid],0)}
    answer=shortest_horizon_derivation(tiers,actions,targets,nmax,
                                       cache_horizons=valid_cache,max_states=max_states)
    direct_total=sum(direct_cost(models[s],nmax)[0] for s in targets)
    return {'version':'1.3','targets':list(targets),'requested_horizon':nmax,'scope':list(scope),
            'horizon_tiers':{sid:list(v) for sid,v in tiers.items()},
            'score':answer['score'],'independent_direct_score':direct_total,
            'states_expanded':answer['states_expanded'],'states_reached':answer['states_reached'],
            'steps':[a.as_dict() for a in answer['actions']],
            'cached_prefix_horizons':valid_cache,
            'model_fingerprints':{sid:formula_fingerprint(models[sid]) for sid in scope},
            'enumeration':{**tier_report,**action_report,'max_states':max_states},
            'optimality':answer['optimality'],
            'cost_scope':'full-prefix recomputation work score, not elapsed time or global optimum',
            'proof_scope':'all-index identities of extracted formulas, not OEIS sequence identifications'}


def apply_certified_indexed_hyperedge(prefixes, cert, models, h, *,verify_algebra=True):
    t=cert['target'];inputs=cert['inputs']
    required=required_input_horizons(cert,h)
    if any(s not in prefixes or len(prefixes[s])<=needed for s,needed in required.items()):
        raise ValueError('insufficient indexed source prefix')
    for sid in (t,*inputs):
        stamp=cert['bindings'][sid]
        if stamp['source_sha256']!=models[sid]['source_sha256'] or \
                stamp['formula_fingerprint']!=formula_fingerprint(models[sid]):
            raise ValueError('indexed hyperedge formula or provenance changed')
    expr=safe_parse(cert['rhs'])
    if expr is None:raise ValueError('unsafe hyperedge expression')
    # The horizon map is proof-relevant data. Recompute it from the exact
    # source AST, rather than trusting an external serialized index map.
    observed=defaultdict(Counter)
    for call in ast.walk(expr):
        if not isinstance(call,ast.Call):continue
        if not isinstance(call.func,ast.Name) or call.func.id not in inputs or len(call.args)!=1:
            raise ValueError('unexpected dependency in certified expression')
        sid=call.func.id
        m,intercept=affine(call.args[0],models[t]['offset'])
        shift=intercept-models[sid]['offset']
        if type(m) is not int or type(shift) is not int or m<1 or shift<0:
            raise ValueError('invalid affine source domain')
        observed[sid][(m,shift)]+=1
    expected={sid:Counter(tuple(pair) for pair in cert['index_maps'][sid]) for sid in inputs}
    if set(observed)!=set(inputs) or any(observed[sid]!=expected[sid] for sid in inputs):
        raise ValueError('source-index maps differ from the certified formula')
    if verify_algebra:
        source={sid:models[sid]['ep'] for sid in inputs}
        if any(model is None for model in source.values()) or models[t]['ep'] is None:
            raise ValueError('exact algebra certificate model unavailable')
        identity=symbolic(expr,models[t]['offset'],source)
        if formal_key(identity)!=models[t]['ep']['key']:
            raise ValueError('hyperedge no longer satisfies the all-index algebraic identity')
    def lookup(sid,mathematical_index):
        ix=mathematical_index-models[sid]['offset']
        if ix<0 or ix>=len(prefixes[sid]):raise ValueError('source index outside certified prefix')
        return prefixes[sid][ix]
    off=models[t]['offset']
    return [integer_exact(eval_arithmetic(expr,off+n,lookup),t,n) for n in range(h+1)]


def run_variable_plan(plan, models, *,cache=None,spot_check=True,verify_cached_values=True):
    cache=cache or {};computed={};validated={}
    for sid,h in plan['cached_prefix_horizons'].items():
        snap=cache.get(sid)
        if snap is None or not cache_valid(models[sid],snap,h):
            raise ValueError('missing, corrupted or source-stale cached prefix')
        computed[sid]=list(snap['values']);validated[sid]=len(computed[sid])-1
        if verify_cached_values:
            direct_method=direct_cost(models[sid],validated[sid])[1]
            if evaluate_model(models[sid],validated[sid],direct_method)!=computed[sid]:
                raise ValueError('cached content differs from its exact source formula')
    for s in plan['scope']:
        if plan['model_fingerprints'][s]!=formula_fingerprint(models[s]):
            raise ValueError('formula changed since query planning')
    step_receipts=[]
    for item in plan['steps']:
        t=item['target'];h=item['horizon'];inputs=item['inputs']
        req=item['required_horizons'];kind=item['kind'];rec=item['record']
        if t not in plan['scope'] or h<=validated.get(t,-1):
            raise ValueError('duplicate, shrinking or out-of-scope execution')
        if any(s not in computed or len(computed[s])<=req[s] for s in inputs):
            raise ValueError('missing indexed prerequisite')
        if kind=='direct':
            if inputs or rec is not None:raise ValueError('malformed direct action')
            expected_cost,method=direct_cost(models[t],h)
            if method!=item['method'] or expected_cost!=item['cost']:
                raise ValueError('modified direct evaluator or cost')
            result=evaluate_model(models[t],h,method)
        elif kind=='gauge':
            if len(inputs)!=1 or req!={inputs[0]:h} or gauge_score(rec,h)!=item['cost']:
                raise ValueError('modified gauge action')
            forward=rec['source']==inputs[0] and rec['target']==t
            if not forward and not(rec['target']==inputs[0] and rec['source']==t):
                raise ValueError('wrong gauge direction')
            # Re-derive the algebraic gauge, including all source receipts,
            # even if the caller disables optional value spot checks.
            src=rec['source'];dst=rec['target']
            if src not in models or dst not in models or not models[src].get('gauge') or not models[dst].get('gauge'):
                raise ValueError('gauge lacks source formula')
            a,b=models[src]['gauge'],models[dst]['gauge']
            for field,actual in (('source_formula',a['formula_id']),('target_formula',b['formula_id']),
                                 ('source_sha256',a['source_sha256']),('target_sha256',b['source_sha256'])):
                if rec.get(field)!=actual:raise ValueError('gauge source identity mismatch')
            proof=certify_pair(a,b,max_support=max(4,rec['support']))
            fields=('tail_start_local','base_ratio','exponential_factor','gauge_linear_factors','support')
            if proof is None or any(rec.get(k)!=proof.get(k) for k in fields):
                raise ValueError('gauge no longer has its all-index transfer certificate')
            result=apply_gauge(computed[inputs[0]][:h+1],rec,forward,h)
        elif kind=='hyperedge':
            if rec['target']!=t or tuple(rec['inputs'])!=tuple(inputs) or \
                    req!=required_input_horizons(rec,h) or hyperedge_score(rec,h)!=item['cost']:
                raise ValueError('modified indexed hyperedge')
            result=apply_certified_indexed_hyperedge(computed,rec,models,h)
        else:raise ValueError('unknown computation type')
        if len(result)!=h+1 or any(type(x) is not int for x in result):
            raise ArithmeticError('invalid integer prefix')
        if spot_check:
            checkpoints={0,h//3,h//2,h}
            for n in checkpoints:
                model=models[t]
                if model.get('ep'):
                    true=integer_exact(formal_eval(model['ep']['expression'],n),t,n)
                else:
                    true=evaluate_model(model,n,'direct_ast')[-1]
                if true!=result[n]:raise AssertionError('computed formula differs from exact source')
        computed[t]=result;validated[t]=h
        step_receipts.append({'target':t,'horizon':h,'kind':kind,
                              'required_horizons':req,'length':len(result),
                              'sha256':hashlib.sha256(json.dumps(result,separators=(',',':')).encode()).hexdigest()})
    requested=plan['requested_horizon']
    if any(t not in computed or len(computed[t])<=requested for t in plan['targets']):
        raise AssertionError('requested prefix not fully computed')
    values={t:computed[t][:requested+1] for t in plan['targets']}
    return values,step_receipts



def measured_variable_strategy(plan, models, *,cache=None,runs=3):
    """Calibrate two exact strategies and report the actual measured winner.

    Calibration evaluates *both* alternatives. Source checking and cache
    authentication occur on each timed shared execution. This is a local
    workload measurement, not an analytical complexity upper bound.
    """
    if type(runs) is not int or not 1<=runs<=10:raise ValueError('runs must be 1..10')
    cache=cache or {}
    n=plan['requested_horizon']
    def independent():
        return {sid:evaluate_model(models[sid],n,direct_cost(models[sid],n)[1])
                for sid in plan['targets']}
    def compiled():return run_variable_plan(plan,models,cache=cache,spot_check=False)[0]
    expected=independent()
    if compiled()!=expected:raise AssertionError('certified planner disagrees with independent exact formulas')
    timings={}
    for label,work in (('independent',independent),('variable_horizon_dag',compiled)):
        samples=[]
        for _ in range(runs):
            now=time.perf_counter()
            actual=work()
            samples.append(time.perf_counter()-now)
            if actual!=expected:raise AssertionError('calibrated outputs are not exact')
        timings[label]={'median_seconds':statistics.median(samples),'samples_seconds':samples}
    winner=min(timings,key=lambda k:timings[k]['median_seconds'])
    return {'winner':winner,'target_count':len(expected),'values_compared':len(expected)*(n+1),
            'timings':timings,'runs':runs,'calibration_performed':True,
            'scope':'source-formula exact outputs and machine-specific execution time',
            'cost_note':'Both strategies are executed during calibration; validation and proof replay are not free.'}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',required=True,type=Path)
    p.add_argument('--hyperedges',required=True,type=Path)
    p.add_argument('--gauges',required=True,type=Path)
    p.add_argument('--extra',type=Path)
    p.add_argument('--targets',nargs='+',required=True)
    p.add_argument('--nmax',type=int,default=30)
    p.add_argument('--max-nodes',type=int,default=10)
    p.add_argument('--max-depth',type=int,default=2)
    p.add_argument('--max-states',type=int,default=25000)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        models,model_info=load_formula_models(db,args.extra)
        hyperedges,hyperedge_info=certify_hyperedges(db,args.hyperedges,models,
                                                       require_multi=False,allow_indexed=True)
        gauge_models,_=load_models(db,args.extra)
    ok, gauge_info=verified_gauges(gauge_models,args.gauges)
    gauges=verified_compatible_gauges(models,ok)
    plan=plan_variable_horizon(models,gauges,hyperedges,args.targets,args.nmax,
                              max_nodes=args.max_nodes,max_depth=args.max_depth,max_states=args.max_states)
    outputs,receipts=run_variable_plan(plan,models)
    plan['source_audit']={'models':model_info,'hyperedges':hyperedge_info,
                          'verified_gauges':len(gauges),'gauge_ledger':gauge_info}
    plan['execution_check']={'status':'passed','prefix_values':sum(map(len,outputs.values())),
                             'step_receipts':receipts}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(plan,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({key:val for key,val in plan.items() if key not in ('steps','model_fingerprints','source_audit')},indent=2))


if __name__=='__main__':main()
