"""Offline search atlas for certified sparse formula and archived Riordan transfers.
Author: Komorebi P. Source statuses remain visible; no unsupported promotion.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path


def render(sparse,archive,out):
    s=json.loads(Path(sparse).read_text(encoding='utf8'))
    a=json.loads(Path(archive).read_text(encoding='utf8'))
    rows=[]
    for item in s['samples']:
        rows.append({'type':'sparse','name':item['target'],
            'source':', '.join(item['inputs']),'target':item['target'],
            'parameters':', '.join(f'{sid}: '+','.join(f'{m}n+{r}' for m,r in maps)
                                   for sid,maps in item['index_maps'].items()),
            'proof':'exact extracted formula identity','terms':1,
            'description':f"Only {item['computed_term_count']} sparse computations at target-local index {item['requested_index']}; source-prefix maximum {item['full_source_prefix_horizon']}",
            'id':item['certified_formula_id']})
    for item in a['certificates']:
        rows.append({'type':'riordan','name':item['target_oeis_id'],
            'source':item['source_oeis_id'],'target':item['target_oeis_id'],
            'parameters':f"c={item['c']}, s={item['s']}, r={item['r']}, t={item['t']}",
            'proof':'exact rational OGF, conditional OEIS premise',
            'terms':item['finite_terms_replayed'],
            'description':item['archived_premise_status']+ ('; formal inverse available' if item['invertible_unramified'] else '; ramified, no general inverse'),
            'id':item['archived_certificate_key']})
    for item in a['quadratic_crosschecks']:
        rows.append({'type':'quadratic','name':item['B_id']+' + '+item['D_id'],
            'source':item['source_id'],'target':item['B_id']+' '+item['D_id'],
            'parameters':f"q={item['q']}, c={item['c']}",
            'proof':'exact quadratic-extension family; finite OEIS match',
            'terms':item['checked_indices'],
            'description':'Paired Pell-type channels; shared binary exponentiation and exact norm',
            'id':item['B_id']+'/'+item['D_id']})
    obj=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Komorebi OEIS Sparse Transfer Atlas v1.4</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark;--bg:#f6f7f9;--fg:#20252c;--surface:#fff;--muted:#5e6670;--line:#d5dae0;--link:#245b99}
@media(prefers-color-scheme:dark){:root{--bg:#141a22;--fg:#f2f4f7;--surface:#202936;--muted:#bcc8d5;--line:#4b5c6d;--link:#95c9ff}}
*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);margin:0;line-height:1.5}main{max-width:1180px;margin:auto;padding:26px 20px 48px}h1{font-size:clamp(1.45rem,4vw,2.2rem);margin:.35em 0}h2{font-size:1.15rem}p{max-width:80ch}a{color:var(--link)}.sub{color:var(--muted)}.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}.tile{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--surface)}.value{font-size:1.85rem;font-weight:650;font-variant-numeric:tabular-nums}.controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:20px 0}input,select{font:inherit;background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:9px;padding:10px}input{flex:1;min-width:190px}table{border-collapse:collapse;width:100%;background:var(--surface);font-size:.92rem}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:12px 9px}th{background:var(--bg);position:sticky;top:0}td:first-child{white-space:nowrap}table a{font-weight:600}.wrapper{border:1px solid var(--line);overflow:auto;border-radius:12px;max-height:680px}.meta{color:var(--muted);font-size:.86rem}.scope{border-left:3px solid var(--line);padding-left:14px}.foot{color:var(--muted);margin-top:24px}
</style></head><body><main>
<p class="sub">Komorebi P. · 22 November 2026 · exact formula research</p>
<h1>Sparse-index and Riordan transfer atlas</h1>
<p>Index-aware transfers from the 99,999-record OEIS snapshot, together with previously separate v0.8 operators recovered and independently replayed. All algebraic claims below concern the stated mathematical formulas.</p>
<div class="tiles">
 <div class="tile"><div class="value">110</div><div>Indexed hyperedges replayed</div><span class="meta">Formula-level all-index certificates</span></div>
 <div class="tile"><div class="value">41</div><div>Riordan OGF identities</div><span class="meta">Exact Q(x) certificates, source premise conditional</span></div>
 <div class="tile"><div class="value">2</div><div>Quadratic paired families</div><span class="meta">Pell channels with binary powering</span></div>
</div>
<section class="scope"><h2>Evidence boundary</h2><p><b>Exact formula identity</b> means algebraic equality of extracted formula definitions. <b>Conditional OGF</b> means the rational identity is exact once the listed source generating functions are accepted. Neither classification independently proves every infinite OEIS identification; exact stored terms supply additional finite checks. Optimization scores are workload-dependent, not claims of universally optimal runtime.</p></section>
<div class="controls"><input id="query" type="search" placeholder="Sequence ID, operator or parameter" aria-label="Search transfer records"><select id="kind" aria-label="Filter by proof family"><option value="all">All families</option><option value="sparse">Indexed formula hyperedges</option><option value="riordan">Riordan rational OGFs</option><option value="quadratic">Quadratic channels</option></select><strong id="count" aria-live="polite"></strong></div>
<div class="wrapper"><table><thead><tr><th>Target</th><th>Source</th><th>Operator</th><th>Proof scope / finite check</th></tr></thead><tbody id="records"></tbody></table></div>
<p class="foot">Data attribution: The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc. (CC BY-SA 4.0). The original v0.8 archive and its code were supplied by the research author. All original OEIS program snippets remain unexecuted.</p>
</main><script id="atlas-data" type="application/json">__DATA__</script>
<script>
'use strict';
const rows=JSON.parse(document.getElementById('atlas-data').textContent);
const q=document.getElementById('query'),kind=document.getElementById('kind'),body=document.getElementById('records'),count=document.getElementById('count');
function text(el,v){el.textContent=String(v??'');return el}
function cell(tr,v){const td=document.createElement('td');text(td,v);tr.appendChild(td);return td}
function link(td,v){const codes=String(v).match(/A\\d{6}/g)||[];if(codes.length){for(const code of codes){const a=document.createElement('a');a.href='https://oeis.org/'+code;a.textContent=code;a.rel='noopener noreferrer';td.appendChild(a);td.appendChild(document.createTextNode(' '));}}else{text(td,v)}}
function draw(){const needle=q.value.trim().toLowerCase(),filter=kind.value;let n=0;body.replaceChildren();
 for(const row of rows){if(filter!=='all'&&row.type!==filter)continue;
  if(needle&&!JSON.stringify(row).toLowerCase().includes(needle))continue;
  n++;const tr=document.createElement('tr');const a=cell(tr,'');link(a,row.name);const b=cell(tr,'');link(b,row.source);
  const op=cell(tr,row.parameters);const small=document.createElement('div');small.className='meta';small.textContent=row.description;op.appendChild(small);
  const status=cell(tr,row.proof+' ('+row.terms+' stored-term checks)');const id=document.createElement('div');id.className='meta';id.textContent=row.id;status.appendChild(id);body.appendChild(tr)
  if(n>=300)break;
 }
 count.textContent=n+' shown'+(n>=300?' (limit 300)':'')
}
q.addEventListener('input',draw);kind.addEventListener('change',draw);draw();
</script></body></html>'''.replace('__DATA__',obj)
    Path(out).write_text(page,encoding='utf-8')
    return {'rows':len(rows),'sparse':len(s['samples']),'riordan':len(a['certificates']),
            'quadratic':len(a['quadratic_crosschecks']),'bytes':len(page.encode())}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sparse',required=True,type=Path);p.add_argument('--archive',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    print(json.dumps(render(a.sparse,a.archive,a.output)))
if __name__=='__main__':main()
