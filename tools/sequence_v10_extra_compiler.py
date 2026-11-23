"""Promote finitely checked chained expressions into exact formula certificates.

Author: Komorebi P. Generated source overlays are checked again against
retained OEIS terms, without mutating the historical v0.9 database.
"""
from __future__ import annotations
import argparse,json,sqlite3
from collections import Counter
from pathlib import Path
from sequence_holonomic_compiler import compile_formula,walk_ast
from sequence_holonomic_ogfs import construct
from sequence_oeis_chain_normalizer import verify


def compile_extra(db,overlay,out_recurrences,out_ogfs,summary=None):
    stats=Counter();rows=[];odes=[]
    for raw in Path(overlay).open(encoding='utf8'):
        if not raw.strip():continue
        x=json.loads(raw);stats['attempted']+=1
        fid,sid,ast=x['formula_id'],x['oeis_id'],x['evaluator']
        checked,state=verify(db,sid,ast)
        if state!='finite_checked' or checked!=x['checked_terms']:
            raise ValueError('stale or incorrect supplemental source formula '+fid)
        off,terms,sha=db.execute('SELECT offset,terms_json,source_sha256 FROM sequences WHERE oeis_id=?',(sid,)).fetchone()
        # High-degree polynomial differences are already within the older
        # C-finite polynomial compiler. Their expanded Ore minors can become
        # huge with no mathematical gain. Keep the source formula as a lead.
        if any(node.get('op')=='pow' and type(node.get('exp')) is int
               and node['exp']>=7 for node in walk_ast(ast)):
            stats['high_degree_delegated_to_cfinite']+=1
            continue
        cert=compile_formula(fid,sid,ast,off,[int(z) for z in json.loads(terms)],sha)
        if cert is None:stats['not_holonomic_in_supported_grammar']+=1;continue
        rows.append(cert);odes.append(construct(cert,ast));stats['certified']+=1
    for path,data in ((out_recurrences,rows),(out_ogfs,odes)):
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('w',encoding='utf8') as f:
            for x in data:f.write(json.dumps(x,separators=(',',':'))+'\n')
    report={'status':'additional_exact_formula_certificates','attempted':stats['attempted'],
        'certified':stats['certified'],'unsupported':stats['not_holonomic_in_supported_grammar'],
        'high_degree_delegated':stats['high_degree_delegated_to_cfinite'],
        'scope':'Theorem about supplied extracted expressions, not all-index OEIS identification'}
    if summary:Path(summary).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True);p.add_argument('--overlay',type=Path,required=True)
    p.add_argument('--recurrences',type=Path,required=True);p.add_argument('--ogfs',type=Path,required=True)
    p.add_argument('--summary',type=Path);a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:r=compile_extra(db,a.overlay,a.recurrences,a.ogfs,a.summary)
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
