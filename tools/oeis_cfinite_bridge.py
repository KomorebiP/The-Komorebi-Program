#!/usr/bin/env python3
"""All-index certificates between explicit bounded-order C-finite sequence definitions.

Author: Komorebi P.

A seed is an explicitly asserted recurrence plus initial values for a named
sequence. The identity between the abstract recurrences is proved for all
n>=0. Independent verification of the OEIS-to-seed identification is separate.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path
import re

ID = re.compile(r"A\d{6}\Z")


def terms(a: int, b: int, initial: list[int], count: int = 10) -> list[int]:
    vals = list(initial)
    for _ in range(2, count):
        vals.append(a*vals[-1]+b*vals[-2])
    return vals[:count]


def sequence_terms(coefficients: list[int], initials: list[int], count: int) -> list[int]:
    """Compute any constant-coefficient integral recurrence exactly."""
    d=len(coefficients)
    if not 1<=d<=8 or len(initials)!=d:
        raise ValueError('Recurrence order or initial data unsupported')
    vals=list(initials)
    for n in range(d,count):
        vals.append(sum(coefficients[j-1]*vals[n-j] for j in range(1,d+1)))
    return vals[:count]


def exact_linear_solve(matrix: list[list[Q]], rhs: list[Q]) -> tuple[list[Q], int] | None:
    """Solve Hc=t over Q, including compatible singular shift orbits.

    Free coefficients are canonically set to zero. Return None only if the
    target initial vector is outside the span of the source shifts.
    """
    d=len(matrix)
    if not d or len(rhs)!=d or any(len(row)!=d for row in matrix):
        raise ValueError('Non-square recurrence interface')
    rows=[[Q(x) for x in row]+[Q(rhs[i])] for i,row in enumerate(matrix)]
    pivots=[]
    for j in range(d):
        pivot=next((i for i in range(len(pivots),d) if rows[i][j]),None)
        if pivot is None:
            continue
        k=len(pivots)
        rows[k],rows[pivot]=rows[pivot],rows[k]
        factor=rows[k][j]
        rows[k]=[x/factor for x in rows[k]]
        for i in range(d):
            if i==k or rows[i][j]==0:continue
            mul=rows[i][j]
            rows[i]=[x-mul*y for x,y in zip(rows[i],rows[k])]
        pivots.append(j)
    rank=len(pivots)
    if any(rows[i][-1]!=0 for i in range(rank,d)):
        return None
    solution=[Q(0)]*d
    for i,j in enumerate(pivots):
        solution[j]=rows[i][-1]
    return solution,rank


def recurrence_transfer(source: dict, target: dict) -> dict | None:
    """Prove T(n) = sum_j c_j S(n+j) by d initial values and recurrence induction."""
    if source['recurrence'] != target['recurrence']:
        return None
    coeff=source['recurrence']; d=len(coeff)
    if len(source['initial'])!=d or len(target['initial'])!=d:
        raise ValueError('Mismatched recurrence data')
    values=sequence_terms(coeff,source['initial'],2*d-1)
    matrix=[[Q(values[i+j]) for j in range(d)] for i in range(d)]
    solved=exact_linear_solve(matrix,[Q(x) for x in target['initial']])
    if solved is None:
        return None
    solution,rank=solved
    assert all(sum(matrix[i][j]*solution[j] for j in range(d))==target['initial'][i] for i in range(d))
    out={"source":source['id'],"target":target['id'],
         "shift_coefficients":[str(x) for x in solution],
         "statement":"target(n) = sum_j c[j]*source(n+j), n >= 0",
         "recurrence":{"coefficients":coeff,"order":d},
         "source_initial":source['initial'],"target_initial":target['initial'],
         "proof_method":f"Exact {d}x{d} rational shift-orbit solve and order-{d} recurrence induction",
         "source_shift_rank":rank,"coefficients_unique":rank==d,
         "domain":"all integers n >= 0, conditional on both asserted sequence definitions",
         "source_definition_status":"requires independently checked OEIS identification",
         "formal_abstract_identity":"proved","source_seed":source['source'],"target_seed":target['source']}
    if d==2:
        out['alpha']=str(solution[0]);out['beta']=str(solution[1])
    return out


def build(registry: dict, network_ids: set[str], component: dict[str,int]) -> dict:
    if registry.get('schema')!=1:
        raise ValueError('Unsupported recurrence seed registry schema')
    seeds=registry.get('sequences')
    if not isinstance(seeds,list):
        raise ValueError('Missing recurrence seeds')
    by_rec=defaultdict(list);ids=set()
    for seq in seeds:
        i=seq['id']
        if not ID.fullmatch(i) or i in ids:raise ValueError('Duplicate or malformed recurrence seed ID')
        ids.add(i)
        if seq.get('offset')!=0 or seq.get('evidence')!='asserted_oeis_definition':
            raise ValueError('Only offset-zero, explicitly asserted recurrence seeds are supported')
        coeffs=seq.get('recurrence'); initial=seq.get('initial')
        if (not isinstance(coeffs,list) or not 1<=len(coeffs)<=8 or not all(type(x) is int and abs(x)<10**6 for x in coeffs)
            or not isinstance(initial,list) or len(initial)!=len(coeffs) or not all(type(x) is int for x in initial)):
            raise ValueError('Malformed exact recurrence/initial conditions')
        if seq.get('source')!=f'https://oeis.org/{i}':
            raise ValueError('OEIS seed provenance missing')
        by_rec[tuple(coeffs)].append(seq)
    cert=[];rank_def=[]
    for rec,group in sorted(by_rec.items()):
        for s in group:
            for t in group:
                if s['id']==t['id']:continue
                result=recurrence_transfer(s,t)
                if result is None:
                    rank_def.append([s['id'],t['id']]);continue
                result['network_relation']=(
                    'cross_component' if s['id'] in component and t['id'] in component and component[s['id']]!=component[t['id']]
                    else 'same_component' if s['id'] in component and t['id'] in component
                    else 'outside_curated_network')
                cert.append(result)
    return {"schema":1,"author":"Komorebi P.","seed_count":len(seeds),"certificate_count":len(cert),
            "cross_component_certificate_count":sum(x['network_relation']=='cross_component' for x in cert),
            "rank_deficient_pairs_unresolved":rank_def,"certificates":cert,
            "claim_boundary":"Full recurrence identities are proved; their application to OEIS IDs requires independent verification of the asserted seed recurrence and initial data."}


def write_certificates(registry_path: Path, network_ids: set[str], component: dict[str,int], output: Path) -> dict:
    from oeis_gap_automation import write_json
    results=build(json.loads(registry_path.read_text(encoding='utf-8')),network_ids,component)
    write_json(output,results)
    return {k:v for k,v in results.items() if k not in ('certificates','rank_deficient_pairs_unresolved')}
