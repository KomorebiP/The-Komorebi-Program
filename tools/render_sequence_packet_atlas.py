"""Create a self-contained, read-only atlas of exact recurrence phase packets.

Author: Komorebi P. Uses only retained mathematical certificate data.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
DEFAULT=BASE/'sequence-packet-atlas.html'


def build(root:Path=BASE,output:Path=DEFAULT):
    folder=root/'research/oeis-formulas'
    phases=[json.loads(line) for line in (folder/'phase-formulas.jsonl').read_text().splitlines() if line]
    links=[json.loads(line) for line in (folder/'exact-linear-identities.jsonl').read_text().splitlines() if line]
    basis=json.loads((folder/'EXACT_BASIS.json').read_text())
    packet=json.loads((folder/'packet-atlas-index.json').read_text())
    if not phases or not links or not basis['basis']:
        raise ValueError('No exact phase or identity certificates')
    counts={'phase_count':len(phases),'transfer_count':len(links),'source_count':len({v['source'] for v in phases}),
            'basis_size':len(basis['basis']),'module_count':packet['denominator_modules']}
    jsondata=json.dumps({'counts':counts,'phases':phases,'links':links,'basis':basis,'packet':packet},separators=(',',':'),ensure_ascii=False).replace('</','<\\/')
    doc='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi | Exact Sequence Transfer Atlas</title>
<style>
:root{color-scheme:light dark;--bg:#f9fafb;--card:#fff;--ink:#1f2a3a;--soft:#576577;--line:#dbe2e9;--accent:#174f93;--panel:#f1f5f9}
@media(prefers-color-scheme:dark){:root{--bg:#101720;--card:#192431;--ink:#e6edf4;--soft:#abbacf;--line:#374455;--accent:#9bcbff;--panel:#253343}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1150px;margin:0 auto;padding:32px 18px 60px}h1{font-size:clamp(1.55rem,3vw,2.4rem);margin:0 0 10px;letter-spacing:-.03em}h2{font-size:1.3rem}p{color:var(--soft)}a{color:var(--accent)}.muted{color:var(--soft)}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:11px;margin:24px 0}.metric{border:1px solid var(--line);padding:15px;border-radius:11px;background:var(--card)}.metric b{display:block;font-size:1.6rem}.metric small{color:var(--soft)}.tabs{display:flex;gap:7px;margin:26px 0 12px;flex-wrap:wrap}.tabs button{border:1px solid var(--line);background:var(--card);padding:9px 14px;color:var(--ink);border-radius:9px;cursor:pointer}.tabs button[aria-selected=true]{background:var(--accent);color:var(--bg);font-weight:700}.toolbar{display:flex;gap:10px;flex-wrap:wrap;margin:12px 0}input,select{padding:11px 12px;border:1px solid var(--line);color:var(--ink);background:var(--card);border-radius:8px;min-width:170px;flex:1}select{flex:0 1 195px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:12px}.item{background:var(--card);border:1px solid var(--line);padding:14px;border-radius:10px;min-width:0}.item h3{margin:0 0 6px;font-size:1rem}.item p{margin:5px 0}.item code{word-break:break-word;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85rem;color:var(--ink)}.pill{color:var(--accent);font-size:12px;font-weight:700}.foot{font-size:.82rem;border-top:1px solid var(--line);margin-top:35px;padding-top:15px}.hidden{display:none}button.more{padding:12px 22px;border:1px solid var(--line);border-radius:9px;background:var(--card);color:var(--ink);cursor:pointer;margin-top:20px}#count{font-size:13px;color:var(--soft)}
</style></head><body><main><h1>Exact Sequence Transfer Atlas</h1><p>Komorebi P. · OEIS formula and recurrence compilation · exact algebra, separate from finite OEIS identification</p>
<div class="metrics" id="metrics"></div>
<p><strong>Scope:</strong> Phase recurrences follow from the supplied constant-coefficient recurrences by Cayley–Hamilton and observability. Expression transfers follow from canonical algebra. Neither result alone proves that its attributed OEIS sequence is globally identical to the supplied curated formula.</p>
<div class="tabs" role="tablist" aria-label="Atlas collections"><button data-tab="identity" aria-selected="true">Exact transfers</button><button data-tab="phase" aria-selected="false">Polyphase recurrences</button><button data-tab="basis" aria-selected="false">Linear basis</button></div>
<div class="toolbar"><label for="query" class="hidden">Search certificates</label><input id="query" type="search" placeholder="Search OEIS ID, operator, or formula" aria-label="Search certificates"><select id="category" aria-label="Filter operator"><option value="">All operator classes</option></select></div>
<p id="count" role="status" aria-live="polite"></p><div id="cards" class="grid"></div><button type="button" class="more hidden" id="more">Show more</button>
<p class="foot">OEIS attribution: The Online Encyclopedia of Integer Sequences, OEIS Foundation Inc. · OEIS-derived data CC BY-SA 4.0. Source terms were finite-checked; displayed transfer certificates concern exact curated formula definitions, and no historical novelty is claimed.</p></main>
<script id="embedded" type="application/json">__DATA__</script><script>
'use strict'; const data=JSON.parse(document.getElementById('embedded').textContent); const $=id=>document.getElementById(id); let current='identity',shown=40;
const metrics=[['Polyphase formulas',data.counts.phase_count],['Algebraic transfers',data.counts.transfer_count],['Source sequences',data.counts.source_count],['Shared denominator modules',data.counts.module_count],['Expression basis',data.counts.basis_size]];
for(const [label,count] of metrics){const v=document.createElement('div');v.className='metric';const b=document.createElement('b');b.textContent=count.toLocaleString();const s=document.createElement('small');s.textContent=label;v.append(b,s);$('metrics').append(v)}
function el(tag,klass,txt){const x=document.createElement(tag);if(klass)x.className=klass;if(txt!==undefined)x.textContent=String(txt);return x}
function mk(label,value){const p=el('p');p.append(el('span','muted',label+' '),el('code','',value));return p}
function card(v,kind){const c=el('div','item');let h='';if(kind==='identity'){
h=v.target+' ← '+v.sources.join(', ');c.append(el('span','pill',v.operator.replaceAll('_',' ')),el('h3','',h),mk('Identity:',v.statement),mk('Parameters:',JSON.stringify(v.parameters)),el('p','muted','All-index formula algebra; source OEIS match is finite-checked'))
}else if(kind==='phase'){
h=v.source+' · m='+v.modulus+', r='+v.residue;c.append(el('span','pill','Exact phase recurrence'),el('h3','',h),mk('Order:',v.recurrence.order),mk('Coefficients:',v.recurrence.coefficients.join(', ')||'[zero]'),mk('Initial:',v.recurrence.initial.slice(0,7).join(', ')||'[zero]'))
}else{h=v.target;c.append(el('span','pill','Exact basis projection'),el('h3','',h),mk('Representation:',v.coefficients.map(t=>t.weight+' × '+t.source).join(' + ')||'0'))}return c}
function collection(){if(current==='identity')return data.links;if(current==='phase')return data.phases;return data.basis.projections}
function options(){const select=$('category');select.replaceChildren(el('option','','All operator classes'));select.firstChild.value='';if(current==='identity'){const names=[...new Set(data.links.map(v=>v.operator))].sort();for(const name of names){const o=el('option','',name.replaceAll('_',' '));o.value=name;select.append(o)}}else if(current==='phase'){for(const n of [2,3,4,5,6,7,8]){const o=el('option','',`mod ${n}`);o.value=String(n);select.append(o)}}else{select.classList.add('hidden');return}select.classList.remove('hidden')}
function repaint(){const needle=$('query').value.trim().toLowerCase(),category=$('category').value;const arr=collection().filter(x=>{if(category && (current==='phase'?String(x.modulus)!==category:x.operator!==category))return false;return (JSON.stringify(x).toLowerCase().includes(needle))});$('cards').replaceChildren(...arr.slice(0,shown).map(x=>card(x,current)));$('count').textContent=`${arr.length.toLocaleString()} ${current==='phase'?'phase formulas':current==='basis'?'basis projections':'algebraic identities'} · showing ${Math.min(shown,arr.length).toLocaleString()}`;$('more').classList.toggle('hidden',shown>=arr.length)}
for(const b of document.querySelectorAll('[data-tab]'))b.addEventListener('click',()=>{current=b.dataset.tab;shown=40;for(const t of document.querySelectorAll('[data-tab]'))t.setAttribute('aria-selected',String(t===b));options();repaint()});$('query').addEventListener('input',()=>{shown=40;repaint()});$('category').addEventListener('change',()=>{shown=40;repaint()});$('more').addEventListener('click',()=>{shown+=40;repaint()});options();repaint();
</script></body></html>'''.replace('__DATA__',jsondata)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(doc,encoding='utf-8')
    return counts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=BASE)
    parser.add_argument('--output',type=Path,default=DEFAULT)
    args=parser.parse_args()
    print(json.dumps(build(args.root,args.output),indent=2))

if __name__=='__main__':main()
