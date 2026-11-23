"""Render a self-contained, searchable exact gauge network atlas.

Author: Komorebi P. Formula-level proof evidence remains clearly scoped.
"""
from __future__ import annotations
import argparse,html,json
from pathlib import Path

CSS='''
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color-scheme:light dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);--bg:#fafbfc;--fg:#19212f;--panel:#fff;--border:#d6dce4;--muted:#536173;--accent:#1b648d}
@media(prefers-color-scheme:dark){body{--bg:#111820;--fg:#eaf0f6;--panel:#1a2632;--border:#3b4a5b;--muted:#b7c2ce;--accent:#80cbef}}
header,main,footer{max-width:1140px;margin:auto;padding:22px}header{padding-top:38px}h1{font-size:clamp(1.4rem,3vw,2rem);margin:0 0 .4rem}h2{font-size:1.15rem;margin:1.4rem 0 .65rem}
p{line-height:1.55}small,.muted{color:var(--muted)}code{overflow-wrap:anywhere}a{color:var(--accent)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.stat,.panel,.chart{border:1px solid var(--border);background:var(--panel);border-radius:12px;padding:16px}
.stat strong{font-size:1.8rem;display:block}.stat span{font-size:.8rem;color:var(--muted)}
.tools{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:16px 0}
input,select{background:var(--panel);color:var(--fg);border:1px solid var(--border);border-radius:7px;padding:9px;font:inherit}
input{flex:1;min-width:220px}select{min-width:130px}
ul.records{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:10px}
li.chart{min-width:0;line-height:1.55}li.chart strong{display:block;margin-bottom:5px}
.math{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.85rem;overflow-wrap:anywhere}
footer{border-top:1px solid var(--border);color:var(--muted);font-size:.88rem}button{background:var(--panel);color:var(--fg);border:1px solid var(--border);padding:8px 12px;border-radius:7px;cursor:pointer}
'''

def render(report,benchmark=None):
    s=report['summary'];charts=report['charts']
    items=[]
    for item in sorted(charts,key=lambda e:(e['root'],e['node'])):
        r,n=item['root'],item['node']
        factor=' × '.join(f"({f['a']}n{f['b']:+d})^{f['power']}" for f in item['gauge_linear_factors']) or '1'
        lhs=f'{n}(n) / {r}(n)'
        formula=f"K={item['base_ratio']}, c={item['exponential_factor']}, L(n)={factor}"
        items.append(f'<li class="chart" data-record="{html.escape((r+" "+n).lower())}"><strong><a href="https://oeis.org/{r}">{r}</a> → <a href="https://oeis.org/{n}">{n}</a></strong><div class="math">{html.escape(lhs)}</div><div class="math">{html.escape(formula)}</div><small>Steps in spanning tree: {item["steps"]} · all-index formula gauge</small></li>')
    benches=[]
    if benchmark:
        for w in benchmark.get('workloads',[]):
            m=w['measured'];v=m['observed_direct_to_shared_ratio']
            benches.append(f'<li><strong>{html.escape(w["name"])}</strong>: direct/shared timing ratio {v:.3f}×; measured winner: {html.escape(m["winner"])}; 5-run exact verification</li>')
    be='<section class="panel"><h2>Exact computational comparisons</h2><ul>'+''.join(benches)+'</ul><p class="muted">Reported ratios are specific to the tested computer and workload. The calibration cost is additional.</p></section>' if benches else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi — exact gauge transfer atlas</title><style>{CSS}</style></head>
<body><header><h1>Komorebi Exact Gauge Transfer Atlas</h1><p>Source-bound multiplicative transformations between formula definitions, with independent cycle-consistency checks. Author: Komorebi P.</p></header>
<main><section class="stats"><div class="stat"><strong>{s['connected_formula_models']}</strong><span>Formula models connected</span></div>
<div class="stat"><strong>{s['accepted_full_prefix_gauges']}</strong><span>Validated transfers</span></div><div class="stat"><strong>{s['component_count']}</strong><span>Connected components</span></div><div class="stat"><strong>{s['flat_cycles']}/{s['fundamental_cycles']}</strong><span>Fundamental cycles passing exact holonomy tests</span></div></section>
<section class="panel"><h2>What the audit proves</h2><p>Every accepted edge is re-derived from the current formula expressions, checked for nonsingular positive-index factors, and normalized at index zero. Every fundamental cycle has exact base multiplier 1 and exact rational step multiplier 1. Therefore all paths within a connected component are algebraically consistent for the admitted formula definitions.</p><p><strong>Not established:</strong> All-index identification of each OEIS entry, novelty, or lowest runtime across all possible algorithms. Source OEIS IDs were checked only to finite excerpt depth.</p></section>
{be}<section><h2>Canonical transfer charts</h2><div class="tools"><input id="query" aria-label="Search sequence IDs" placeholder="Search OEIS source or destination ID"><select id="size"><option value="all">All components</option><option value="short">1-step charts</option><option value="long">2+ steps</option></select><span id="count" aria-live="polite"></span></div><ul class="records" id="records">{''.join(items)}</ul></section></main><footer>OEIS © OEIS Foundation Inc. (CC BY-SA 4.0 for source data). Independent Komorebi visualization and exact formula audits. Published as an experimental proof-conditional research tool.</footer>
<script>const q=document.getElementById('query'),sel=document.getElementById('size'),items=[...document.querySelectorAll('.chart')];function update(){{let count=0;const val=q.value.toLowerCase().trim();for(const item of items){{const steps=Number((item.textContent.match(/Steps in spanning tree: (\\d+)/)||[])[1]);const show=item.dataset.record.includes(val)&&(sel.value==='all'||(sel.value==='short'?steps===1:steps>1));item.hidden=!show;if(show)count++;}}document.getElementById('count').textContent=count.toLocaleString()+' of '+items.length.toLocaleString()+' charts';}}q.addEventListener('input',update);sel.addEventListener('change',update);update();</script></body></html>'''

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--atlas',type=Path,required=True)
    p.add_argument('--benchmark',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    report=json.loads(a.atlas.read_text(encoding='utf8'))
    bench=json.loads(a.benchmark.read_text(encoding='utf8')) if a.benchmark else None
    out=render(report,bench)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(out,encoding='utf8')
    print(json.dumps({'charts':len(report['charts']),'html_bytes':len(out.encode()),'output':str(a.output)}))
if __name__=='__main__':main()
