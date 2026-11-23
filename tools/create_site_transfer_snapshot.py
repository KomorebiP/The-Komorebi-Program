"""Offline one-shot release tool: project audited OEIS transfer ledgers into a read-only site index.

This is NOT called by the website build. It needs the retained v1.4 ledger files and
read-only, pinned OEIS SQLite snapshot. Run it separately during a reviewed refresh.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sqlite3

OEIS_RE = re.compile(r'^A[0-9]{6}$')
DB_SHA256 = 'a121d7a6a5b6aa78a5a333fe748b604f170511bf8250ca16533f58cbcfa9e9f5'

def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as fd:
        for buf in iter(lambda: fd.read(1 << 20), b''):
            digest.update(buf)
    return digest.hexdigest()

def rows(path):
    with open(path, encoding='utf-8') as fd:
        for line in fd:
            if line.strip():
                yield json.loads(line)

def construct(db_path, hyperedges, gauges, riordan_replay, output):
    assert sha256(db_path) == DB_SHA256, 'Pinned OEIS SQLite snapshot hash differs'
    paths = {'hyperedges':Path(hyperedges),'gauges':Path(gauges),'riordan':Path(riordan_replay)}
    edges = []
    for obj in rows(paths['hyperedges']):
        if obj.get('status') != 'all_index_extracted_formula_identity':
            raise ValueError('Unexpected hyperedge verification scope')
        edges.append(dict(key='h:'+obj['formula_id'][:20],kind='hyperedge',target=obj['target'],inputs=obj['inputs'],
                          expression=obj['rhs'],index_maps=obj['index_maps'],domain='all local n>=0',
                          evidence='all_index_formula_identity',proof_ref=obj['formula_id'],
                          source_receipt=obj['source_text_sha256']))
    for obj in rows(paths['gauges']):
        source,target=obj['source'],obj['target']
        if obj['proof_method'].startswith('Exact shift-orbit') is False:raise ValueError('Unreviewed gauge')
        components = obj.get('gauge_linear_factors',[])
        if len(components)>8:continue
        terms = ['(%s*n%+d)^%s'%(int(c['a']),int(c['b']),int(c['power'])) for c in components]
        statement = 'b(n) / a(n): base=%s, exponential=%s, factors=%s'%(
            obj['base_ratio'],obj['exponential_factor'],','.join(terms) or '1')
        edges.append(dict(key='g:'+hashlib.sha256((obj['source_formula']+'|'+obj['target_formula']).encode()).hexdigest()[:20],
                          kind='gauge',target=target,inputs=[source],expression=statement,
                          index_maps={source:[[1,0]]},domain='local n>='+str(obj['tail_start_local'])+
                           ' with nonsingular ratio denominator',valid_from=int(obj['tail_start_local']),
                          evidence='all_index_formula_identity_on_tail',proof_ref=obj['target_formula'],
                          source_receipt=obj['source_sha256']))
    replay=json.loads(paths['riordan'].read_text())
    for obj in replay['certificates']:
        if not obj.get('exact_rational_identity'):
            raise ValueError('Conditional Riordan proof missing')
        source,target=obj['source_oeis_id'],obj['target_oeis_id']
        edges.append(dict(key='r:'+obj['archived_certificate_key'][:20],kind='riordan',target=target,inputs=[source],
                          expression='R[c=%s,s=%s,r=%s,t=%s] OGF transform'%(obj['c'],obj['s'],obj['r'],obj['t']),
                          index_maps={},domain='formal generating series under source and target OGF premises',
                          evidence='conditional_exact_ogf_identity',proof_ref=obj['archived_certificate_key'],
                          source_receipt=obj['source_formula_sha256_current']))
    # Two established quadratic exponential channels, with two outputs per family.
    for c,q,targets in ((1,2,['A001333','A000129']),(2,3,['A001075','A001353'])):
        for target in targets:
            edges.append(dict(key=f'q:{c}:{q}:{target}',kind='quadratic',target=target,inputs=[x for x in targets if x!=target],
                              expression=f'(c+sqrt(q))^n=B_n+sqrt(q)*D_n; c={c}, q={q}',
                              index_maps={},domain='all integer n>=0 for quadratic channel definition',
                              evidence='exact_quadratic_algebra',proof_ref=f'quadratic-channel:{c}:{q}',
                              source_receipt=DB_SHA256))
    keys = [x['key'] for x in edges]
    if len(keys) != len(set(keys)):raise ValueError('Colliding edge keys')
    ids={x['target'] for x in edges}
    for x in edges:ids.update(x['inputs'])
    if not all(OEIS_RE.fullmatch(x) for x in ids):raise ValueError('Malformed OEIS ID')
    with sqlite3.connect(f'file:{db_path}?mode=ro',uri=True) as db:
        records=[]
        for item in sorted(ids):
            row=db.execute('SELECT name,offset FROM sequences WHERE oeis_id=?',(item,)).fetchone()
            if row:records.append({'id':item,'name':row[0],'offset':row[1]})
            else:records.append({'id':item,'name':'OEIS reference (outside retained source sample)','offset':None})
    out=dict(schema=1,collection='Komorebi Sequence Library · Transfer Network',author='Komorebi P.',
            oeis=dict(name='The Online Encyclopedia of Integer Sequences',license='CC-BY-SA-4.0',
                      reference='https://oeis.org/',snapshot_sha256=DB_SHA256,
                      coverage='First 99,999 imported OEIS source entries; not a full OEIS formula export'),
            evidence_note='All-index algebraic statements concern extracted formula definitions or conditional generating functions. Infinite OEIS record identities have not been independently established.',
            counts=dict(Counter(x['kind'] for x in edges)),
            sources={name:dict(sha256=sha256(path),basename=path.name) for name,path in paths.items()},
            records=records,edges=edges)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    return dict(edges=len(edges),nodes=len(records),counts=out['counts'],sha256=sha256(output),bytes=output.stat().st_size)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for item in ('db','hyperedges','gauges','riordan','output'):ap.add_argument('--'+item,required=True,type=Path)
    a=ap.parse_args();print(json.dumps(construct(a.db,a.hyperedges,a.gauges,a.riordan,a.output),indent=2))
if __name__=='__main__':main()
