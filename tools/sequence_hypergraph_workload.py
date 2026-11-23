"""Proof-gated exact shared-workload planner for OEIS formula hypergraphs.

Author: Komorebi P.

All claims are about the extracted source formula *expressions*. OEIS's finite
reference prefix does not prove infinite OEIS identities. Hyperedge input
formulas, raw source text, offsets, and symbolic normal forms are rechecked
against the live SQLite source before any edge is admitted. The optimizer is
exact only within its explicitly selected finite set of available actions and
additive arithmetic-work scores, never a claim of globally fastest runtime.

Python 3.10+, standard library. Does not eval or exec imported OEIS text.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import heapq
import json
from pathlib import Path
import sqlite3
import statistics
import time

from sequence_oeis_formula_dependencies import rhs as extract_rhs, safe_parse, eval_arithmetic, IDENTIFIER
from sequence_oeis_hyperedge_proofs import affine, symbolic
from sequence_oeis_symbolic_network import load_formulas, formal_eval
from sequence_linear_identity_compiler import normalized, key as formal_key
from sequence_hypergeometric_gauges import load_models
from sequence_workload_planner import (
    verified_gauges, gauge_score, direct_choice, evaluate_prefix, apply_gauge,
    safe_formula_fingerprint,
)


@dataclass(frozen=True)
class Action:
    target: str
    inputs: tuple[str, ...]
    cost: int
    kind: str  # direct, gauge, or certified_hyperedge
    record: dict | None = None
    method: str | None = None


class PlanningBudgetExceeded(RuntimeError):
    pass


def formula_fingerprint(model):
    """Bind cached computations to formula identity, source and evaluator."""
    data = {'oeis_id': model['oeis_id'], 'source_sha256':model['source_sha256'],
            'offset':model['offset'], 'terms_sha256':model.get('terms_sha256'), 'ep_formula':model['ep']['formula_id'] if model.get('ep') else None,
            'ep_key':model['ep']['key'] if model.get('ep') else None,
            'gauge_formula':model['gauge']['formula_id'] if model.get('gauge') else None,
            'gauge_evaluator':safe_formula_fingerprint(model['gauge']) if model.get('gauge') else None}
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def load_formula_models(db,extra=None):
    """Combine exact EP expression models and admitted gauge evaluators.

    If the two independent formula normalizers disagree, do not mix them in
    a single graph: retain the EP model but disallow incompatible gauges.
    """
    ep, conflicts = load_formulas(db)
    gauges, gauge_info = load_models(db, extra)
    models = {}
    skipped=[]
    for sid in sorted(set(ep)|set(gauges)):
        e=ep.get(sid);g=gauges.get(sid)
        if e is not None and g is not None:
            equivalent=False
            try:
                normal=normalized(g['ast'],g['offset'])
                equivalent=(normal is not None and formal_key(normal)==e['key'] and g['offset']==e['offset']
                            and g['source_sha256']==e['record_sha256'])
            except (ValueError, TypeError, ArithmeticError):pass
            if not equivalent:
                skipped.append(sid);g=None
        source_sha=e['record_sha256'] if e is not None else g['source_sha256']
        models[sid]={'oeis_id':sid,'source_sha256':source_sha,
                     'offset':e['offset'] if e is not None else g['offset'],
                     'ep':e,'gauge':g}
    # Recheck source evidence against CURRENT stored terms. Source hashes and
    # verification flags alone can be stale following a database mutation.
    # This is a finite source-identity gate, not an all-index OEIS theorem.
    rejected=[];checked=0
    from sequence_holonomic_compiler import fraction_eval
    sorted_ids=sorted(models)
    for begin in range(0,len(sorted_ids),700):
        chunk=sorted_ids[begin:begin+700]
        query='SELECT oeis_id,terms_json FROM sequences WHERE oeis_id IN ('+','.join('?'*len(chunk))+')'
        for sid,raw_terms in db.execute(query,chunk):
            model=models[sid];values=json.loads(raw_terms)
            model['terms_sha256']=hashlib.sha256(raw_terms.encode('utf-8')).hexdigest()
            sample=min(12,len(values))
            try:
                for n in range(sample):
                    if model.get('ep') is not None:
                        observed=formal_eval(model['ep']['expression'],n)
                    else:
                        observed=fraction_eval(model['gauge']['ast'],model['offset']+n)
                    if observed!=int(values[n]):raise ValueError('stored OEIS term and formula differ')
                checked+=1
            except (ValueError,ArithmeticError,TypeError,OverflowError,ZeroDivisionError):
                rejected.append(sid)
    for sid in rejected:models.pop(sid,None)
    info={'ep_models':len(ep),'gauge_models':len(gauges),'combined_models':len(models),
          'finite_source_rechecked':checked,'rejected_stale_or_inconsistent_models':rejected,
          'conflicting_ep_models':conflicts,'incompatible_overlapping_models':skipped,
          'excluded_mixed_formula_routes_for_incompatible':True}
    return models, info


def certify_hyperedges(db, ledger, models, *, strict=True, require_multi=True, allow_indexed=False):
    """Reprove every admitted source-bound hyperedge using canonical Q forms."""
    counts=Counter();out=[];seen=set()
    source_text=Path(ledger).read_text(encoding='utf-8')
    try:
        source=json.loads(source_text)
        if isinstance(source,dict):records=source['admissible_edges'] if 'admissible_edges' in source else [source]
        elif isinstance(source,list):records=source
        else:raise ValueError('unsupported ledger root')
    except json.JSONDecodeError:
        records=[json.loads(line) for line in source_text.splitlines() if line.strip()]
    for c in records:
        counts['read']+=1
        target=c.get('target',c.get('oeis_id'))
        input_ids=tuple(c.get('inputs',c.get('input_sequences',())))
        if require_multi and len(input_ids)<2:
            counts['single_input_excluded']+=1;continue
        try:
            if len(input_ids)!=len(set(input_ids)) or target in input_ids:
                raise ValueError('self-loop or duplicated input')
            if target not in models or any(i not in models for i in input_ids):
                raise ValueError('missing source formula')
            m=models[target]
            if not m['ep'] or any(not models[i]['ep'] for i in input_ids):
                raise ValueError('no exact exponential-polynomial formula for node')
            raw_source=db.execute('''SELECT expression FROM formulas
                WHERE formula_id=? AND oeis_id=? AND origin='oeis_formula' ''',
                (c['formula_id'],target)).fetchone()
            if raw_source is None:raise ValueError('source formula record missing')
            text=raw_source[0]
            if hashlib.sha256(text.encode('utf-8')).hexdigest()!=c['source_text_sha256']:
                raise ValueError('stale raw OEIS formula text hash')
            if extract_rhs(text)!=c['rhs']:
                raise ValueError('candidate RHS is not the saved source formula expression')
            tree=safe_parse(c['rhs'])
            if tree is None:raise ValueError('source formula expression is unsafe or unsupported')
            calls=[v for v in ast.walk(tree) if isinstance(v,ast.Call)]
            if {v.func.id for v in calls}!=set(input_ids) or not calls:
                raise ValueError('mismatched dependencies in formula')
            off=m['offset']
            maps=defaultdict(list)
            for call in calls:
                sid=call.func.id
                if not IDENTIFIER.fullmatch(sid) or len(call.args)!=1:
                    raise ValueError('unsupported dependency call')
                # No head/tail padding. Every input must be evaluated at its
                # own local index t when the output is requested at t.
                mrate,intercept=affine(call.args[0],off)
                local_shift=intercept-models[sid]['offset']
                if mrate<1 or local_shift<0:
                    raise ValueError('negative or invalid input index outside all-index domain')
                if not allow_indexed and (mrate,local_shift)!=(1,0):
                    raise ValueError('index shifted, unaligned, or not covered by prefix')
                maps[sid].append((mrate,local_shift))
            expression=symbolic(tree,off,{i:models[i]['ep'] for i in input_ids})
            if formal_key(expression)!=m['ep']['key']:
                raise ValueError('canonical all-index expression identity failed')
            # Numerical checks are diagnostic only, not used to establish proof.
            for n in (0,1,2,5,12):
                if formal_eval(expression,n)!=formal_eval(m['ep']['expression'],n):
                    raise AssertionError('independent exact check failed')
            stamp={i:{'source_sha256':models[i]['source_sha256'],
                      'formula_fingerprint':formula_fingerprint(models[i])}
                   for i in (target,*input_ids)}
            # If the external proof ledger retains raw OEIS record hashes,
            # enforce them as additional independent provenance controls.
            if c.get('target_source_sha256') not in (None,m['source_sha256']):
                raise ValueError('target raw source receipt differs')
            if c.get('input_source_sha256') is not None and any(
                c['input_source_sha256'].get(i)!=models[i]['source_sha256'] for i in input_ids):
                raise ValueError('input raw source receipt differs')
            out.append({'target':target,'inputs':list(input_ids),'rhs':c['rhs'],
                        'formula_id':c['formula_id'],'source_text_sha256':c['source_text_sha256'],
                        'index_maps':{i:[list(v) for v in maps[i]] for i in input_ids},
                        'bindings':stamp,'status':'all_index_extracted_formula_identity',
                        'proof':'Canonical Q-exponential-polynomial equality with aligned indices',
                        'oeis_identification':'finite_prefix_only'})
            counts['certified']+=1
            seen.add((target,input_ids,c['rhs']))
        except (ValueError,TypeError,KeyError,ArithmeticError,AssertionError,OverflowError) as exc:
            counts['rejected']+=1
            if strict:raise ValueError(f'unsafe or stale hyperedge {target}: {exc}') from exc
    return out,dict(counts)


def verified_compatible_gauges(models, raw_gauges):
    """Eliminate gauge edges touching inconsistent formula representations."""
    result=[]
    for row in raw_gauges:
        s,t=row['source'],row['target']
        if s not in models or t not in models:continue
        a,b=models[s].get('gauge'),models[t].get('gauge')
        if a is None or b is None:continue
        if a['formula_id']!=row['source_formula'] or b['formula_id']!=row['target_formula']:
            continue
        result.append(row)
    return result


def direct_cost(model,nmax):
    g=model.get('gauge')
    if g is not None:
        cost,method=direct_choice(g,nmax)
        return max(1,int(cost)),method
    e=model.get('ep')
    if e is None:raise ValueError('no exact model for '+model['oeis_id'])
    complexity=sum(1+len(poly)*3 for poly in e['expression'].values())
    return max(1,20+(nmax+1)*(8+complexity*3)),'direct_ep'


def hyperedge_score(cert,nmax):
    tree=safe_parse(cert['rhs'])
    operations=Counter(type(v.op).__name__ for v in ast.walk(tree)
                       if isinstance(v,(ast.BinOp,ast.UnaryOp)))
    price=2+len(cert['inputs'])+2*(operations['Add']+operations['Sub'])
    price+=4*operations['Mult']+6*operations['Div']+8*operations['Pow']
    return max(1,8+(nmax+1)*price)


def choose_scope(targets,models,gauges,hyperedges,*,max_nodes=18,max_depth=3):
    """Bounded deterministic backward slice. Exact optimum is slice-relative.

    A hyperedge is only added when *all* of its inputs fit the scope. The
    parent gauge graph can be undirected; hyperedges are never reversed.
    """
    targets=tuple(dict.fromkeys(targets))
    if not targets or any(t not in models for t in targets):
        raise ValueError('target missing exact formula')
    if len(targets)>max_nodes:raise ValueError('more targets than permitted nodes')
    incoming=defaultdict(list);neighbors=defaultdict(set)
    for c in hyperedges:incoming[c['target']].append(c)
    for c in gauges:
        a,b=c['source'],c['target'];neighbors[a].add(b);neighbors[b].add(a)
    pool=set(targets);q=deque((sid,0) for sid in targets)
    while q:
        target,depth=q.popleft()
        if depth>=max_depth:continue
        # Hyperedges have priority: preserve every prerequisite together.
        for c in sorted(incoming[target],key=lambda x:(len(x['inputs']),x['rhs'])):
            additions=set(c['inputs'])-pool
            if len(pool)+len(additions)>max_nodes:continue
            for sid in sorted(additions):pool.add(sid);q.append((sid,depth+1))
        for sid in sorted(neighbors[target]):
            if sid not in pool and len(pool)<max_nodes:
                pool.add(sid);q.append((sid,depth+1))
    return tuple(sorted(pool))


def make_actions(models,gauges,hyperedges,scope,nmax):
    nodes=set(scope);actions=[]
    for sid in sorted(nodes):
        cost,method=direct_cost(models[sid],nmax)
        actions.append(Action(sid,(),cost,'direct',None,method))
    for e in gauges:
        a,b=e['source'],e['target']
        if a in nodes and b in nodes:
            cost=gauge_score(e,nmax)
            actions.extend((Action(b,(a,),cost,'gauge',e),
                            Action(a,(b,),cost,'gauge',e)))
    for c in hyperedges:
        if c['target'] in nodes and set(c['inputs'])<=nodes:
            actions.append(Action(c['target'],tuple(c['inputs']),hyperedge_score(c,nmax),
                                  'hyperedge',c))
    return sorted(actions,key=lambda a:(a.target,a.cost,a.kind,a.inputs))


def shortest_derivation(scope,actions,targets,*,cached=(),max_states=120000):
    """Exact minimum-cost derivation in a finite directed AND/OR hypergraph.

    A state is the subset of available computed nodes. Each nonnegative-cost
    action adds one node iff ALL its inputs have been computed. Dijkstra over
    subset states returns an exact shortest dependency DAG in this model.
    No cyclic dependency is ever executed. Stated optimality is restricted to
    the chosen scope, available source methods and additive work scores.
    """
    nodes=tuple(sorted(set(scope)));index={n:i for i,n in enumerate(nodes)}
    if len(nodes)>24:raise ValueError('state-space node count exceeds 24')
    wanted=0;initial=0
    for sid in targets:
        if sid not in index:raise ValueError('target outside scope')
        wanted|=1<<index[sid]
    for sid in cached:
        if sid in index:initial|=1<<index[sid]
    encoded=[]
    for a in actions:
        if a.target not in index or not set(a.inputs)<=set(index):continue
        if a.cost<0:raise ValueError('negative action cost')
        bits=sum(1<<index[x] for x in set(a.inputs))
        encoded.append((1<<index[a.target],bits,a))
    distances={initial:0};parents={};queue=[(0,initial)];expanded=0
    while queue:
        cost,state=heapq.heappop(queue)
        if distances[state]!=cost:continue
        if state&wanted==wanted:
            steps=[]
            while state!=initial:
                old,a=parents[state];steps.append(a);state=old
            steps.reverse()
            return {'score':cost,'steps':steps,'states_expanded':expanded,
                    'states_reached':len(distances),'optimality':'exact_within_selected_scope'}
        expanded+=1
        if expanded>max_states:
            raise PlanningBudgetExceeded('exact search state budget exceeded; no optimality claim')
        for output_bit,input_bits,a in encoded:
            if (state&output_bit) or (state&input_bits)!=input_bits:continue
            next_state=state|output_bit;next_cost=cost+a.cost
            if next_cost<distances.get(next_state,10**100):
                distances[next_state]=next_cost
                parents[next_state]=(state,a)
                heapq.heappush(queue,(next_cost,next_state))
    raise ValueError('no admissible exact computation path')



def required_input_horizons(cert,nmax):
    """Exact prefix horizons for one indexed or polyphase hyperedge.

    If a source is referenced at local index m*t+r, t=0,...,N, its
    required prefix is 0..m*N+r. This handles several references to the
    same source sequence with different shifts without dropping a boundary.
    """
    if type(nmax) is not int or nmax<0:raise ValueError('negative horizon')
    maps=cert['index_maps']
    return {sid:max(m*nmax+r for m,r in maps[sid]) for sid in cert['inputs']}


def run_indexed_hyperedge(cert,models,nmax):
    """Independently evaluate source prefixes at the exact affine horizons."""
    required=required_input_horizons(cert,nmax)
    prefixes={sid:evaluate_model(models[sid],needed,direct_cost(models[sid],needed)[1])
              for sid,needed in required.items()}
    target=cert['target']
    for sid in (target,*cert['inputs']):
        if cert['bindings'][sid]['source_sha256']!=models[sid]['source_sha256'] or \
                cert['bindings'][sid]['formula_fingerprint']!=formula_fingerprint(models[sid]):
            raise ValueError('indexed transfer source changed')
    parsed=safe_parse(cert['rhs'])
    if parsed is None:raise ValueError('unsafe indexed transfer')
    off=models[target]['offset']
    def lookup(sid,n):
        local=n-models[sid]['offset']
        if local<0 or local>=len(prefixes[sid]):raise ValueError('indexed prerequisite horizon exceeded')
        return prefixes[sid][local]
    return [integer_exact(eval_arithmetic(parsed,off+t,lookup),target,t)
            for t in range(nmax+1)]


def cache_snapshot(model,values):
    if not values or any(type(x) is not int for x in values):raise ValueError('invalid cache prefix')
    h=hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()
    return {'oeis_id':model['oeis_id'],'formula_fingerprint':formula_fingerprint(model),
            'nmax':len(values)-1,'values':list(values),'values_sha256':h}


def cache_valid(model,record,nmax):
    if not isinstance(record,dict) or record.get('oeis_id')!=model['oeis_id'] or record.get('nmax',-1)<nmax:return False
    if record.get('formula_fingerprint')!=formula_fingerprint(model):return False
    values=record.get('values')
    if not isinstance(values,list) or len(values)!=record['nmax']+1 or any(type(x) is not int for x in values):return False
    return hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()==record.get('values_sha256')


def plan_prefix(models,gauges,hyperedges,targets,nmax,*,max_nodes=18,max_depth=3,
                max_states=120000,cache=None,scope=None):
    if nmax<0 or nmax>10000:raise ValueError('prefix bound outside 0..10000')
    cache=cache or {}
    scope=choose_scope(targets,models,gauges,hyperedges,max_nodes=max_nodes,max_depth=max_depth) if scope is None else tuple(scope)
    if any(s not in models for s in scope):raise ValueError('invalid scope')
    actions=make_actions(models,gauges,hyperedges,scope,nmax)
    admitted={s for s in scope if s in cache and cache_valid(models[s],cache[s],nmax)}
    result=shortest_derivation(scope,actions,targets,cached=admitted,max_states=max_states)
    stamps={sid:formula_fingerprint(models[sid]) for sid in scope}
    direct=sum(direct_cost(models[t],nmax)[0] for t in set(targets))
    return {'status':'exact_cost_minimum_within_scope','targets':list(dict.fromkeys(targets)),
            'nmax':nmax,'scope':list(scope),'scope_node_count':len(scope),
            'candidate_actions':len(actions),'cached_nodes':sorted(admitted),
            'score':result['score'],'independent_direct_score':direct,
            'estimated_savings':(direct/result['score'] if result['score'] else None),
            'states_expanded':result['states_expanded'],'states_reached':result['states_reached'],
            'optimality':result['optimality'],
            'steps':[{'target':a.target,'inputs':list(a.inputs),'kind':a.kind,
                      'cost':a.cost,'record':a.record,'method':a.method} for a in result['steps']],
            'model_fingerprints':stamps,
            'proof_scope':'all-index extracted-formula identities; OEIS global identity unproved',
            'cost_scope':'additive heuristic; optimal only within enumerated scope and actions, not wall-clock optimal'}


def integer_exact(value,sid,n):
    value=Fraction(value)
    if value.denominator!=1:raise ArithmeticError(f'{sid}[{n}] is not an integer')
    return int(value)


def evaluate_model(model,nmax,method):
    if method=='direct_ep':
        exp=model['ep']['expression']
        return [integer_exact(formal_eval(exp,n),model['oeis_id'],n) for n in range(nmax+1)]
    if not model['gauge']:raise ValueError('missing exact one-term formula for '+method)
    return evaluate_prefix(model['gauge'],nmax,method)


def apply_hyperedge(prefixes,cert,models,nmax):
    target=cert['target'];inputs=cert['inputs']
    for sid in [target,*inputs]:
        if cert['bindings'][sid]['formula_fingerprint']!=formula_fingerprint(models[sid]) or cert['bindings'][sid]['source_sha256']!=models[sid]['source_sha256']:
            raise ValueError('hyperedge source model has changed')
    expr=safe_parse(cert['rhs'])
    if expr is None:raise ValueError('unsafe hyperedge expression')
    off=models[target]['offset']
    def lookup(sid,mathematical_index):
        if sid not in prefixes:raise ValueError('missing hyperedge input')
        ix=mathematical_index-models[sid]['offset']
        if ix<0 or ix>nmax:raise ValueError('unsupported index shift in hyperedge')
        return prefixes[sid][ix]
    return [integer_exact(eval_arithmetic(expr,off+n,lookup),target,n) for n in range(nmax+1)]


def run_plan(plan,models,*,cache=None,spot_check=True):
    cache=cache or {};nmax=plan['nmax'];computed={}
    for sid in plan['cached_nodes']:
        if not cache_valid(models[sid],cache.get(sid),nmax):raise ValueError('stale or forged cache')
        computed[sid]=list(cache[sid]['values'][:nmax+1])
    for step in plan['steps']:
        sid=step['target'];deps=step['inputs'];kind=step['kind'];cert=step['record']
        for x in (sid,*deps):
            if plan['model_fingerprints'][x]!=formula_fingerprint(models[x]):
                raise ValueError('source changed after planning: '+x)
        if sid in computed:raise AssertionError('duplicate evaluation in DAG')
        if any(d not in computed for d in deps):raise AssertionError('unavailable prerequisite')
        if kind=='direct':
            vals=evaluate_model(models[sid],nmax,step['method'])
        elif kind=='gauge':
            src=deps[0];forward=(cert['source']==src and cert['target']==sid)
            if not forward and not (cert['target']==src and cert['source']==sid):
                raise ValueError('wrong gauge direction')
            vals=apply_gauge(computed[src],cert,forward,nmax)
        elif kind=='hyperedge':
            if cert['target']!=sid or tuple(cert['inputs'])!=tuple(deps):raise ValueError('hyperedge mismatch')
            vals=apply_hyperedge(computed,cert,models,nmax)
        else:raise ValueError('unsupported step')
        computed[sid]=vals
        if spot_check:
            checkpoints={0,1 if nmax else 0,nmax//2,nmax}
            for n in checkpoints:
                if models[sid].get('ep'):
                    exact=integer_exact(formal_eval(models[sid]['ep']['expression'],n),sid,n)
                elif models[sid].get('gauge'):
                    exact=evaluate_model(models[sid],n,'direct_ast')[-1]
                else:raise ValueError('node lacks proof-bound formula')
                if vals[n]!=exact:raise AssertionError(f'incorrect DAG computation {sid}[{n}]')
    if any(sid not in computed for sid in plan['targets']):raise AssertionError('missing requested output')
    return {sid:computed[sid] for sid in plan['targets']}



def measured_strategy(models,plan,*,runs=3,cache=None):
    """Exact-agreement-checked calibration of shared DAG vs direct evaluation.

    Benchmarking both alternatives costs time. The selected result is a
    workload-specific measurement, not a general-performance theorem.
    """
    if type(runs) is not int or not 1<=runs<=15:raise ValueError('runs must be in 1..15')
    targets=plan['targets'];nmax=plan['nmax']
    def independent():
        return {sid:evaluate_model(models[sid],nmax,direct_cost(models[sid],nmax)[1])
                for sid in targets}
    expected=independent()
    if run_plan(plan,models,cache=cache,spot_check=True)!=expected:
        raise AssertionError('shared DAG disagrees with independent source formulas')
    times={};total_calibration=0.0
    for name,operation in (('shared_dag',lambda:run_plan(plan,models,cache=cache,spot_check=False)),
                           ('independent',independent)):
        trial=[]
        for _ in range(runs):
            start=time.perf_counter();values=operation();elapsed=time.perf_counter()-start
            total_calibration+=elapsed
            if values!=expected:raise AssertionError('benchmark output changed')
            trial.append(elapsed)
        times[name]={'median_seconds':statistics.median(trial),'samples_seconds':trial}
    selected=min(times,key=lambda x:times[x]['median_seconds'])
    return {'status':'exact_value_agreement','winner':selected,'targets':targets,'nmax':nmax,
        'output_values_compared':len(targets)*(nmax+1),'runs':runs,
        'timings':times,'calibration_elapsed_seconds':total_calibration,
        'independent_to_shared_ratio':times['independent']['median_seconds']/times['shared_dag']['median_seconds'],
        'scope':'Source-bound extracted formula values, not independent OEIS all-index identities',
        'warning':'Timing winner is machine- and workload-specific. Calibration executes both strategies.'}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',type=Path,required=True)
    parser.add_argument('--hyperedges',type=Path,required=True)
    parser.add_argument('--gauges',type=Path,required=True)
    parser.add_argument('--extra',type=Path)
    parser.add_argument('--targets',nargs='+',required=True)
    parser.add_argument('--nmax',type=int,default=30)
    parser.add_argument('--max-nodes',type=int,default=18)
    parser.add_argument('--max-depth',type=int,default=3)
    parser.add_argument('--max-states',type=int,default=120000)
    parser.add_argument('--output',type=Path)
    a=parser.parse_args(argv)
    with sqlite3.connect(a.db) as db:
        models,source_info=load_formula_models(db,a.extra)
        all_hypers,hyper_info=certify_hyperedges(db,a.hyperedges,models,
                                                 require_multi=False,allow_indexed=True)
        raw_gauge_models,_=load_models(db,a.extra)
    hypers=[c for c in all_hypers if all(v==[1,0] for maps in c['index_maps'].values() for v in maps)]
    approved,gs=verified_gauges(raw_gauge_models,a.gauges)
    gauges=verified_compatible_gauges(models,approved)
    p=plan_prefix(models,gauges,hypers,a.targets,a.nmax,max_nodes=a.max_nodes,max_depth=a.max_depth,max_states=a.max_states)
    p['data_audit']={'source_models':source_info,'hyperedge_ledger':hyper_info,
                     'all_index_formula_hyperedges':len(all_hypers),
                     'prefix_aligned_optimizer_hyperedges':len(hypers),
                     'indexed_hyperedges_not_in_uniform_horizon_optimizer':len(all_hypers)-len(hypers),
                     'certified_gauges':len(gauges),'gauge_ledger':gs}
    values=run_plan(p,models)
    p['evaluation_check']={'status':'passed','values_compared':sum(map(len,values.values())),
                           'terminal_digit_counts':{sid:len(str(abs(seq[-1]))) for sid,seq in values.items()}}
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(p,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in p.items() if k not in ('steps','model_fingerprints')},indent=2))


if __name__=='__main__':main()
