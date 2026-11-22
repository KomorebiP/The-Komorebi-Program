"""Compress proven recurrence-polyphase formulas into denominator-sharing modules.

Author: Komorebi P.

Only formulas proven for the supplied recurrence definition are admitted.
This builds one rational OGF and one recurrence per phase, then groups common
reduced OGF denominators. Edges are quotient identities in Q((z)) and are
explicitly scoped to the supplied exact recurrence definitions.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sqlite3

from sequence_recurrence_transfers import (ogf_from_recurrence,
                                            rational_ogf_filter,pdivmod,gcdpoly,trim)
from sequence_recurrence_packets import load_sources


def reduced_rational(initial,coeff):
    if not coeff:
        return {'P':[Q(0)],'Q':[Q(1)]}
    result=ogf_from_recurrence({'op':'linear_recurrence','coefficients':coeff,'initial':initial})
    if result is None:raise ValueError('invalid derived recurrence')
    p,q=result['P'],result['Q']
    if p==[0]:return {'P':[Q(0)],'Q':[Q(1)]}
    d=gcdpoly(p,q)
    p,rem1=pdivmod(p,d);q,rem2=pdivmod(q,d)
    if rem1!=[0] or rem2!=[0]:raise ArithmeticError('failed rational OGF reduction')
    scale=q[0]
    return {'P':trim([v/scale for v in p]),'Q':trim([v/scale for v in q])}


def poly_to_text(poly):return [str(x) for x in poly]


def filter_cost(filter_record):
    if not filter_record:return 10**10
    n=[Q(v) for v in filter_record['numerator']]
    d=[Q(v) for v in filter_record['denominator']]
    return 3*(len(n)-1)+4*(len(d)-1)+sum(v!=0 for v in n+d)+abs(filter_record['shift'])


def build(db,formula_path,graph_path,max_cost=15):
    # All data is self-contained in the derived packet tables; no new OEIS
    # identity is inferred from coincident finite terms.
    ids=[sid for (sid,) in db.execute('SELECT oeis_id FROM recurrence_packet_sources ORDER BY oeis_id')]
    if ids:load_sources(db,ids)  # refuse any stale source / evaluator hash
    rows=db.execute('''SELECT oeis_id,modulus,residue,characteristic_json,
        general_recurrence_json,minimal_recurrence_json,minimal_initial_json,
        minimal_order,observed_terms,proof_scope
        FROM recurrence_packet_phases ORDER BY oeis_id,modulus,residue''').fetchall()
    groups=defaultdict(list)
    formulas=[]
    for sid,m,r,ch,gen,cr,iv,k,observed,scope in rows:
        initial=json.loads(iv);coeff=json.loads(cr)
        if k!=len(initial) or k!=len(coeff):raise ValueError('derived recurrence has wrong order')
        gf=reduced_rational(initial,coeff)
        record={'source':sid,'modulus':m,'residue':r,
                'recurrence':{'initial':initial,'coefficients':coeff,'order':k},
                'ogf':{'numerator':poly_to_text(gf['P']),'denominator':poly_to_text(gf['Q'])},
                'finite_oeis_overlap':observed,'proof_scope':scope,
                'identity':'B(z) = sum_(n>=0) a_(m*n+r) z^n, with a indexed from its OEIS mathematical offset'}
        formulas.append(record)
        key=tuple(record['ogf']['denominator'])
        groups[key].append((record,gf))
    targets=[];module_summaries=[];reduced_groups=0
    for denom,items in sorted(groups.items(), key=lambda x:(len(x[0]),x[0])):
        nonzero=[(record,gf) for record,gf in items if gf['P']!=[0]]
        if len(items)>1:reduced_groups+=1
        # The most sparse small-degree OGF numerator is the module's preferred hub.
        def weight(item):
            p=item[1]['P']
            return (len(p)-1,sum(v!=0 for v in p),item[0]['modulus'],item[0]['residue'],item[0]['source'])
        hub=min(nonzero,key=weight) if nonzero else None
        module_summaries.append({'denominator':list(denom),'phases':len(items),
              'source_sequences':len({row['source'] for row,_ in items}),
              'hub':({k:hub[0][k] for k in ('source','modulus','residue')} if hub else None)})
        if hub is None:continue
        for target in nonzero:
            if target is hub:continue
            filter_=rational_ogf_filter(hub[1],target[1])
            cost=filter_cost(filter_)
            if cost>max_cost:continue
            targets.append({'source':{key:hub[0][key] for key in ('source','modulus','residue')},
              'target':{key:target[0][key] for key in ('source','modulus','residue')},
              'filter':filter_,'structural_cost':cost,
              'scope':'exact Laurent-rational identity of curated recurrence-defined polyphases'})
    formula_path=Path(formula_path);graph_path=Path(graph_path)
    formula_path.parent.mkdir(parents=True,exist_ok=True)
    graph_path.parent.mkdir(parents=True,exist_ok=True)
    formula_path.write_text(''.join(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n' for x in formulas),encoding='utf-8')
    summary={'phase_formulas':len(formulas),'denominator_modules':len(groups),
             'nontrivial_shared_denominators':reduced_groups,
             'small_exact_quotient_links':len(targets),'max_filter_cost':max_cost,
             'modules':module_summaries,'links':targets,
             'non_claims':['The source OEIS identity is only finite-checked',
                            'OGF ratios are exact for the curated recurrence definitions',
                            'An OGF quotient need not be a faster evaluator']}
    graph_path.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return {k:summary[k] for k in ['phase_formulas','denominator_modules','nontrivial_shared_denominators','small_exact_quotient_links']}


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--formulas',type=Path,required=True)
    p.add_argument('--index',type=Path,required=True)
    p.add_argument('--max-cost',type=int,default=15)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        report=build(db,args.formulas,args.index,max_cost=args.max_cost)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
