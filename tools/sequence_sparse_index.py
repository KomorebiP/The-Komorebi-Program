"""Exact sparse-index workload planning on source-bound OEIS formula hyperedges.

Author: Komorebi P.

Unlike v1.3, a task is (sequence, *individual local index*). A certified
hyperedge pulls back the finite index SET it needs, without requiring a
contiguous prefix. Dijkstra minimizes an explicit nonnegative action score
on the finite AND/OR task graph. All supported mathematical identities are
rederived algebraically from source formula models. OEIS identification is
still only finite-prefix checked, NOT an all-index OEIS theorem.

Optional C-finite packet jumping uses polynomial/exponential normal forms;
its recurrence follows from (S-lambda)^d annihilators, not interpolation.
"""
from __future__ import annotations

import ast
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import heapq
import itertools
import json

from sequence_hypergraph_workload import formula_fingerprint, integer_exact, PlanningBudgetExceeded
from sequence_oeis_formula_dependencies import safe_parse, eval_arithmetic, rhs as source_rhs
from sequence_oeis_hyperedge_proofs import affine, symbolic
from sequence_oeis_symbolic_network import formal_eval
from sequence_linear_identity_compiler import key as formal_key
from sequence_exponential_polynomial import recurrence_from_roots
from sequence_recurrence_packets import x_packet
from sequence_sparse_packets import SparsePacketBank


@dataclass(frozen=True)
class SparseAction:
    target: tuple[str,int]
    inputs: tuple[tuple[str,int], ...]
    cost: int
    kind: str
    certificate: dict | None = None
    method: str = 'formula'

    def view(self):
        return {'target':[self.target[0],self.target[1]],
                'inputs':[[s,n] for s,n in self.inputs],
                'cost':self.cost,'kind':self.kind,'method':self.method,
                'certificate_formula':self.certificate.get('formula_id') if self.certificate else None}


def checked_task(sid,n,models,max_index):
    if sid not in models or type(n) is not int or not 0<=n<=max_index:
        raise ValueError('invalid or unbounded sparse task')
    return (sid,n)


def _calls(tree):
    return [v for v in ast.walk(tree) if isinstance(v,ast.Call)]


def certify_sparse_edge(cert,models,db=None):
    """Recheck certificate bindings, actual index maps and exact symbolic identity.

    This validates a *formula* identity; no raw OEIS text or source program is
    executed. The source text hash is established during original admission.
    """
    t=cert['target'];sources=tuple(cert['inputs'])
    if db is not None:
        source_row=db.execute('''SELECT expression FROM formulas
            WHERE formula_id=? AND oeis_id=? AND origin='oeis_formula' ''',
            (cert.get('formula_id'),t)).fetchone()
        if source_row is None:
            raise ValueError('original OEIS formula source missing')
        source_text=source_row[0]
        if (hashlib.sha256(source_text.encode()).hexdigest()!=cert.get('source_text_sha256')
                or source_rhs(source_text)!=cert['rhs']):
            raise ValueError('stale OEIS formula text; recertification required')
    if t not in models or any(s not in models for s in sources) or t in sources:
        raise ValueError('missing, repeated or self-referential certificate input')
    for sid in (t,*sources):
        model=models[sid];stamp=cert['bindings'][sid]
        if (model['source_sha256']!=stamp['source_sha256'] or
                formula_fingerprint(model)!=stamp['formula_fingerprint']):
            raise ValueError('source-bound formula fingerprint changed')
        if model.get('ep') is None:raise ValueError('formula lacks exact EP representation')
    tree=safe_parse(cert['rhs'])
    if tree is None:raise ValueError('unsafe formula text')
    found=defaultdict(Counter)
    for call in _calls(tree):
        sid=call.func.id
        if sid not in sources:raise ValueError('unexpected sequence dependency')
        slope,shift=affine(call.args[0],models[t]['offset'])
        local_shift=shift-models[sid]['offset']
        if type(slope) is not int or type(local_shift) is not int or slope<1 or local_shift<0:
            raise ValueError('invalid source-local index map')
        found[sid][(slope,local_shift)]+=1
    expected={sid:Counter(tuple(x) for x in cert['index_maps'][sid]) for sid in sources}
    if set(found)!=set(sources) or found!=expected:
        raise ValueError('altered dependency index maps')
    out=symbolic(tree,models[t]['offset'],{sid:models[sid]['ep'] for sid in sources})
    if formal_key(out)!=models[t]['ep']['key']:
        raise ValueError('all-index symbolic formula identity failed')
    return tree


def needed_indices(cert,n):
    if type(n) is not int or n<0:raise ValueError('negative local index')
    return tuple(sorted({(sid,m*n+r)
                         for sid in cert['inputs'] for m,r in cert['index_maps'][sid]}))


def source_requirements(cert,indices):
    """Union of exact source-index sets for sparse requested output indices."""
    if any(type(n) is not int or n<0 for n in indices):raise ValueError('bad index set')
    return tuple(sorted({pair for n in indices for pair in needed_indices(cert,n)}))


def packet_from_ep(model):
    """Globally justified C-finite recurrence for a supported EP formula."""
    ep=model.get('ep')
    if ep is None:return None
    expr=ep['expression'];roots={}
    for rate,poly in expr.items():
        if not isinstance(rate,(int,Fraction)) or Fraction(rate).denominator!=1:
            return None
        r=int(rate)
        if r==0:return None
        roots[r]=max(roots.get(r,0),len(poly))
    if not roots:return {'coefficients':(0,),'initial':(0,), 'proof':'identically zero EP expression'}
    coefficients=recurrence_from_roots(roots)
    if not coefficients or len(coefficients)>24:return None
    initial=[]
    for n in range(len(coefficients)):
        value=formal_eval(expr,n)
        if Fraction(value).denominator!=1:return None
        initial.append(int(value))
    return {'coefficients':tuple(coefficients),'initial':tuple(initial),
            'proof':'Product of (S-rate)^degree annihilates each exponential-polynomial component'}


def packet_nth(packet,n,memo=None):
    c=packet['coefficients'];iv=packet['initial']
    if n<len(iv):return iv[n]
    memo=memo if memo is not None else {}
    key=(c,n)
    if key not in memo:
        bank=memo.setdefault(('bank',c),SparsePacketBank(c))
        memo[key]=bank.packet(n)
    return sum(a*b for a,b in zip(memo[key],iv))


def direct_value(model,n,*,packet=None,packet_memo=None,method='formula'):
    if type(n) is not int or n<0:raise ValueError('nonnegative local index required')
    if method=='packet':
        if packet is None:raise ValueError('packet evaluator absent')
        return int(packet_nth(packet,n,packet_memo))
    if method!='formula':raise ValueError('unknown direct method')
    if model.get('ep') is not None:
        return integer_exact(formal_eval(model['ep']['expression'],n),model['oeis_id'],n)
    if model.get('gauge') is not None:
        from sequence_holonomic_compiler import fraction_eval
        return integer_exact(fraction_eval(model['gauge']['ast'],model['offset']+n),model['oeis_id'],n)
    raise ValueError('no exact source formula')


def default_direct_score(model,n):
    """Heuristic, NOT measured time or a bit-complexity bound."""
    ep=model.get('ep')
    terms=sum(len(p) for p in ep['expression'].values()) if ep else 6
    return max(1,terms)*(3+n.bit_length())


def prepare_sparse_tasks(models,certificates,requested,*,max_index=100000,
                         depth=3,max_tasks=24,max_actions=140,
                         direct_score=None,hyperedge_score=None,allow_packets=True,db=None):
    """Build finite backward dependency closure, including direct fallbacks."""
    if type(max_index) is not int or max_index<0:raise ValueError('invalid index cap')
    if type(depth) is not int or not 0<=depth<=8:raise ValueError('invalid depth')
    requests=tuple(sorted({checked_task(s,n,models,max_index) for s,n in requested}))
    if not requests:raise ValueError('empty request')
    by_target=defaultdict(list)
    # Only admit source-bound all-index certificates.
    for cert in certificates:
        certify_sparse_edge(cert,models,db=db)
        by_target[cert['target']].append(cert)
    direct_score=direct_score or (lambda sid,n:default_direct_score(models[sid],n))
    hyperedge_score=hyperedge_score or (lambda cert,n: 1+len(cert['rhs'])//12)
    tasks=set(requests);edges={};queue=deque((task,0) for task in requests)
    while queue:
        task,d=queue.popleft();sid,n=task
        if d>=depth:continue
        for cert in by_target[sid]:
            needs=needed_indices(cert,n)
            if any(k>max_index for _,k in needs):continue
            edges[(task,cert['formula_id'])]=(cert,needs)
            for pair in needs:
                if pair not in tasks:
                    tasks.add(pair)
                    if len(tasks)>max_tasks:
                        raise PlanningBudgetExceeded('sparse dependency task cap exceeded; no optimum claimed')
                    queue.append((pair,d+1))
    packets={sid:packet_from_ep(models[sid]) for sid,n in tasks}
    actions=[]
    for sid,n in sorted(tasks):
        dcost=direct_score(sid,n)
        if type(dcost) is not int or dcost<0:raise ValueError('bad direct score')
        actions.append(SparseAction((sid,n),(),dcost,'direct',method='formula'))
        if allow_packets and packets[sid] is not None and n>=2:
            pcost=max(1,n.bit_length()*max(1,len(packets[sid]['coefficients']))**2)
            actions.append(SparseAction((sid,n),(),pcost,'direct',method='packet'))
    for (task,_),(cert,needs) in edges.items():
        cost=hyperedge_score(cert,task[1]);
        if type(cost) is not int or cost<0:raise ValueError('bad transfer score')
        actions.append(SparseAction(task,needs,cost,'hyperedge',certificate=cert))
    if len(actions)>max_actions:raise PlanningBudgetExceeded('sparse action cap exceeded')
    actions.sort(key=lambda a:(a.target,a.cost,a.kind,a.method,a.inputs))
    return {'requests':requests,'tasks':tuple(sorted(tasks)),'actions':tuple(actions),
            'packets':packets,'source_fingerprints':{sid:formula_fingerprint(models[sid])
                for sid in {sid for sid,_ in tasks}},
            'limits':{'max_index':max_index,'depth':depth,'max_tasks':max_tasks,
                      'max_actions':max_actions}}


def shortest_sparse_plan(graph,*,cache=None,max_states=100000):
    """Exact minimum additive score within enumerated task/action graph.

    Dijkstra states store which individual (sequence,index) values are known.
    All legal transitions add one new value with already-known dependencies.
    """
    tasks=graph['tasks'];pos={k:i for i,k in enumerate(tasks)}
    if len(tasks)>45:raise PlanningBudgetExceeded('bitmask graph too large')
    cache=cache or {}
    start=sum(1<<pos[k] for k in cache if k in pos)
    goal=sum(1<<pos[k] for k in graph['requests'])
    encoded=[]
    for a in graph['actions']:
        mask=sum(1<<pos[k] for k in a.inputs)
        encoded.append((1<<pos[a.target],mask,a))
    frontier=[(0,0,start)];order=itertools.count(1);best={start:0};parent={};expanded=0
    while frontier:
        cost,_,state=heapq.heappop(frontier)
        if cost!=best[state]:continue
        if state&goal==goal:
            steps=[];last=state
            while last!=start:
                previous,a=parent[last];steps.append(a);last=previous
            steps.reverse()
            return {'cost':cost,'steps':steps,'states_expanded':expanded,
                    'states_reached':len(best),'starting_cached_tasks':len(cache),
                    'optimality':'exact_within_enumerated_sparse_action_graph'}
        expanded+=1
        if expanded>max_states:raise PlanningBudgetExceeded('sparse Dijkstra state budget exceeded')
        for bit,needed,a in encoded:
            if state&bit or state&needed!=needed:continue
            next_state=state|bit;candidate=cost+a.cost
            if next_state not in best or candidate<best[next_state]:
                best[next_state]=candidate;parent[next_state]=(state,a)
                heapq.heappush(frontier,(candidate,next(order),next_state))
    raise ValueError('no valid sparse plan')


def _cache_value(record,model,task):
    if not isinstance(record,dict) or type(record.get('value')) is not int:
        raise ValueError('malformed sparse cache')
    if record.get('source_sha256')!=model['source_sha256'] or \
       record.get('formula_fingerprint')!=formula_fingerprint(model):
        raise ValueError('stale sparse cache receipt')
    return record['value']


def integer_sha256(value):
    """Sign-stable binary digest, avoiding Python's decimal-digit conversion limit."""
    if type(value) is not int:raise ValueError('integer required')
    raw=abs(value).to_bytes(max(1,(abs(value).bit_length()+7)//8),'big')
    return hashlib.sha256((b'-' if value<0 else b'+')+raw).hexdigest()


def cache_record(task,value,model):
    checked_task(task[0],task[1],{task[0]:model},task[1])
    if type(value) is not int:raise ValueError('integer value required')
    return {'value':value,'source_sha256':model['source_sha256'],
            'formula_fingerprint':formula_fingerprint(model)}


def execute_sparse_plan(graph,plan,models,*,cache=None,verify_cache=True,
                        spot_check=True,db=None):
    """Execute formula-bound exact arithmetic; no imported source code executed."""
    cache=cache or {}
    values={};packet_memo={};proofs=set();receipts=[]
    for sid,fingerprint in graph['source_fingerprints'].items():
        if formula_fingerprint(models[sid])!=fingerprint:
            raise ValueError('source formula changed since sparse planning')
    for task,record in cache.items():
        if task not in graph['tasks']:continue
        value=_cache_value(record,models[task[0]],task)
        if verify_cache and value!=direct_value(models[task[0]],task[1]):
            raise ValueError('forged cache, even if cache checksum was replaced')
        values[task]=value
    for a in plan['steps']:
        sid,n=a.target
        if a.target in values:raise ValueError('duplicate sparse computation')
        if any(k not in values for k in a.inputs):raise ValueError('missing prerequisite indices')
        if a.kind=='direct':
            value=direct_value(models[sid],n,packet=graph['packets'][sid],
                               packet_memo=packet_memo,method=a.method)
        elif a.kind=='hyperedge':
            cert=a.certificate
            if (sid,n)!=a.target or tuple(a.inputs)!=needed_indices(cert,n):
                raise ValueError('altered sparse operator arguments')
            identity=cert['formula_id']
            if identity not in proofs:
                certify_sparse_edge(cert,models,db=db);proofs.add(identity)
            tree=safe_parse(cert['rhs'])
            def lookup(source,math_index):
                local=math_index-models[source]['offset']
                pair=(source,local)
                if pair not in values:raise ValueError('unexpected sparse dependency')
                return values[pair]
            value=integer_exact(eval_arithmetic(tree,models[sid]['offset']+n,lookup),sid,n)
        else:raise ValueError('invalid sparse action')
        if spot_check and value!=direct_value(models[sid],n):
            raise AssertionError('sparse plan conflicts with source formula')
        values[(sid,n)]=value
        receipts.append({'target':[sid,n],'kind':a.kind,'method':a.method,
                         'prerequisites':[[s,k] for s,k in a.inputs],
                         'value_sha256':integer_sha256(value)})
    return {task:values[task] for task in graph['requests']},receipts


def plan_and_run(models,certs,requests,*,cache=None,**limits):
    graph=prepare_sparse_tasks(models,certs,requests,**limits)
    validated_cache={k:v for k,v in (cache or {}).items() if k in graph['tasks']}
    plan=shortest_sparse_plan(graph,cache=validated_cache)
    result,receipts=execute_sparse_plan(graph,plan,models,cache=validated_cache)
    return {'outputs':result,'proof_receipts':receipts,'score':plan['cost'],
            'actions':tuple(a.view() for a in plan['steps']),
            'task_count':len(graph['tasks']),'computed_values':len(plan['steps']),
            'certificate_scope':'extracted formula identities, not all-index OEIS identification'}
