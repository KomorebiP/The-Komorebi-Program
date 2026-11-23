"""Offline formula-transfer certificate index for Komorebi OEIS v1.0.

Author: Komorebi P. Reads generated certificate JSONL and source names;
does not execute, evaluate or interpret raw OEIS text as code.
"""
import argparse
import json
import sqlite3
from pathlib import Path
from collections import Counter


class RecordReader:
    def __init__(self,root):
        self.root=Path(root)
        self.records=[]
        self.stats=Counter()
        self.seen=set()

    def ingest(self,file,kind,mapper):
        path=self.root/'outputs'/file
        if not path.exists():return
        with path.open(encoding='utf8') as stream:
            for line in stream:
                if not line.strip():continue
                original=json.loads(line)
                record=mapper(original)
                if record is None:continue
                rec=dict(kind=kind,**record)
                key=(rec['kind'],rec['id'],rec.get('formula',''),rec.get('label',''))
                if key in self.seen:continue
                self.seen.add(key)
                self.records.append(rec)
                self.stats[kind]+=1


def render(db,root,output):
    reader=RecordReader(root)
    reader.ingest('holonomic-all-final.jsonl','P-recursive',lambda x:dict(
        id=x['oeis_id'],formula=x['formula_id'],label='order '+str(x['order']),
        summary=f"Exact order-{x['order']} recurrence from {x['component_count']} hypergeometric components",
        detail={'coefficients':x['operator_coefficients'],'mathematical_start':x['mathematical_start'],
                'checked_reference_positions':x['checked_oeis_recursion_positions']},
        proof='Exact rational-function nullspace; formula expression all indices on its tail'))
    reader.ingest('holonomic-extra.jsonl','Supplemental recurrence',lambda x:dict(
        id=x['oeis_id'],formula=x['formula_id'],label='order '+str(x['order']),
        summary='Recovered OEIS formula expression; exact recurrence',
        detail={'coefficients':x['operator_coefficients'],'mathematical_start':x['mathematical_start']},
        proof='Exact symbolic recurrence of a source-line-normalized expression'))
    reader.ingest('hypergeom-phases.jsonl','Pochhammer phase',lambda x:dict(
        id=x['oeis_id'],formula=x['formula_id'],label=f"mod {x['modulus']} / phase {x['residue']}",
        summary='Exact terminating-product/Pochhammer representation of a subsequence',
        detail={'base_value':x['base_value'],'modulus':x['modulus'],'residue':x['residue'],
                'pochhammer':x['pochhammer'],'hypergeometric_formal_OGF':x['hypergeometric_ogf']},
        proof='Multiplication of exact affine successive-term ratios'))
    reader.ingest('p-recursive-phases-200.jsonl','Higher-order phase',lambda x:dict(
        id=x['oeis_id'],formula=x['formula_id'],label=f"mod {x['modulus']} / phase {x['residue']}",
        summary=f"Exact phase recurrence of order {x['result_order']} from order {x['source_order']}",
        detail={'operator_coefficients':x['operator_coefficients'],
                'mathematical_base_start':x['mathematical_base_start'],
                'source_leader_sign':x['leader_sign']},
        proof='Exact rational companion matrix, nonsingular tail, symbolic cyclic-row nullspace'))
    reader.ingest('structured-gauges.jsonl','Direct transfer',lambda x:dict(
        id=x['source'],to=x['target'],formula=x['source_formula'],label=x['source']+' → '+x['target'],
        summary=f"Exact multiplicative gauge of support {x['support']}",
        detail={'base_ratio':x['base_ratio'],'exponential_factor':x['exponential_factor'],
                'factors':x['gauge_linear_factors'],'tail_start_local':x['tail_start_local']},
        proof='Exact equality of successive-term rational functions and nonzero initial ratio'))
    reader.ingest('composed-gauges.jsonl','Composed path',lambda x:dict(
        id=x['source'],to=x['target'],formula=x['source_formula'],
        label=x['source']+' → '+x['via']+' → '+x['target'],
        summary=f"Proof-carrying two-hop multiplicative transfer of support {x['support']}",
        detail={'via':x['via'],'base_ratio':x['base_ratio'],'exponential_factor':x['exponential_factor'],
                'factors':x['gauge_linear_factors'],'tail_start_local':x['tail_start_local'],
                'certificate_sha256':x['certificate_sha256']},
        proof='Both input gauge certificates regenerated; direct Q(t) composite identity verified'))
    reader.ingest('chain-anchors.jsonl','Source normalization',lambda x:dict(
        id=x['oeis_id'],formula=x['formula_id'],label=x.get('expression','source formula'),
        summary=f"Source expression recovered and exact-prefix checked ({x['checked_terms']} terms)",
        detail={'source_line_sha256':x['source_line_sha256'], 'checked_terms':x['checked_terms'],
                'verification':'finite_checked only'},
        proof='NO all-index OEIS identity asserted by finite source comparison'))
    with sqlite3.connect(db) as conn:
        ids=sorted({r['id'] for r in reader.records}|{r.get('to') for r in reader.records if r.get('to')})
        names={}
        for i in range(0,len(ids),800):
            chunk=ids[i:i+800]
            names.update(conn.execute('SELECT oeis_id,name FROM sequences WHERE oeis_id IN ('+','.join('?'*len(chunk))+')',chunk))
    for rec in reader.records:rec['name']=names.get(rec['id'],'')
    # Raw records may include benign Unicode and untrusted names. Put JSON in a
    # non-executable script tag and render only via DOM textContent.
    data={'records':reader.records,'counts':reader.stats,'version':'1.0',
          'claims':['Proof of exact symbolic expression identities, not automatically of OEIS identities',
                    'Finite source matches are distinct from all-index proofs',
                    'Formal OGF/hypergeometric identities need not converge analytically',
                    'No universal runtime speedup is implied']}
    packed=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Komorebi OEIS Transfer Atlas v1.0</title>
<style>
:root{color-scheme:dark;--background:#10151d;--panel:#1c2633;--line:#344255;--text:#eef4fb;--muted:#b8c8da;--accent:#96caff}
*{box-sizing:border-box}body{margin:0;background:var(--background);color:var(--text);font:15px/1.55 system-ui,-apple-system,sans-serif}
a{color:var(--accent)}.container{max-width:1340px;margin:auto;padding:22px}h1{font-size:clamp(24px,3vw,36px);line-height:1.15;margin:0 0 14px}h2{font-size:20px;margin:24px 0 10px}.subtitle,.minor{color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:20px 0}.stat{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}.stat strong{font-size:25px;display:block;font-variant-numeric:tabular-nums}.controls{display:grid;grid-template-columns:2fr 1fr auto;gap:10px;margin:20px 0}.controls input,.controls select,.route input{background:#253346;color:#fff;border:1px solid #718299;border-radius:8px;padding:12px;font:inherit;min-width:0}.controls button,.route button,.pager button{background:#354e6e;color:#fff;border:1px solid #7790ad;border-radius:7px;padding:10px 16px;cursor:pointer}button:hover{background:#456488}.route{display:flex;flex-wrap:wrap;gap:9px;align-items:center}.route input{width:125px}.route-output{min-height:25px;color:#d3e4f4}#records{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:12px}.entry{padding:13px;border:1px solid var(--line);border-radius:10px;background:var(--panel);min-width:0}.entry h3{font-size:16px;margin:0 0 7px;overflow-wrap:anywhere}.entry p{margin:5px 0}.entry small{color:#b5cbe0}details{margin-top:8px;border-top:1px solid var(--line);padding-top:7px}summary{cursor:pointer;color:var(--accent)}pre{white-space:pre-wrap;word-break:break-word;font:12px/1.4 ui-monospace,Consolas,monospace;background:#0e1823;padding:10px;border-radius:7px;max-height:260px;overflow:auto}.pager{display:flex;align-items:center;justify-content:space-between;margin:18px 0}.note{border-left:3px solid #7398bd;padding:10px 13px;background:var(--panel);color:var(--muted);margin:15px 0}#shown{font-variant-numeric:tabular-nums}.id{font-family:ui-monospace,monospace}footer{color:#afc0d1;margin-top:35px}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #a1c7f4;outline-offset:2px}@media(max-width:650px){.controls{grid-template-columns:1fr}.container{padding:14px}}
</style></head><body><main class="container">
<h1>Komorebi OEIS Formula Transfer Atlas <small style="color:#adc7df;font-size:.45em">v1.0</small></h1>
<p class="subtitle">Author: Komorebi P. · Exact algebra over extracted source formulas · Offline search and route inspection</p>
<p class="note">A symbolic all-index certificate establishes a relation between the <b>mathematical formula expressions</b> shown. It does not by itself prove that the entire OEIS sequence equals the extracted formula. Raw and finite-checked expressions are a separate category. No source program text is executed.</p>
<div class="stats" id="stats"></div>
<section><h2>Find a verified formula route</h2><div class="route"><label for="start">Source</label><input id="start" value="A000108" placeholder="A000108" maxlength="7"/><label for="end">Target</label><input id="end" value="A002544" placeholder="A002544" maxlength="7"/><button id="routeBtn">Find route</button></div><p class="route-output" id="routeResult" aria-live="polite"></p><p class="minor">Routes use all-index algebraic gauge edges between admitted formula definitions, not numeric prefix matches or guaranteed speedups.</p></section>
<section><h2>Browse certificates</h2><div class="controls"><input id="search" type="search" placeholder="Search A000108, Catalan, recurrence, modulus, formula ID…" aria-label="Search"/><select id="kind" aria-label="Certificate type"><option value="">All certificate types</option></select><button id="clear">Clear search</button></div><p id="shown" class="minor" aria-live="polite"></p><div id="records"></div><nav class="pager"><button id="prev">Previous</button><span id="pageText"></span><button id="next">Next</button></nav></section>
<footer>OEIS references and source excerpts: <a href="https://oeis.org/">OEIS Foundation Inc.</a>, CC BY-SA 4.0. Derived code and algebra: Komorebi P. Proof ledgers and source checksums are distributed beside this atlas. This page is self-contained and does not upload searches.</footer></main>
<script id="data" type="application/json">__DATA__</script>
<script>
(()=>{'use strict';const raw=JSON.parse(document.getElementById('data').textContent);const data=raw.records;const cats=Object.keys(raw.counts).sort();const stats=document.getElementById('stats');
for(const [key,val] of [['Imported source records','99,999'],['Exact recurrence ledgers',(raw.counts['P-recursive']||0)+(raw.counts['Supplemental recurrence']||0)],['First-order phase expressions',raw.counts['Pochhammer phase']||0],['Higher-order phase certificates',raw.counts['Higher-order phase']||0],['Direct gauge transfers',raw.counts['Direct transfer']||0],['Composed paths',raw.counts['Composed path']||0]]){const box=document.createElement('div');box.className='stat';const v=document.createElement('strong');v.textContent=typeof val==='number'?val.toLocaleString():val;const n=document.createElement('span');n.className='minor';n.textContent=key;box.append(v,n);stats.append(box)}
const kind=document.getElementById('kind');for(const k of cats){const o=document.createElement('option');o.value=k;o.textContent=k+' ('+raw.counts[k].toLocaleString()+')';kind.append(o)}
const search=document.getElementById('search');let results=data,offset=0;const pageSize=90;
const searchable=r=>[r.id,r.to,r.name,r.kind,r.label,r.summary,r.formula].join(' ').toLowerCase();
function filter(){const terms=search.value.trim().toLowerCase().split(/\\s+/).filter(Boolean);results=data.filter(r=>(!kind.value||r.kind===kind.value)&&terms.every(t=>searchable(r).includes(t)));offset=0;render()}
function node(tag,content,cls){const e=document.createElement(tag);if(cls)e.className=cls;e.textContent=content;return e}
function render(){const area=document.getElementById('records');area.replaceChildren();for(const r of results.slice(offset,offset+pageSize)){
const card=node('article','','entry');const header=node('h3','');const href=document.createElement('a');href.href='https://oeis.org/'+encodeURIComponent(r.id);href.textContent=r.id;href.target='_blank';href.rel='noopener noreferrer';header.append(href,document.createTextNode(' · '+r.kind));
card.append(header,node('p',r.name||'', 'minor'),node('p',r.summary||''),node('small',r.label||''));
const d=document.createElement('details');d.append(node('summary','View exact certificate data'),node('p',r.proof||'', 'minor'),node('pre',JSON.stringify(r.detail,null,2)));card.append(d);area.append(card)}
document.getElementById('shown').textContent=results.length.toLocaleString()+' records found, showing '+(results.length?offset+1:0)+'–'+Math.min(offset+pageSize,results.length);document.getElementById('pageText').textContent='Page '+(1+Math.floor(offset/pageSize))+' of '+Math.max(1,Math.ceil(results.length/pageSize));document.getElementById('prev').disabled=offset===0;document.getElementById('next').disabled=offset+pageSize>=results.length}
search.addEventListener('input',filter);kind.addEventListener('change',filter);document.getElementById('clear').onclick=()=>{search.value='';kind.value='';filter()};document.getElementById('prev').onclick=()=>{offset=Math.max(0,offset-pageSize);render()};document.getElementById('next').onclick=()=>{offset=Math.min((Math.ceil(results.length/pageSize)-1)*pageSize,offset+pageSize);render()};
const graph=new Map();for(const r of data.filter(x=>x.kind==='Direct transfer'||x.kind==='Composed path')){if(!r.to)continue;(graph.get(r.id)||graph.set(r.id,[]).get(r.id)).push(r.to);(graph.get(r.to)||graph.set(r.to,[]).get(r.to)).push(r.id)}
function route(){const a=document.getElementById('start').value.trim().toUpperCase(),b=document.getElementById('end').value.trim().toUpperCase(),out=document.getElementById('routeResult');if(!/^A\\d{6}$/.test(a)||!/^A\\d{6}$/.test(b)){out.textContent='Enter two complete OEIS IDs such as A000108.';return}const q=[[a]],seen=new Set([a]);let found=null;while(q.length){const p=q.shift();const u=p[p.length-1];if(u===b){found=p;break}if(p.length>=5)continue;for(const v of graph.get(u)||[]){if(!seen.has(v)){seen.add(v);q.push([...p,v])}}}out.textContent=found?'Algebraic gauge route: '+found.join(' → '):'No algebraically certified route found within four edges in this release.'}
document.getElementById('routeBtn').onclick=route;filter();route();
})();
</script></body></html>'''
    html=html.replace('__DATA__',packed)
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(html,encoding='utf8')
    return {'records':len(reader.records),'categories':dict(reader.stats),'bytes':out.stat().st_size,'html':str(out)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--db',required=True,type=Path)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();print(json.dumps(render(a.db,a.root,a.output),indent=2))
if __name__=='__main__':main()
