"""Render a self-contained, provenance-aware Komorebi transfer atlas.

Author: Komorebi P.

Uses only the already generated graph and candidate tables. No network runtime,
no arbitrary expression execution, and no visual implication that a candidate
is proven. HTML/JS are bundled in one portable file.
"""
from __future__ import annotations

import argparse
from collections import Counter
from html import escape
import json
from pathlib import Path
import sqlite3


def render(db, target):
    nodes=[{'id':r[0],'type':r[1],'name':r[2]} for r in db.execute(
        'SELECT node_id,type,label FROM transfer_nodes ORDER BY node_id')]
    edges=[{'id':r[0],'source':r[1],'target':r[2],
            'operator':r[3],'status':r[4], 'statement':r[5],
            'evidence':r[6], 'checked':r[7], 'source_url':r[9]}
           for r in db.execute('SELECT * FROM transfer_edges ORDER BY source_node,target_node')]
    ratios={r[0]:{'start':r[1],'mathematical_start':r[2], 'base':r[3],
                  'numerator':json.loads(r[4]),'denominator':json.loads(r[5]),
                  'pochhammer':json.loads(r[6]) if r[6] else None,
                  'fit':r[7],'holdout':r[8],'checked':r[9]}
            for r in db.execute('SELECT * FROM rational_ratio_candidates')}
    dataset=json.dumps({'nodes':nodes,'edges':edges,'ratios':ratios},
                       ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    total=Counter(x['status'] for x in edges)
    summary=f'{len(nodes)} nodes · {len(edges)} visible edges · {total.get("algebraic_identity",0)} proved'
    html_template=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Komorebi — Sequence Transfer Atlas</title><style>
:root{color-scheme:light;--ink:#182639;--muted:#536478;--line:#cbd3dc;--bg:#f6f8fb;--surface:white;--accent:#264d79;--proof:#146657;--candidate:#996110;--reference:#536477}
*{box-sizing:border-box}body{font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;color:var(--ink);background:var(--bg)}
header{background:var(--surface);border-bottom:1px solid var(--line);padding:22px max(20px,calc((100% - 1320px)/2))}
h1{font-size:clamp(1.4rem,3vw,2rem);letter-spacing:-.03em;margin:0 0 3px}h2{font-size:1.15rem;margin:0 0 10px}p{margin:4px 0 10px}small,.muted{color:var(--muted)}a{color:var(--accent)}
main{max-width:1320px;margin:auto;padding:18px 20px 45px} .toolbar,.cols{display:grid;gap:16px}.toolbar{grid-template-columns:2fr 1fr 1fr;align-items:end;margin-bottom:16px}.cols{grid-template-columns:minmax(0,1.65fr) minmax(320px,1fr)}
label{display:block;font-weight:600;font-size:.84rem;margin-bottom:5px}input,select,button{font:inherit;padding:10px;border:1px solid var(--line);border-radius:7px;background:white;color:inherit;max-width:100%}input,select{width:100%}button{cursor:pointer;font-weight:600;background:var(--accent);color:white;border-color:var(--accent)}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #82a6d2;outline-offset:1px}
.panel{border:1px solid var(--line);background:var(--surface);border-radius:12px;padding:16px;min-width:0}.controls{display:flex;flex-wrap:wrap;gap:14px;margin:0 0 12px}.controls label{font-weight:500;margin:0}.controls input{width:auto;margin-right:6px;vertical-align:middle}
#plot{border:1px solid #e5eaf0;background:#fbfcfe;border-radius:8px;min-height:520px;width:100%}svg{display:block;width:100%;height:auto;min-height:520px}svg text{font:12px system-ui;fill:var(--ink)}svg .node{cursor:pointer}svg .node:focus{outline:none}svg .node:focus rect{stroke:#17253a;stroke-width:3}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:.83rem;margin:10px 0}.legend i{display:inline-block;width:15px;height:3px;vertical-align:middle;margin-right:5px}.legend .proof{background:var(--proof)}.legend .candidate{background:var(--candidate)}.legend .reference{background:var(--reference)}
ul{padding-left:20px}.edge{border-top:1px solid var(--line);padding:9px 0}.edge strong{font-size:.92rem}.edge p{font-size:.87rem;color:var(--muted);margin:3px 0}.tag{display:inline-block;border:1px solid var(--line);padding:2px 7px;border-radius:20px;font-size:.75rem;margin-right:4px;background:#f8fafb}.tag.proof{color:var(--proof);border-color:#accfc6}.tag.candidate{color:var(--candidate);border-color:#ddcca8}.tag.reference{color:var(--reference)}
#edges{max-height:540px;overflow:auto}#ratio{white-space:pre-wrap;overflow-wrap:anywhere;font-size:.86rem;line-height:1.55}#path{min-height:26px;white-space:pre-wrap;color:var(--muted)}
.fine{border-top:1px solid var(--line);padding-top:12px;margin-top:18px}.pair{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:end;margin-top:12px}
@media(max-width:850px){.toolbar,.cols{grid-template-columns:1fr}.pair{grid-template-columns:1fr}main{padding:12px}#plot{min-height:330px}svg{min-height:330px}}
</style></head><body>
<header><h1>Komorebi / Sequence Transfer Atlas</h1><p class="muted">__SUMMARY__ · Author: Komorebi P.</p><p>Explore exact sequence representations. <b>Green:</b> algebraic identity with proof argument. <b>Amber:</b> exact finite-prefix candidate. Grey: source representation or reference. Candidate paths are never represented as proofs.</p></header>
<main><div class="toolbar"><div><label for="select">Select a sequence or formula node</label><input id="select" type="search" list="choices" placeholder="A000045, Fibonacci, Catalan…"><datalist id="choices"></datalist></div><div><label for="kind">Edge class</label><select id="kind"><option value="all">All classes</option><option value="algebraic_identity">Proved identities only</option><option value="finite_candidate">Finite candidates only</option><option value="recorded_representation">Recorded formulas</option><option value="crosswalk_reference">Cross-references</option></select></div><div><label for="op">Operator</label><select id="op"><option value="all">All operators</option></select></div></div>
<div class="cols"><section class="panel"><h2 id="selectedtitle">Neighborhood view</h2><p class="muted">Select a node to see incoming and outgoing transfers. Arrow direction matters. Hyperedges require all listed inputs.</p>
<div class="controls"><label><input type="checkbox" id="incoming" checked> Incoming</label><label><input type="checkbox" id="outgoing" checked> Outgoing</label><label><input type="checkbox" id="formulas"> Include formula nodes</label></div>
<div id="plot" role="region" aria-label="Transfer graph neighborhood" tabindex="0"><svg viewBox="0 0 880 560" xmlns="http://www.w3.org/2000/svg" aria-label="Transfer neighborhood graph"><text x="40" y="50">Select a sequence to draw the graph.</text></svg></div>
<div class="legend"><span><i class="proof"></i>Algebraic identity</span><span><i class="candidate"></i>Finite candidate</span><span><i class="reference"></i>Reference/recorded</span></div><p id="visible" class="muted"></p>
<div class="pair"><div><label for="destination">Find a proved route to</label><input id="destination" list="choices" placeholder="Destination OEIS ID"></div><button id="go">Find proved route</button></div><p id="path" role="status" aria-live="polite"></p></section>
<aside class="panel"><h2>Transfers and provenance</h2><p id="nodeinfo" class="muted">Select a graph node to inspect its relations.</p><div id="edges"></div><div class="fine"><h2>Rational-ratio candidate</h2><div id="ratio" class="muted">Available for sequences with an exact finite Pochhammer/rational-ratio fit.</div></div></aside></div>
<div class="fine muted">Data sources: <a href="https://oeis.org/">OEIS Foundation</a> (CC BY-SA 4.0) and Komorebi research sources. The graph is a mathematical working index: an OEIS record, finite prefix, or lexical cross-reference is not a proof of a global identity. Hyperedges are AND relations; both inputs are required. The shortest proved path is structural and not necessarily computationally cheapest.</div>
</main><script>const DATA=__DATA__;
const nodeMap=new Map(DATA.nodes.map(n=>[n.id,n]));const input=document.getElementById('select');const choice=document.getElementById('choices');const kind=document.getElementById('kind');const op=document.getElementById('op');const edgesDiv=document.getElementById('edges');
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const n of DATA.nodes){if(n.type==='oeis_sequence'||n.type==='komorebi_sequence'){const el=document.createElement('option');el.value=n.id+' — '+n.name.slice(0,75);choice.appendChild(el)}}
for(const operator of [...new Set(DATA.edges.map(e=>e.operator))].sort()){const el=document.createElement('option');el.value=operator;el.textContent=operator;op.appendChild(el)}
const color=e=>e.status==='algebraic_identity'?'#146657':e.status==='finite_candidate'?'#996110':'#536477';
let current='A000045';
function getId(s){s=s.trim();const m=s.match(/^(A\d{6}|K[A-Z0-9_-]+|FORMULA:[a-f0-9]+|HYPER:[a-f0-9]+|RATIO:A\d{6}|OP:[a-z_]+)/);if(m&&nodeMap.has(m[1]))return m[1];let z=DATA.nodes.find(x=>x.name.toLowerCase().includes(s.toLowerCase())&&s.length>2);return z?.id||null}
function filtered(){const f=kind.value;const o=op.value;const inc=document.getElementById('incoming').checked;const out=document.getElementById('outgoing').checked;const formulas=document.getElementById('formulas').checked;
return DATA.edges.filter(e=>(f==='all'||e.status===f)&&(o==='all'||e.operator===o)&&((inc&&e.target===current)||(out&&e.source===current))&&(formulas||!((nodeMap.get(e.source)?.type==='formula')||(nodeMap.get(e.target)?.type==='formula'))))}
function show(){document.getElementById('path').textContent='';const n=nodeMap.get(current);if(!n)return;document.getElementById('selectedtitle').textContent=n.name.slice(0,95);document.getElementById('nodeinfo').textContent=current+' — '+n.type;const related=filtered();const cap=34;document.getElementById('visible').textContent=related.length+' linked edges'+(related.length>cap?' (first '+cap+' drawn)':'')+'.';
const list=related.slice(0,cap);const around=[];for(const e of list){let id=e.source===current?e.target:e.source;if(!around.includes(id))around.push(id)}
const positions=new Map([[current,[440,270]]]);const w=880,h=560,step=Math.min(around.length,32);around.forEach((id,i)=>{const x=440+325*Math.cos(2*Math.PI*i/Math.max(step,1));const y=270+220*Math.sin(2*Math.PI*i/Math.max(step,1));positions.set(id,[x,y])});
let svg='<svg viewBox="0 0 880 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Neighborhood of '+escapeHTML(current)+'"><defs><marker id="a" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L0 6 L6 3 Z" fill="#536477"/></marker></defs>';
for(const e of list){const p=positions.get(e.source),q=positions.get(e.target);if(!p||!q)continue;svg+='<line x1="'+p[0]+'" y1="'+p[1]+'" x2="'+q[0]+'" y2="'+q[1]+'" stroke="'+color(e)+'" stroke-width="1.8" stroke-dasharray="'+(e.status==='finite_candidate'?'5 4':'')+'" marker-end="url(#a)" opacity=".76"/>'}
for(const [id,[x,y]] of positions){const selected=id===current;const label=(nodeMap.get(id)?.name||id).slice(0,20);svg+='<g class="node" data-id="'+escapeHTML(id)+'" tabindex="0" role="button" aria-label="Open '+escapeHTML(id)+'"><rect x="'+(x-53)+'" y="'+(y-24)+'" width="106" height="48" rx="7" fill="'+(selected?'#e4edf8':'white')+'" stroke="'+(selected?'#264d79':'#afbac9')+'" stroke-width="'+(selected?2:1)+'"/><text x="'+x+'" y="'+(y-6)+'" text-anchor="middle" font-weight="600">'+escapeHTML(id.slice(0,16))+'</text><text x="'+x+'" y="'+(y+11)+'" text-anchor="middle" font-size="10">'+escapeHTML(label)+'</text></g>'}
svg+='</svg>';document.getElementById('plot').innerHTML=svg;
for(const g of document.querySelectorAll('.node')){const sel=()=>{current=g.dataset.id;input.value=current;show()};g.addEventListener('click',sel);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();sel()}})}
edgesDiv.innerHTML=related.slice(0,100).map(e=>'<div class="edge"><span class="tag '+(e.status==='algebraic_identity'?'proof':e.status==='finite_candidate'?'candidate':'reference')+'">'+escapeHTML(e.status)+'</span><strong>'+escapeHTML(e.source)+' → '+escapeHTML(e.target)+'</strong><p>'+escapeHTML(e.operator)+' · '+escapeHTML(e.statement)+'</p><p>Exact comparisons: '+e.checked+'. '+escapeHTML(e.evidence)+'</p></div>').join('')||'<p class="muted">No links in this filter.</p>';
const r=DATA.ratios[current];document.getElementById('ratio').textContent=r?('a('+r.mathematical_start+') = '+r.base+'\nP(t) = '+r.numerator.join(', ')+' (ascending coefficients)\nQ(t) = '+r.denominator.join(', ')+' (ascending coefficients)\na(start+t+1)/a(start+t) = P(t)/Q(t)\nFit: '+r.fit+' ratios; holdout: '+r.holdout+'.\n'+(r.pochhammer?('Factorization: c = '+r.pochhammer.multiplier+'; upper = ['+r.pochhammer.upper.join(', ')+']; lower = ['+r.pochhammer.lower.join(', ')+']'):'Rational roots not all established')+'\nStatus: finite candidate, not a global theorem.'):'No rational-ratio candidate for this node.';
}
function proofRoute(src,dst){const adj=new Map();for(const e of DATA.edges){if(e.status!=='algebraic_identity')continue;if(!adj.has(e.source))adj.set(e.source,[]);adj.get(e.source).push(e)}let q=[src],seen=new Set([src]),prev=new Map();for(let i=0;i<q.length;i++){const x=q[i];if(x===dst)break;for(const e of adj.get(x)||[]){if(seen.has(e.target))continue;seen.add(e.target);prev.set(e.target,e);q.push(e.target)}}if(!seen.has(dst))return null;let p=[];while(dst!==src){const e=prev.get(dst);if(!e)return null;p.push(e);dst=e.source}return p.reverse()}
function search(){const id=getId(input.value);if(id){current=id;input.value=id;show()}else document.getElementById('visible').textContent='No matching graph node. Use an OEIS ID or a name fragment.'}
input.addEventListener('change',search);input.addEventListener('keydown',e=>{if(e.key==='Enter')search()});for(const id of ['kind','op','incoming','outgoing','formulas'])document.getElementById(id).addEventListener('change',show);
document.getElementById('go').addEventListener('click',()=>{const dst=getId(document.getElementById('destination').value);const e=document.getElementById('path');if(!dst){e.textContent='Unknown destination node.';return}if(current===dst){e.textContent='Start and destination coincide.';return}const route=proofRoute(current,dst);e.textContent=route?route.map(x=>x.source+' —['+x.operator+']→ '+x.target).join('\n'):'No route using only algebraic-identity edges. Finite candidates and references are excluded.'});input.value=current;show();
</script></body></html>'''
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html_template.replace('__SUMMARY__',escape(summary))
        .replace('__DATA__',dataset),encoding='utf-8')
    return {'html':str(target),'bytes':target.stat().st_size,
            'nodes':len(nodes),'edges':len(edges),'statuses':dict(total)}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:r=render(db,args.output)
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
