"""Export a self-contained read-only HTML browser for finitely checked OEIS formulas."""
import argparse
import html
import json
import sqlite3
from pathlib import Path

STYLE = '''
:root{color-scheme:light dark;font-family:system-ui,-apple-system,Segoe UI,sans-serif}
body{max-width:1100px;margin:0 auto;padding:30px 24px;line-height:1.6}
header{border-bottom:1px solid #8886;margin-bottom:24px;padding-bottom:16px}
h1{font-size:clamp(1.6rem,4vw,2.6rem);line-height:1.2}
a{color:inherit;text-decoration:underline;text-underline-offset:3px}
.controls{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}
input,select{font:inherit;padding:10px 12px;border:1px solid #7779;border-radius:8px;min-width:180px;background:transparent;color:inherit}
input{flex:1}output{font-weight:600}.entry{padding:14px 20px;border:1px solid #8886;border-radius:10px;margin:12px 0}
.entry h2{font-size:1.1rem;margin:.2rem 0}.entry p{margin:.2rem 0}.formula{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.45;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.93rem;margin-top:8px;padding:12px;background:Canvas;color:CanvasText;border-left:3px solid currentColor}
small,.meta{opacity:.8}.empty{padding:30px 0}button{font:inherit;border:1px solid;border-radius:7px;padding:5px 10px;background:transparent;color:inherit;cursor:pointer}
'''


def build(db_path, out_path):
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute('''SELECT s.oeis_id,s.name,s.offset,f.kind,f.expression,
            f.verification,f.checked_terms,f.complexity,f.source_url
            FROM formulas f JOIN sequences s ON s.oeis_id=f.oeis_id
            WHERE f.verification='finite_checked' ORDER BY s.oeis_id,f.ordinal''').fetchall()
    data = [dict(r) for r in rows]
    payload = json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Komorebi OEIS Formula Catalogue</title><style>''' + STYLE + '''</style></head><body>
<header><h1>Komorebi OEIS Formula Catalogue</h1><p>Exact evaluator collection. Only finite prefix-checked formulas appear here. Finite checks are not proofs of infinite identities.</p><small>OEIS Foundation Inc. · <a href="https://oeis.org/">OEIS</a> · OEIS-derived data CC BY-SA 4.0 · Author: Komorebi P.</small></header>
<div class="controls"><label for="q">Search <input id="q" type="search" placeholder="OEIS ID, name, formula…"></label><label for="kind">Representation <select id="kind"><option value="">All formula classes</option></select></label></div>
<p><output id="count" aria-live="polite"></output></p><main id="results" aria-label="Formula search results"></main>
<script>const data='''+payload+''';const input=document.getElementById('q'),kind=document.getElementById('kind'),results=document.getElementById('results'),count=document.getElementById('count');
for(const k of [...new Set(data.map(x=>x.kind))].sort()){const o=document.createElement('option');o.value=k;o.textContent=k.replaceAll('_',' ');kind.append(o)}
function tag(name,text){const x=document.createElement(name);x.textContent=text;return x}
function render(){const q=input.value.trim().toLowerCase(),k=kind.value;const selected=data.filter(x=>(!k||x.kind===k)&&(!q||[x.oeis_id,x.name,x.expression].some(t=>t.toLowerCase().includes(q))));count.textContent=selected.length+' of '+data.length+' finitely checked formulas';results.replaceChildren();for(const r of selected.slice(0,250)){const el=tag('article','');el.className='entry';const h=document.createElement('h2');const a=document.createElement('a');a.href='https://oeis.org/'+r.oeis_id;a.textContent=r.oeis_id+' · '+r.name;h.append(a);el.append(h);const meta=tag('p',r.kind.replaceAll('_',' ')+' · n begins at '+r.offset+' · '+r.checked_terms+' exact reference terms checked');meta.className='meta';el.append(meta);const pre=tag('div',r.expression);pre.className='formula';el.append(pre);if(r.complexity)el.append(tag('small','Computation: '+r.complexity));results.append(el)}if(selected.length>250)results.append(tag('p','Showing first 250; refine the search.'));if(!selected.length){const p=tag('p','No matching formulas in this local export.');p.className='empty';results.append(p)}}
input.addEventListener('input',render);kind.addEventListener('change',render);render();</script></body></html>'''
    Path(out_path).write_text(page,encoding='utf-8',newline='\n')
    return len(data)

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--db',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    print(json.dumps({'formulas':build(args.db,args.output),'path':args.output}))
