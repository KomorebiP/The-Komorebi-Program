"""Offline searchable atlas of source-certified indexed transfer workloads.
Author: Komorebi P.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path


def render(receipt):
    records=receipt['indexed_edge_detail']
    if len(records)!=receipt['indexed_formula_hyperedges']:
        raise ValueError('indexed atlas source and reported count differ')
    count=sum(r['cost_model_choice']=='indexed_transfer' for r in records)
    if count!=receipt['query_plans_with_selected_indexed_edge']:
        raise ValueError('indexed candidate selection counts differ')
    payload=json.dumps(records,ensure_ascii=False,separators=(',',':'))
    # JSON data is untrusted OEIS-derived text; do not allow script/HTML escape.
    payload=payload.replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Komorebi | Variable-horizon transfer atlas v1.3</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,sans-serif;--blue:#2264c0}
*{box-sizing:border-box}body{margin:0;background:Canvas;color:CanvasText;line-height:1.55}
header,main{width:min(1050px,calc(100% - 32px));margin:auto}header{padding:32px 0 16px}
h1{font-size:clamp(1.65rem,4vw,2.5rem);line-height:1.15;margin:8px 0}
h2{font-size:1.18rem}small,.muted{color:GrayText}a{color:var(--blue)}
.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:18px 0}
.metric{padding:16px;border:1px solid color-mix(in srgb,CanvasText 22%,Canvas);border-radius:12px}
.metric strong{font-size:1.7rem;display:block;font-variant-numeric:tabular-nums}
.controls{display:flex;flex-wrap:wrap;gap:9px;padding:14px 0;position:sticky;top:0;background:Canvas;z-index:2}
input,select{min-height:42px;border:1px solid GrayText;background:Canvas;color:CanvasText;border-radius:8px;padding:8px;font:inherit}
input{flex:1;min-width:210px}select{min-width:160px}
article{border:1px solid color-mix(in srgb,CanvasText 23%,Canvas);border-radius:11px;margin:10px 0;padding:12px 14px}
article.selected{border-left:5px solid var(--blue)}article .lead{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
article h2{margin:0;font-size:1.03rem}.pill{font-size:.77rem;border:1px solid GrayText;padding:2px 9px;border-radius:20px}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:color-mix(in srgb,CanvasText 7%,Canvas);border-radius:8px;padding:11px}
code{overflow-wrap:anywhere}details{margin-top:6px}summary{cursor:pointer;font-weight:500}
footer{margin:30px 0 55px;border-top:1px solid GrayText;padding:14px 0;font-size:.9rem}
@media(max-width:520px){.metrics{grid-template-columns:1fr}.metric{padding:8px}.controls{position:static}}
</style></head><body><header><small>Komorebi P. · Exact formula-transfer research</small>
<h1>Variable-horizon transfer atlas</h1>
<p>Exact indexed formulas and backwards prefix requirements for a 21-term OEIS workload.
Every algebraic identity refers to extracted source formulas. OEIS-wide all-index identities are <strong>not</strong> established by finite source matching.</p>
<div class="metrics"><div class="metric"><strong>''' + str(len(records)) + '''</strong><small>Indexed formulas audited</small></div>
<div class="metric"><strong>''' + str(count) + '''</strong><small>Transfer routes selected</small></div>
<div class="metric"><strong>''' + str(receipt['query_plan_values_checked']) + '''</strong><small>Exact output values verified</small></div></div></header>
<main><label for="search">Find a transfer by OEIS ID, expression, or input</label>
<div class="controls"><input id="search" type="search" placeholder="Search sequences or formulas" aria-label="Search indexed transfers">
<select id="selection" aria-label="Filter optimizer decision"><option value="all">All decisions</option>
<option value="indexed_transfer">Transfer selected</option><option value="direct">Direct selected</option></select>
<select id="sourcecount" aria-label="Filter number of source sequences"><option value="all">All source counts</option>
<option value="single">One input</option><option value="multi">Multiple inputs</option></select></div>
<p id="count" aria-live="polite"></p><div id="results"></div>
<footer>Data: official OEIS snapshot (CC BY-SA 4.0). Formula and provenance verification performed by Komorebi's restricted exact compiler. Heuristic score ratios are not measured runtime improvements. No source formula or program is executed from this web page.</footer>
</main><script type="application/json" id="records">''' + payload + '''</script>
<script>"use strict";
const rows=JSON.parse(document.querySelector('#records').textContent);
const search=document.querySelector('#search'),selection=document.querySelector('#selection'),sourcecount=document.querySelector('#sourcecount');
const count=document.querySelector('#count'),results=document.querySelector('#results');
function el(tag,txt,klass){const node=document.createElement(tag);if(txt!==null)node.textContent=txt;if(klass)node.className=klass;return node;}
function render(){results.replaceChildren();const q=search.value.trim().toLowerCase();let shown=0;
for(const row of rows){if(selection.value!=='all'&&row.cost_model_choice!==selection.value)continue;
if(sourcecount.value==='single'&&row.inputs.length!==1)continue;
if(sourcecount.value==='multi'&&row.inputs.length<2)continue;
const hay=[row.target,row.rhs,...row.inputs].join(' ').toLowerCase();if(q&&!hay.includes(q))continue;
const card=el('article',null,row.cost_model_choice==='indexed_transfer'?'selected':'');
const head=el('div',null,'lead'),h=el('h2',null);
const anchor=el('a',row.target);anchor.href='https://oeis.org/'+encodeURIComponent(row.target);anchor.target='_blank';anchor.rel='noopener noreferrer';
h.append(anchor);head.append(h);head.append(el('span',row.cost_model_choice==='indexed_transfer'?'Transfer selected':'Direct selected','pill'));card.append(head);
card.append(el('p',row.rhs));const more=el('details',null),sum=el('summary','Exact input horizons and provenance');more.append(sum);
more.append(el('pre',JSON.stringify({index_maps:row.index_maps,required_local_horizon:row.required_input_horizons,
score:row.score,independent_score:row.independent_direct_score,source_text_sha256:row.source_text_sha256},null,2)));
card.append(more);results.append(card);shown++;}count.textContent=shown+' of '+rows.length+' indexed formula records displayed.';}
for(const node of [search,selection,sourcecount])node.addEventListener(node===search?'input':'change',render);
render();</script></body></html>'''


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    receipt=json.loads(a.audit.read_text(encoding='utf-8'))
    content=render(receipt)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(content,encoding='utf-8')
    print(json.dumps({'html_bytes':len(content.encode()),'indexed_records':receipt['indexed_formula_hyperedges']}))

if __name__=='__main__':main()
