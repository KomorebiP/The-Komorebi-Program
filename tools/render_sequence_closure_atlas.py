"""Portable local browse/search interface for exact transfer closure certificates.

Author: Komorebi P. No network, runtime eval, or third-party scripts.
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import sqlite3


def build(db,closure_path,sparse_path,output):
    names={sid:name for sid,name in db.execute('SELECT oeis_id,name FROM sequences')}
    closure=[json.loads(s) for s in Path(closure_path).read_text(encoding='utf-8').splitlines() if s.strip()]
    sparse=[json.loads(s) for s in Path(sparse_path).read_text(encoding='utf-8').splitlines() if s.strip()]
    items=[]
    for x in closure:
        matches=[m for m in x['matches'] if m['oeis_id']!='A000004']
        if x['operator'] in ('cauchy_product','hadamard_product') and not matches:
            # Keep the exact output recurrence even when no named target matches.
            pass
        items.append({'type':x['operator'],'inputs':x['inputs'],
           'name':' + '.join(names.get(s,s)[:55] for s in x['inputs']),
           'recurrence':x['certificate']['coefficients'],
           'initial':x['certificate']['initial'][:8],
           'matches':matches[:10], 'more_matches':max(0,len(matches)-10),
           'proof':x['certificate']['proof'],
           'scope':x['certificate']['scope']})
    for x in sparse:
        p=x['lift']
        items.append({'type':'sparse_polyphase','inputs':[x['source_oeis_id']],
           'name':names.get(x['source_oeis_id'],x['source_oeis_id'])[:75],
           'recurrence':x['recurrence'],'initial':x['initial'][:8],
           'phase':p['modulus'],'poly':p['polynomial'],
           'support':p['support'],'matches':[], 'proof':p['proof'],
           'scope':x['scope']})
    items.sort(key=lambda x:(x['type'] not in ('binomial','sparse_polyphase'),
                             not bool(x['matches']),len(x['recurrence']),x['inputs']))
    payload=json.dumps(items,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi · Exact Sequence Transfer Compiler</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark}
*{box-sizing:border-box}body{margin:0;line-height:1.55;background:light-dark(#f7f8fa,#10151b);color:light-dark(#152131,#e8edf5)}
main{max-width:1150px;margin:auto;padding:26px 18px 64px}header{padding:12px 0 22px;border-bottom:1px solid light-dark(#cbd4dd,#394454)}
h1{font-size:clamp(1.45rem,2.5vw,2.2rem);line-height:1.25;letter-spacing:-.025em;margin:.2em 0}
p{max-width:82ch}.meta{color:light-dark(#4b6279,#bac8d8);font-size:.94rem}
.metrics{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.metric{border:1px solid light-dark(#c7d3de,#445265);border-radius:10px;padding:10px 16px;min-width:145px}
.metric b{font-size:1.4rem;display:block}.tools{display:flex;gap:10px;flex-wrap:wrap;padding:14px 0}
input,select{font:inherit;border:1px solid light-dark(#b4c0cc,#536479);border-radius:8px;padding:10px 12px;background:light-dark(#fff,#18212b);color:inherit;max-width:100%}
input{flex:1;min-width:210px}select{min-width:150px}
#results{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:12px}
article{border:1px solid light-dark(#cad5df,#3b4b5c);border-radius:11px;background:light-dark(white,#16202a);padding:16px;overflow-wrap:anywhere}
article h3{font-size:1.02rem;line-height:1.4;margin:.4rem 0}.tag{display:inline-block;font-size:.8rem;font-weight:650;padding:3px 7px;border:1px solid light-dark(#c5d1dd,#4c5e73);border-radius:6px}
code{font-family:ui-monospace,Consolas,monospace;font-size:.9em;white-space:normal}pre{margin:10px 0;padding:9px;border-radius:6px;overflow:auto;background:light-dark(#f0f4f7,#0d1722)}
a{color:light-dark(#245b95,#a4cdf7)}.notice{border-left:3px solid light-dark(#72869a,#94a8bd);padding:8px 12px;margin:18px 0}
small{opacity:.85}button{font:inherit;border:1px solid gray;border-radius:7px;background:none;color:inherit;padding:7px 10px;cursor:pointer}
footer{margin-top:28px;border-top:1px solid light-dark(#ddd,#444);padding-top:12px;font-size:.85rem}
</style></head><body><main><header><div class="meta">KOMOREBI P. · SEQUENCE RESEARCH</div>
<h1>Exact sequence transfer compiler</h1>
<p>Search algebraically certified binomial, product, convolution and sparse-polyphase transfers. Every global proof concerns the stored recurrence <em>definition</em>. Connections to OEIS entries were checked only on finite terms.</p></header>
<div class="metrics"><div class="metric"><b id="all">—</b><small>Operator certificates</small></div>
<div class="metric"><b id="shown">—</b><small>Visible results</small></div><div class="metric"><b id="kinds">—</b><small>Transfer types</small></div></div>
<div class="notice"><strong>Proof boundary:</strong> A globally proved transfer among declared formula definitions does not establish that every term in the corresponding OEIS entry follows that formula. Raw OEIS mentions and finite matches are not proofs.</div>
<div class="tools"><input id="search" type="search" placeholder="Search OEIS ID, recurrence, transfer or name" aria-label="Search exact transfer certificates">
<select id="kind" aria-label="Filter operator"><option value="">All operators</option></select>
<select id="limit" aria-label="Results per page"><option value="40">40 results</option><option value="100">100 results</option><option value="250">250 results</option></select></div>
<p class="meta" id="info" aria-live="polite"></p><section id="results" aria-label="Transfer certificates"></section>
<footer><strong>Author: Komorebi P.</strong> • OEIS reference names © OEIS Foundation Inc., CC BY-SA 4.0 • All source links point to the official entry. No source code from OEIS is executed.</footer>
</main><script>
const ROWS=__PAYLOAD__;
const Q=document.getElementById('search'),K=document.getElementById('kind'),L=document.getElementById('limit'),O=document.getElementById('results');
const kinds=[...new Set(ROWS.map(x=>x.type))].sort();
for(const kind of kinds){const option=document.createElement('option');option.value=kind;option.textContent=kind.replaceAll('_',' ');K.appendChild(option)}
document.getElementById('all').textContent=ROWS.length.toLocaleString();document.getElementById('kinds').textContent=kinds.length;
function line(tag,text){const node=document.createElement(tag);node.textContent=text;return node}
function render(){const query=Q.value.trim().toLowerCase(),kind=K.value,limit=+L.value;
 const found=ROWS.filter(x=>(!kind||x.type===kind)&&(!query||[x.type,x.name,x.inputs.join(' '),x.recurrence.join(','),JSON.stringify(x.matches),x.poly?.join(',')||''].join(' ').toLowerCase().includes(query)));
 document.getElementById('shown').textContent=Math.min(found.length,limit).toLocaleString();
 document.getElementById('info').textContent=`${found.length.toLocaleString()} matched, displaying ${Math.min(found.length,limit)}. These are exact operator certificates, not separate claims of novel theorems.`;
 O.replaceChildren();for(const entry of found.slice(0,limit)){
  const card=document.createElement('article');card.appendChild(line('span',entry.type.replaceAll('_',' ').toUpperCase()));card.lastChild.className='tag';
  card.appendChild(line('h3',entry.inputs.join(' + ')));
  const name=line('p',entry.name);name.className='meta';card.appendChild(name);
  const rec=line('pre',`Recurrence: ${JSON.stringify(entry.recurrence)}\nInitial: ${JSON.stringify(entry.initial)}`);card.appendChild(rec);
  if(entry.phase){card.appendChild(line('p',`Polyphase m=${entry.phase}, X^m mod P(X) = ${JSON.stringify(entry.poly)} (ascending coefficients)`))}
  if(entry.matches.length){card.appendChild(line('p','All-index definition matches:'));
   const ul=document.createElement('ul');for(const match of entry.matches){const li=document.createElement('li');const a=document.createElement('a');a.href='https://oeis.org/'+match.oeis_id;a.textContent=match.oeis_id;li.appendChild(a);li.appendChild(document.createTextNode(` · phase (${match.modulus},${match.residue})`));ul.appendChild(li)}card.appendChild(ul)
  }else{card.appendChild(line('p','No named target identified in the compiled phase catalog'))}
  const details=document.createElement('details');details.appendChild(line('summary','Proof construction and scope'));
  details.appendChild(line('p',entry.proof));details.appendChild(line('small',entry.scope));card.appendChild(details);O.appendChild(card)
 }}
Q.addEventListener('input',render);K.addEventListener('change',render);L.addEventListener('change',render);render();
</script></body></html>'''.replace('__PAYLOAD__',payload)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(page,encoding='utf-8')
    return {'operator_certificates':len(closure),'sparse_lifts':len(sparse),
            'display_records':len(items),'bytes':output.stat().st_size,'output':str(output)}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--closure',type=Path,required=True)
    p.add_argument('--sparse',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    with sqlite3.connect(a.db) as db:r=build(db,a.closure,a.sparse,a.output)
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
