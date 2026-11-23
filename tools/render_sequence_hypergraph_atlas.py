"""Export safe static searchable proof-gated OEIS hyperedge atlas.

Author: Komorebi P. Raw OEIS code is never executed. No external runtime.
"""
from __future__ import annotations
import argparse,html,json
from collections import Counter
from pathlib import Path


def render(ledger,output):
    records=[json.loads(line) for line in Path(ledger).read_text(encoding='utf-8').splitlines() if line.strip()]
    view=[]
    for c in records:
        maps=c['index_maps']
        indexed=any(pair!=[1,0] for values in maps.values() for pair in values)
        mgt1=any(pair[0]>1 for values in maps.values() for pair in values)
        view.append({'id':c['target'],'inputs':c['inputs'],'rhs':c['rhs'],
            'index_maps':maps,'kind':'multi-input' if len(c['inputs'])>1 else 'single-input',
            'type':'polyphase' if mgt1 else ('shifted' if indexed else 'aligned'),
            'formula_id':c['formula_id'][:16]})
    payload=json.dumps(view,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e')
    body='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Komorebi | Exact Formula Hypergraph v1.2</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark;
--bg:#f8fafc;--surface:#fff;--ink:#101927;--dim:#52637a;--border:#d8e0eb;
--accent:#1f4a82;--soft:#ecf3fb}
@media(prefers-color-scheme:dark){:root{--bg:#101722;--surface:#192333;--ink:#f4f7fa;--dim:#b3c0d1;--border:#39495f;--accent:#97befb;--soft:#24374e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);line-height:1.5}
main{max-width:1100px;margin:auto;padding:28px 20px 64px}h1{font-size:clamp(24px,4vw,38px);line-height:1.15;letter-spacing:-.03em}h2{font-size:19px}
a{color:var(--accent)}p{max-width:80ch;color:var(--dim)}.top{margin-bottom:22px}.sub{margin-top:-8px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:24px 0}
.stat{border:1px solid var(--border);border-radius:12px;background:var(--surface);padding:15px}
.stat strong{font-size:28px;display:block;font-variant-numeric:tabular-nums}.stat span{font-size:13px;color:var(--dim)}
.controls{display:flex;flex-wrap:wrap;gap:10px;padding:14px;background:var(--surface);border:1px solid var(--border);border-radius:12px}
input,select{background:var(--bg);border:1px solid var(--border);border-radius:7px;color:var(--ink);padding:11px;font:inherit}
input{flex:2;min-width:190px}select{flex:1;min-width:150px}#shown{margin:15px 0;font-size:14px}
article{border:1px solid var(--border);border-radius:11px;padding:15px 17px;margin:10px 0;background:var(--surface)}
.row{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px}.id{font-size:18px;font-weight:700}
.tags{font-size:12px;color:var(--dim)}.formula{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--soft);border-radius:7px;padding:10px;margin:11px 0;font:14px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--ink)}
details summary{cursor:pointer;color:var(--accent);font-size:13px}pre{overflow-x:auto;white-space:pre-wrap;font-size:13px;color:var(--dim)}
.note{font-size:13px;color:var(--dim)}footer{border-top:1px solid var(--border);margin-top:36px;padding-top:20px;font-size:13px;color:var(--dim)}
</style></head><body><main>
<div class="top"><h1>Exact formula transfer hypergraph</h1>
<p class="sub">Komorebi P. · v1.2 · Official OEIS source excerpt corpus</p>
<p>Each card is an independently replayed all-index algebraic identity between <strong>extracted formula expressions</strong>. OEIS record identifications were checked over finite source excerpts only. Arrows are directed. This atlas does not assert that all OEIS identities are globally proved.</p></div>
<div class="stats" id="stats"></div>
<div class="controls"><input id="search" type="search" placeholder="Search A000108, formula, input..." aria-label="Search formula identities">
<select id="arity" aria-label="Input count"><option value="all">All input counts</option><option value="multi-input">Multi-input only</option><option value="single-input">Single-input only</option></select>
<select id="type" aria-label="Index map"><option value="all">All index maps</option><option value="aligned">Aligned prefixes</option><option value="shifted">Shifted index</option><option value="polyphase">Polyphase index</option></select></div>
<div id="shown" aria-live="polite"></div><section id="cards" aria-label="Verified formula relationships"></section>
<footer>All-index formula equalities are certified by canonical exponential-polynomial algebra, with source-hash and raw-formula checks. The 539 relationships include 387 unary and 152 multi-input formulas. Program source text is never executed. OEIS Foundation data attribution and CC BY-SA 4.0 apply to OEIS-derived excerpts. Reusing the exact computer code is governed by the Komorebi repository's code license.</footer>
</main><script id="data" type="application/json">__DATA__</script><script>
'use strict';const data=JSON.parse(document.getElementById('data').textContent);
const stats=document.getElementById('stats');
for(const [number,label] of [['539','Formula identities'],['152','Multi-input'],['429','Prefix aligned'],['110','Shifted or polyphase']]){
 const box=document.createElement('div');box.className='stat';const a=document.createElement('strong');a.textContent=number;const b=document.createElement('span');b.textContent=label;box.append(a,b);stats.appendChild(box)}
const search=document.getElementById('search'),arity=document.getElementById('arity'),type=document.getElementById('type');
function oeisLink(id){const a=document.createElement('a');a.href='https://oeis.org/'+id;a.rel='noopener noreferrer';a.target='_blank';a.textContent=id;return a}
function makeCard(c){const el=document.createElement('article');const header=document.createElement('div');header.className='row';
 const ident=document.createElement('div');ident.className='id';ident.append(oeisLink(c.id));
 const tags=document.createElement('div');tags.className='tags';tags.textContent=c.kind+' · '+c.type;header.append(ident,tags);el.append(header);
 const inputs=document.createElement('div');inputs.className='note';inputs.append('Depends on: ');for(let i=0;i<c.inputs.length;i++){if(i)inputs.append(' and ');inputs.append(oeisLink(c.inputs[i]))}el.append(inputs);
 const formula=document.createElement('div');formula.className='formula';formula.textContent=c.id+'(n) = '+c.rhs;el.append(formula);
 const details=document.createElement('details');const head=document.createElement('summary');head.textContent='Inspect mathematical index maps and source receipt';const pre=document.createElement('pre');
 pre.textContent=JSON.stringify({index_maps_local_t:c.index_maps,source_formula_id_prefix:c.formula_id,evidence:'exact extracted-formula identity; finite OEIS identity check'},null,2);
 details.append(head,pre);el.append(details);return el}
function render(){const q=search.value.toLowerCase().trim(),t=type.value,a=arity.value;
 const found=data.filter(c=>(a==='all'||a===c.kind)&&(t==='all'||t===c.type)&&(!q||[c.id,c.rhs,...c.inputs].join(' ').toLowerCase().includes(q)));
 document.getElementById('shown').textContent=`${found.length.toLocaleString()} of ${data.length.toLocaleString()} exact formula links`;
 const container=document.getElementById('cards');container.replaceChildren();const fragment=document.createDocumentFragment();
 for(const c of found.slice(0,150)){fragment.append(makeCard(c))}container.appendChild(fragment);
 if(found.length>150){const hint=document.createElement('p');hint.textContent='Showing the first 150 results. Narrow the search to inspect additional links.';container.append(hint)}}
for(const e of [search,arity,type])e.addEventListener('input',render);render();
</script></body></html>'''
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(body.replace('__DATA__',payload),encoding='utf-8')
    return {'links':len(view),'multiple_input':sum(len(x['inputs'])>1 for x in view),
        'indexed':sum(x['type']!='aligned' for x in view),'output_bytes':output.stat().st_size}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ledger',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args(argv);print(json.dumps(render(a.ledger,a.output)))
if __name__=='__main__':main()
