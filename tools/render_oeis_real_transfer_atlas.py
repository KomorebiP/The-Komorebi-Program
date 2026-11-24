"""Build a standalone, offline graph browser from real OEIS finite-transfer candidates.

Author: Komorebi P.
OEIS source: OEIS Foundation Inc., CC BY-SA 4.0.

This does not upgrade finite matches to all-index identities. A separately audited
handful of classical identities are labeled proved-from-definitions, with the
proof contract in REAL_OEIS_TRANSFER_AUDIT.md.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from html import escape
import json
from pathlib import Path
import sqlite3

PROVED = {
    ('A000108','A005043','inverse_binomial_transform'):
       'Catalan inverse-binomial transform = Riordan numbers; OGF substitution and first-order differential equation.',
    ('A010051','A000720','prefix_sum'):
       'Prime-counting function is the cumulative sum of the prime-indicator function.',
    ('A000217','A000027','adjacent_difference'):
       'Differences of triangular numbers equal the positive integers, with explicit offsets.',
    ('A000290','A005408','adjacent_difference'):
       'Consecutive square differences give 2n+1.',
    ('A000045','A001906','polyphase'):
       'Even-index Fibonacci subsequence, by its defining recurrence and initial terms.',
}


def build(db:sqlite3.Connection, output:Path, jsonl:Path, summary:Path):
    names=dict(db.execute('SELECT oeis_id,name FROM sequences'))
    rows=db.execute('''SELECT candidate_id,output_id,inputs_json,operator,parameters_json,
           checked_terms,holdout_terms,statement FROM transfer_candidates
           WHERE status='finite_candidate' ORDER BY holdout_terms DESC,candidate_id''')
    candidates=[]
    operator=Counter();vertices=set();by_input=defaultdict(list);pairset=set()
    parents={}
    def root(a):
        parents.setdefault(a,a)
        while parents[a]!=a:
            parents[a]=parents[parents[a]]
            a=parents[a]
        return a
    for cid,out,inputs_raw,op,params_raw,checked,holdout,statement in rows:
        inputs=json.loads(inputs_raw)
        if len(inputs)!=1:raise ValueError('Expected single-source relation from indexed miner')
        inp=inputs[0]
        if out not in names or inp not in names:raise ValueError('Candidate references a missing source')
        par=json.loads(params_raw)
        pair=(inp,out,op)
        hint=PROVED.get(pair)
        item={'id':cid,'source':inp,'target':out,'operator':op,'params':par,
              'checked':checked,'holdout':holdout,'statement':statement,
              'source_name':names[inp],'target_name':names[out],
              'proof':hint or None}
        candidates.append(item);operator[op]+=1;vertices.update((inp,out));pairset.add(tuple(sorted((inp,out))))
        a,b=root(inp),root(out)
        if a!=b:parents[a]=b
    groups=Counter(root(v) for v in vertices)
    proved=[x for x in candidates if x['proof']]
    if len(proved)!=len(PROVED):
        missing=[k for k in PROVED if not any((x['source'],x['target'],x['operator'])==k for x in proved)]
        raise ValueError('Expected classical recovered identities absent: '+str(missing))
    counts={'source':'official OEIS source, independent Komorebi transfer mining',
            'scope':'finite-prefix links are candidates, never proven all-index by numeric agreement',
            'imported_sequences':db.execute('SELECT count(*) FROM sequences').fetchone()[0],
            'all_candidate_links':len(candidates),'vertices_with_links':len(vertices),
            'components':len(groups),'largest_component':max(groups.values()),
            'unique_undirected_pairs':len(pairset),'operator_counts':dict(operator),
            'candidates_with_10_holdout':sum(x['holdout']>=10 for x in candidates),
            'candidates_with_20_holdout':sum(x['holdout']>=20 for x in candidates),
            'independently_proved_examples':len(proved),
            'proof_examples':[{k:x[k] for k in ('source','target','operator','checked','holdout','proof')} for x in proved],
            'raw_formula_lines':db.execute("SELECT count(*) FROM formulas WHERE origin='oeis_formula'").fetchone()[0],
            'raw_program_blocks':db.execute("SELECT count(*) FROM formulas WHERE origin='oeis_program'").fetchone()[0],
            'finite_checked_normalized_formulas':db.execute("SELECT count(*) FROM formulas WHERE verification='finite_checked' AND origin='oeis_normalized'").fetchone()[0]}
    output.parent.mkdir(parents=True,exist_ok=True)
    jsonl.parent.mkdir(parents=True,exist_ok=True)
    with jsonl.open('w',encoding='utf-8') as stream:
        for x in candidates:stream.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
    summary.write_text(json.dumps(counts,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    payload=json.dumps({'rows':candidates,'summary':counts},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    options=''.join('<option value="'+escape(op)+'">'+escape(op.replace('_',' '))+' · '+str(n)+'</option>' for op,n in operator.most_common())
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi OEIS Real Transfer Atlas</title>
<style>
:root{color-scheme:light dark;--bg:#fafafa;--fg:#18252f;--panel:#fff;--line:#d5dce4;--muted:#5a6877;--accent:#18558a;--soft:#eef3f8;--ok:#11734a}
@media(prefers-color-scheme:dark){:root{--bg:#101820;--fg:#eef4f7;--panel:#17232d;--line:#364754;--muted:#b0bec9;--accent:#8fc7ff;--soft:#233442;--ok:#8bddbc}}
*{box-sizing:border-box}body{background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.48;margin:0}main{max-width:1180px;margin:auto;padding:20px 18px 90px}h1{font-size:clamp(1.5rem,4vw,2.25rem);margin:.45em 0}h2{font-size:1.17rem}p{max-width:82ch}.sub{color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:10px;margin:20px 0}.stat{border:1px solid var(--line);border-radius:12px;padding:13px;background:var(--panel)}.stat strong{display:block;font-size:1.65rem}.stat small{color:var(--muted)}.controls{display:flex;gap:12px;flex-wrap:wrap;align-items:end;padding:15px;border:1px solid var(--line);background:var(--panel);border-radius:12px}.controls label{display:flex;flex-direction:column;gap:4px;font-size:.84rem;color:var(--muted)}input,select,button{background:var(--panel);color:var(--fg);border:1px solid var(--line);padding:8px;border-radius:6px;font:inherit}input[type=search]{width:min(410px,85vw)}button{cursor:pointer;background:var(--soft)}button:hover{outline:2px solid var(--accent)}#results{display:grid;gap:9px;margin:15px 0}.item{border:1px solid var(--line);border-radius:10px;background:var(--panel);padding:12px;display:grid;gap:6px}.row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.pill{font-size:.75rem;background:var(--soft);padding:3px 7px;border-radius:5px}a{color:var(--accent)}a:hover{text-decoration:underline}.item h3{margin:0;font-size:1rem;font-weight:650}.item code{white-space:pre-wrap;word-break:break-word;background:var(--soft);padding:6px;font-size:.82rem;border-radius:4px}.proof{border-left:4px solid var(--ok);padding-left:9px}.muted{color:var(--muted);font-size:.86rem}.footer{color:var(--muted);font-size:.85rem}.component{border:1px solid var(--line);padding:12px;border-radius:10px;background:var(--panel)}#neighbors{margin:10px 0}.node{cursor:pointer;fill:var(--panel);stroke:var(--accent);stroke-width:1.5}.node.highlight{stroke-width:3;stroke:var(--ok)}svg text{fill:var(--fg);font:10px system-ui}.link{stroke:var(--line);stroke-width:1.3}button:disabled{opacity:.45;cursor:default}</style></head>
<body><main><header><div class="sub">Komorebi P. · OEIS-derived data CC BY-SA 4.0 · 22 November 2026</div><h1>Real OEIS transfer atlas</h1>
<p>Exact numerical agreement across finite OEIS excerpts is <strong>not</strong> proof of an infinite identity. Five illustrative transfers have independent all-index mathematical arguments based on their sequence definitions. All other links remain candidates, regardless of holdout length.</p>
</header><section class="stats" id="stats" aria-label="Dataset statistics"></section>
<h2>Browse the candidate graph</h2><div class="controls"><label>Search IDs or sequence names<input type="search" id="search" placeholder="Fibonacci, Catalan, A000108…"></label>
<label>Operator<select id="operator"><option value="">All operations</option>___OPTIONS___</select></label>
<label>Minimum holdout terms<input type="number" id="holdout" min="1" max="100" value="10" style="width:100px"></label>
<label>Evidence<select id="evidence"><option value="">All evidence</option><option value="proof">Proved examples only</option><option value="candidate">Numerical candidates only</option></select></label></div>
<p id="count" aria-live="polite" class="muted"></p><div id="results"></div><button id="more">Show 50 more</button>
<h2>Inspect a sequence neighborhood</h2><p class="sub">Select a source OEIS ID to plot its neighboring transformations and their directions. The drawing is a local neighborhood, not the entire graph.</p><div class="controls"><label>Sequence ID<input id="focus" value="A000108" pattern="A[0-9]{6}"></label><button id="focusGo">Display neighborhood</button><span class="muted" id="neighborDesc"></span></div>
<div class="component" id="neighbors"><svg id="graph" role="img" aria-label="Sequence neighborhood graph" width="100%" viewBox="0 0 760 350"></svg></div>
<h2>All-index proof exemplar: Catalan → Riordan</h2>
<p>The inverse binomial transform of Catalan numbers has ordinary generating function</p>
<p><code>R(x) = (1/(1+x)) C(x/(1+x)) = (1 − sqrt((1−3x)/(1+x)))/(2x)</code></p>
<p>It satisfies <code>x(1−2x−3x²)R′(x) + (1−3x²)R(x) = 1</code>, with <code>R(0)=1</code>; hence <code>(n+1)r(n)=(n−1)(2r(n−1)+3r(n−2))</code> for n≥2 and <code>r(1)=0</code>. This is the defining Riordan recurrence of OEIS A005043. See the included detailed audit for the complete proof and index conventions.</p>
<footer class="footer">Source: <a href="https://oeis.org/">OEIS Foundation</a> · <a href="https://oeis.org/LICENSE">CC BY-SA 4.0</a>. Program text and untrusted formula fields are not executed. Search is local and does not send queries to a server.</footer></main>
<script id="catalog" type="application/json">___DATA___</script><script>
'use strict';const data=JSON.parse(document.getElementById('catalog').textContent);const rows=data.rows;const sum=data.summary;
const el=id=>document.getElementById(id), ns='http://www.w3.org/2000/svg';
const metric=[['Real OEIS records',sum.imported_sequences],['Finite candidate links',sum.all_candidate_links],['Connected sequences',sum.vertices_with_links],['20+ holdout terms',sum.candidates_with_20_holdout],['Independently proved examples',sum.independently_proved_examples],['Graph components',sum.components]];
metric.forEach(([lab,val])=>{const b=document.createElement('div');b.className='stat';const strong=document.createElement('strong');strong.textContent=Number(val).toLocaleString();const small=document.createElement('small');small.textContent=lab;b.append(strong,small);el('stats').append(b)});
let matched=[],visible=50;
function link(id){const a=document.createElement('a');a.href='https://oeis.org/'+encodeURIComponent(id);a.textContent=id;a.target='_blank';a.rel='noopener';return a}
function filt(){const query=el('search').value.trim().toLowerCase(),op=el('operator').value,holdout=Math.max(1,Number(el('holdout').value)||1),ev=el('evidence').value;return rows.filter(r=>(!op||r.operator===op)&&r.holdout>=holdout&&(!ev||(ev==='proof'?!!r.proof:!r.proof))&&(!query||[r.source,r.target,r.source_name,r.target_name,r.operator].some(t=>t.toLowerCase().includes(query))))}
function render(){matched=filt();const list=el('results');list.replaceChildren();const sample=matched.slice(0,visible);for(const x of sample){const box=document.createElement('article');box.className='item'+(x.proof?' proof':'');const top=document.createElement('div');top.className='row';top.append(link(x.source));const arrow=document.createElement('span');arrow.textContent='→';top.append(arrow,link(x.target));const pill=document.createElement('span');pill.className='pill';pill.textContent=x.operator.replaceAll('_',' ');top.append(pill);const status=document.createElement('span');status.className='muted';status.textContent=x.proof?'Definition-level proof':'Finite candidate';top.append(status);
const title=document.createElement('div');title.className='muted';title.textContent=x.source_name+'  →  '+x.target_name;const code=document.createElement('code');code.textContent=x.statement;const footer=document.createElement('div');footer.className='muted';footer.textContent=`${x.checked} exact compared terms · ${x.holdout} holdout terms`;
box.append(top,title,code,footer);if(x.proof){const note=document.createElement('div');note.textContent='Proof route: '+x.proof;box.append(note)}list.append(box)}el('count').textContent=matched.length.toLocaleString()+' matches · showing '+sample.length.toLocaleString();el('more').disabled=visible>=matched.length}
for(const id of ['search','operator','holdout','evidence'])el(id).addEventListener('input',()=>{visible=50;render()});el('more').addEventListener('click',()=>{visible+=50;render()});render();
const adj=new Map();rows.forEach(x=>{if(!adj.has(x.source))adj.set(x.source,[]);if(!adj.has(x.target))adj.set(x.target,[]);adj.get(x.source).push(x);adj.get(x.target).push(x)});
function svgElem(name,attrs){const v=document.createElementNS(ns,name);Object.entries(attrs).forEach(([k,val])=>v.setAttribute(k,String(val)));return v}
function neighborhood(){const focus=el('focus').value.toUpperCase().trim(),svg=el('graph');svg.replaceChildren();const links=(adj.get(focus)||[]).slice().sort((a,b)=>b.holdout-a.holdout).slice(0,36);const nodes=[focus,...new Set(links.map(l=>l.source===focus?l.target:l.source))];el('neighborDesc').textContent=`${(adj.get(focus)||[]).length} neighboring candidate edges · displaying ${links.length}`;if(!links.length){const label=svgElem('text',{x:18,y:34});label.textContent='No indexed neighbor found for '+focus;svg.append(label);return}
const xy=new Map([[focus,[380,170]]]);nodes.slice(1).forEach((v,i)=>{const angle=2*Math.PI*i/Math.max(1,nodes.length-1);xy.set(v,[380+290*Math.cos(angle),170+137*Math.sin(angle)])});
for(const edge of links){const a=xy.get(edge.source),b=xy.get(edge.target);svg.append(svgElem('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],class:'link'}))}
for(const id of nodes){const [x,y]=xy.get(id);const circle=svgElem('circle',{cx:x,cy:y,r:id===focus?11:7,class:'node'+(id===focus?' highlight':'')});const ttl=svgElem('title',{});ttl.textContent=id;circle.append(ttl);circle.addEventListener('click',()=>{el('focus').value=id;neighborhood()});svg.append(circle);const label=svgElem('text',{x:x+11,y:y-8});label.textContent=id;svg.append(label)}}
el('focusGo').addEventListener('click',neighborhood);el('focus').addEventListener('keydown',e=>{if(e.key==='Enter')neighborhood()});neighborhood();
</script></body></html>'''.replace('___OPTIONS___',options).replace('___DATA___',payload)
    output.write_text(html,encoding='utf-8')
    return counts


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--jsonl',type=Path,required=True)
    p.add_argument('--summary',type=Path,required=True)
    a=p.parse_args()
    with sqlite3.connect(a.db) as db:report=build(db,a.output,a.jsonl,a.summary)
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
