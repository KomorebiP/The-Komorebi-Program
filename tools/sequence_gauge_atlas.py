"""Cycle-consistent, exact multiplicative transfer atlas for OEIS formulas.

Author: Komorebi P.

A gauge e:u->v is f_v(n)=K_e*c_e**n*L_e(n)/L_e(0)*f_u(n).
An independent cycle carries holonomy H(n) equal to the product of all
oriented gauges. Every closed loop must satisfy H(0)=1 and H(n+1)/H(n)=1
as an identity in Q(n). Checking all fundamental cycles of a spanning forest
certifies the entire graph's path independence, conditional on the admitted
formula definitions. No global identification of source OEIS sequences follows.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json, sqlite3

from sequence_holonomic_compiler import Rat, fraction_eval
from sequence_v10_path_compiler import oriented_edge,composite_factors,gauge_rat
from sequence_workload_planner import verified_gauges,load_project


def normalize_cycle(oriented_edges):
    c=F(1);k=F(1)
    for e in oriented_edges:
        c*=F(e['exponential_factor'])
        k*=F(e['base_ratio'])
    factors=composite_factors(oriented_edges)
    L=gauge_rat(factors)
    # Formal rational functions in Q(n), not a finite-value sample.
    ratio=Rat((c,))*L.shift(1)/L
    return dict(base_value=str(k),step_ratio_is_one=(ratio==Rat((1,))),
        initial_value_is_one=(k==1),flat=(ratio==Rat((1,)) and k==1),
        multiplier=str(c),factors=factors)


def _orient(edge,u,v):
    if edge['source']==u and edge['target']==v:return oriented_edge(edge)
    if edge['target']==u and edge['source']==v:return oriented_edge(edge,True)
    raise ValueError('edge does not connect requested vertices')


def _tree_route(graph,source,target):
    queue=deque([source]);seen={source:None}
    while queue:
        u=queue.popleft()
        if u==target:break
        for v,i in sorted(graph[u],key=lambda x:(x[0],x[1])):
            if v in seen:continue
            seen[v]=(u,i);queue.append(v)
    if target not in seen:raise ValueError('no forest path')
    route=[];v=target
    while v!=source:
        u,i=seen[v];route.append((u,v,i));v=u
    return list(reversed(route))


def make_gauge_atlas(models,ledger,*,strict=True):
    edges,proof_stats=verified_gauges(models,ledger,strict=strict)
    undirected=defaultdict(list)
    for i,e in enumerate(edges):
        undirected[e['source']].append((e['target'],i))
        undirected[e['target']].append((e['source'],i))
    visited=set();components=[];forest=defaultdict(list);forest_indices=set()
    for start in sorted(undirected):
        if start in visited:continue
        comp=set();visited.add(start);queue=deque([start])
        while queue:
            u=queue.popleft();comp.add(u)
            for v,i in sorted(undirected[u]):
                if v in visited:continue
                visited.add(v);queue.append(v)
                forest_indices.add(i)
                forest[u].append((v,i));forest[v].append((u,i))
        components.append(sorted(comp))
    charts=[]
    for comp in components:
        root=comp[0]
        for node in comp:
            if node==root:continue
            route=_tree_route(forest,root,node)
            factors=[_orient(edges[i],u,v) for u,v,i in route]
            summary=normalize_cycle(factors)
            # For a path, H is not generally 1; its base value, c and L
            # constitute the exact canonical multiplicative chart.
            for n in (0,1,3):
                p=F(summary['base_value'])*F(summary['multiplier'])**n
                L=gauge_rat(summary['factors']);p*=L.at(n)/L.at(0)
                expected=fraction_eval(models[root]['ast'],models[root]['offset']+n)*p
                actual=fraction_eval(models[node]['ast'],models[node]['offset']+n)
                if expected!=actual:raise AssertionError('forest chart disagrees with current formula evaluations')
            charts.append(dict(root=root,node=node,steps=len(route),
                source_sha256=models[root]['source_sha256'],
                node_sha256=models[node]['source_sha256'],
                base_ratio=summary['base_value'],
                exponential_factor=summary['multiplier'],
                gauge_linear_factors=summary['factors'],
                scope='Exact formula-expression gauge for all local n>=0; OEIS identification finite-checked'))
    cycles=[];bad=[]
    for i,e in enumerate(edges):
        if i in forest_indices:continue
        u=e['source'];v=e['target']
        # u->v on this extra edge, then v->u along the forest.
        route=[oriented_edge(e)]
        path=_tree_route(forest,v,u)
        route.extend(_orient(edges[j],a,b) for a,b,j in path)
        summary=normalize_cycle(route)
        rec=dict(edge_index=i,edge=[u,v],length=len(route),
                 flat=summary['flat'],base_value=summary['base_value'],
                 step_ratio_is_one=summary['step_ratio_is_one'])
        cycles.append(rec)
        if not summary['flat'] and len(bad)<12:bad.append(rec)
    expected_cycle_rank=len(edges)-len(undirected)+len(components)
    if expected_cycle_rank!=len(cycles):raise AssertionError('spanning-forest cycle rank discrepancy')
    if bad:raise AssertionError('nontrivial gauge cycle detected: '+json.dumps(bad))
    counts=dict(source_models=len(models),source_edges=proof_stats['read'],
        accepted_full_prefix_gauges=len(edges),component_count=len(components),
        connected_formula_models=len(undirected),largest_component=max(map(len,components),default=0),
        spanning_forest_edges=len(forest_indices),fundamental_cycles=len(cycles),
        flat_cycles=sum(v['flat'] for v in cycles),nontrivial_holonomy=len(bad),
        chart_count=len(charts),
        source_proof_gates=proof_stats,
        scope='Exact identities of admitted formulas, not independently proved OEIS identities',
        theorem='Flatness on a fundamental-cycle basis implies path-independent gauge transport on all graph paths')
    return dict(summary=counts,components=components,charts=charts,cycles=cycles)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--extra',type=Path,required=True)
    p.add_argument('--gauges',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    models,_=load_project(a.db,a.extra)
    atlas=make_gauge_atlas(models,a.gauges)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(atlas,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(atlas['summary'],indent=2))

if __name__=='__main__':main()
