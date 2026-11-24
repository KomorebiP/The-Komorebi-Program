"""Standalone searchable HTML for real OEIS formula transfers and shared basis.

Author: Komorebi P. Uses JSON-only data and textContent, never evaluates formula
text or arbitrary OEIS source code in the browser.
"""
from __future__ import annotations
import argparse,html,json,sqlite3
from pathlib import Path


CSS='''
:root{color-scheme:light dark;font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;--bg:#f7f8fa;--surface:#fff;--ink:#1a2433;--muted:#566171;--line:#d6dee8;--navy:#184d85;--s:#eef4ff}
@media(prefers-color-scheme:dark){:root{--bg:#10151d;--surface:#1d2633;--ink:#f0f3f7;--muted:#aeb9c8;--line:#3c485a;--navy:#9ac4ff;--s:#252f40}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink)}main{max-width:1250px;margin:auto;padding:24px 18px 70px}h1{line-height:1.15;font-size:clamp(1.6rem,3.4vw,2.5rem);margin:.4rem 0}h2{font-size:1.3rem;margin-top:2.3rem}p{max-width:95ch}a{color:var(--navy)}small,.muted{color:var(--muted)}.intro{font-size:1.07rem;color:var(--muted)}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0}.metric{background:var(--surface);border:1px solid var(--line);padding:17px;border-radius:12px}.metric b{font-size:1.8rem;display:block;font-variant-numeric:tabular-nums}.metric small{display:block}.controls{background:var(--surface);border:1px solid var(--line);padding:14px;border-radius:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:end}label{display:flex;flex-direction:column;gap:5px;color:var(--muted);font-size:.88rem;flex:1;min-width:185px}input,select{width:100%;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:8px;padding:11px;font:inherit}button{font:inherit;background:var(--surface);border:1px solid var(--line);padding:8px 12px;border-radius:8px;color:var(--ink);cursor:pointer}button:focus,input:focus,select:focus,a:focus{outline:3px solid var(--navy);outline-offset:2px}.toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:12px 0}.tablebox{overflow:auto;max-height:720px;border:1px solid var(--line);border-radius:10px;background:var(--surface)}table{border-collapse:collapse;width:100%;font-size:.91rem}td,th{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}th{position:sticky;top:0;background:var(--surface);z-index:1}tr:hover td{background:var(--s)}code{font:0.9em ui-monospace,SFMono-Regular,Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}.pill{display:inline-block;border:1px solid var(--line);color:var(--muted);border-radius:100px;padding:2px 8px;font-size:.8rem}.notice{padding:13px 0;border-block:1px solid var(--line)}.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.tabs button[aria-selected=true]{background:var(--s);border-color:var(--navy);font-weight:bold}details{padding:10px 0}summary{cursor:pointer}.hidden{display:none!important}#basisDetail{max-height:300px;overflow:auto;background:var(--surface);padding:16px;border:1px solid var(--line);border-radius:10px}
'''
JS=r'''
const raw = JSON.parse(document.getElementById('dataPayload').textContent);
const edges = raw.edges, projections = raw.projections, names = raw.names, basis = raw.basis;
const rows=projections, pageSize=120;
let active='edges',currentPage=0;
const $=id=>document.getElementById(id);
const clear=node=>node.replaceChildren();
const cell=(parent,t,tag='td')=>{const e=document.createElement(tag);e.textContent=String(t);parent.appendChild(e);return e;};
const linked=(parent,id)=>{const c=document.createElement('td');const a=document.createElement('a');a.href='https://oeis.org/'+id;a.target='_blank';a.rel='noopener noreferrer';a.textContent=id;c.appendChild(a);parent.appendChild(c);return c;};
const title=id=>names[id]||id;
const filtered=()=>{
const q=$('query').value.trim().toLowerCase();const op=$('operation').value;
if(active==='edges')return edges.filter(e=>(!op||e.operator===op)&&(!q||[e.source,e.target,title(e.source),title(e.target),e.operator].join(' ').toLowerCase().includes(q)));
return rows.filter(r=>!q||[r.target,title(r.target),...r.linear_combination.map(x=>x.source)].join(' ').toLowerCase().includes(q));
};
function render(){const list=filtered();const start=currentPage*pageSize;const visible=list.slice(start,start+pageSize);$('resultCount').textContent=`${list.length.toLocaleString()} ${active==='edges'?'formula identities':'basis projections'}`;$('pageLabel').textContent=`Page ${currentPage+1} of ${Math.max(1,Math.ceil(list.length/pageSize))}`;$('previous').disabled=currentPage===0;$('next').disabled=start+pageSize>=list.length;const root=$('tableBody');clear(root);
for(const e of visible){let tr=document.createElement('tr');if(active==='edges'){
linked(tr,e.source);linked(tr,e.target);cell(tr,e.operator);cell(tr,JSON.stringify(e.parameters));cell(tr,e.was_finite_mined?'Earlier finite candidate':'New symbolic discovery');
}else{
linked(tr,e.target);cell(tr,title(e.target));cell(tr,e.linear_combination.length);const td=cell(tr,'');const d=document.createElement('details');const s=document.createElement('summary');s.textContent='View exact rational coefficients';d.appendChild(s);const pre=document.createElement('code');pre.textContent=e.linear_combination.map(x=>`${x.coefficient} × ${x.source}`).join(' + ')||'0';d.appendChild(pre);td.appendChild(d);
}root.appendChild(tr);}
$('tableHeader').replaceChildren();for(const t of(active==='edges'?['Source','Target','Operator','Parameters','Discovery']:['Target','OEIS title','Basis terms','Projection']))cell($('tableHeader'),t,'th');
$('operatorLabel').classList.toggle('hidden',active!=='edges');
}
$('query').addEventListener('input',()=>{currentPage=0;render()});$('operation').addEventListener('change',()=>{currentPage=0;render()});
$('previous').addEventListener('click',()=>{if(currentPage>0)currentPage--;render()});$('next').addEventListener('click',()=>{currentPage++;render()});
for(const b of document.querySelectorAll('[data-tab]'))b.addEventListener('click',()=>{active=b.dataset.tab;currentPage=0;for(const x of document.querySelectorAll('[data-tab]'))x.setAttribute('aria-selected',String(x===b));render()});
$('basisIntro').textContent=`${basis.basis_rank} source formula sequences span ${basis.source_count.toLocaleString()} normalized OEIS formula sequences (exact rank over rational coefficients). Every row has a reconstructed all-index projection.`;
$('basisDetail').textContent=basis.basis_sequences.map((id,i)=>`${String(i+1).padStart(3,' ')}. ${id} — ${title(id)}`).join('\n');
render();
'''


def build(db,links,basis_rows,basis_summary,output):
    edges=[json.loads(s) for s in Path(links).read_text(encoding='utf-8').splitlines() if s.strip()]
    projections=[json.loads(s) for s in Path(basis_rows).read_text(encoding='utf-8').splitlines() if s.strip()]
    basis=json.loads(Path(basis_summary).read_text(encoding='utf-8'))
    wanted={v for e in edges for v in (e['source'],e['target'])}
    wanted.update(p['target'] for p in projections)
    wanted.update(x['source'] for p in projections for x in p['linear_combination'])
    names={sid:name for sid,name in db.execute('SELECT oeis_id,name FROM sequences') if sid in wanted}
    op_names=sorted({e['operator'] for e in edges})
    payload=json.dumps({'edges':edges,'projections':projections,'names':names,'basis':basis},ensure_ascii=False,separators=(',',':'))
    payload=payload.replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    opts=''.join('<option value="'+html.escape(o,quote=True)+'">'+html.escape(o)+'</option>' for o in op_names)
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi OEIS Formula Transfers v0.8</title><style>{CSS}</style></head><body><main>
    <small>AUTHOR: KOMOREBI P. · 22 NOVEMBER 2026 · ATTRIBUTION: OEIS FOUNDATION INC. (CC BY-SA 4.0)</small>
    <h1>OEIS Formula Transfer Atlas</h1><p class="intro">Exact algebraic transfers among the admitted formula expressions. Search by OEIS ID, name, operator, or basis source. No unreviewed OEIS program text is executed.</p>
    <div class="metrics"><div class="metric"><b>{len(edges):,}</b><small>Exact symbolic edges</small></div><div class="metric"><b>{sum(not e['was_finite_mined'] for e in edges):,}</b><small>New beyond prefix matching</small></div><div class="metric"><b>{basis['basis_rank']:,}</b><small>Basis sequences</small></div><div class="metric"><b>{len(projections):,}</b><small>Exact basis projections</small></div></div>
    <p class="notice"><strong>Proof scope.</strong> Every displayed identity holds for the supplied formula definitions at all local indices. The correspondence with the full infinite OEIS entry is still supported by finite source-term checks, not an independent global proof. The graph does not claim faster runtime for every path.</p>
    <nav class="tabs" aria-label="Atlas section"><button data-tab="edges" aria-selected="true">Transfer network</button><button data-tab="basis" aria-selected="false">Shared basis</button></nav>
    <h2>Search and filter</h2><div class="controls"><label>OEIS ID, name or operator<input id="query" type="search" placeholder="e.g. A000079, powers of 2, polyphase" autocomplete="off"></label><label id="operationLabel">Operator<select id="operation"><option value="">All operations</option>{opts}</select></label></div>
    <div class="toolbar"><span id="resultCount" aria-live="polite"></span><button id="previous" type="button">Previous</button><span id="pageLabel"></span><button id="next" type="button">Next</button></div>
    <div class="tablebox"><table aria-label="Verified formula transfers and basis projections"><thead><tr id="tableHeader"></tr></thead><tbody id="tableBody"></tbody></table></div>
    <h2>Basis construction</h2><p id="basisIntro"></p><details><summary>Show all {basis['basis_rank']} basis sequence identifiers</summary><pre id="basisDetail"></pre></details>
    <h2>Reproduction and attribution</h2><p>Source data: <a href="https://oeis.org/">OEIS Foundation</a> and <a href="https://github.com/oeis/oeisdata">official oeisdata repository</a>. Symbolic proof certificates, the exact rational projections, the source snapshot hash, and the Python tests are provided alongside this browser in the v0.8 release.</p>
    </main><script id="dataPayload" type="application/json">{payload}</script><script>{JS}</script></body></html>'''
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(page,encoding='utf-8')
    return {'edges':len(edges),'basis_projections':len(projections),'basis_rank':basis['basis_rank'],'bytes':output.stat().st_size}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--links',type=Path,required=True)
    p.add_argument('--basis',type=Path,required=True)
    p.add_argument('--basis-summary',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:print(json.dumps(build(db,args.links,args.basis,args.basis_summary,args.output),indent=2))
if __name__=='__main__':main()
