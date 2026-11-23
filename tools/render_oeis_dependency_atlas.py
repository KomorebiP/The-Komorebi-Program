"""Offline formula-reference hypergraph browser; no dynamic code or network scripts.

Author: Komorebi P. Clear evidence labels distinguish text, finite checks,
and proved all-index identities (the latter are NOT claimed here).
"""
import argparse,html,json,sqlite3
from pathlib import Path
from render_oeis_v08_atlas import CSS

JS=r'''
const data=JSON.parse(document.getElementById('dataPayload').textContent);
const rows=data.rows,names=data.names;
const $=id=>document.getElementById(id);
const label=id=>id+' '+(names[id]||'');
const make=(parent,tag,text)=>{const a=document.createElement(tag);a.textContent=text;parent.appendChild(a);return a;};
let page=0;const pageSize=120;
function oeis(tr,id){const td=make(tr,'td','');const a=make(td,'a',id);a.href='https://oeis.org/'+id;a.rel='noopener noreferrer';a.target='_blank';return td;}
function filtered(){const q=$('query').value.trim().toLowerCase(),kind=$('evidence').value,multi=$('multi').checked;
return rows.filter(r=>(!kind||r.status===kind)&&(!multi||r.references.length>1)&&(!q||[r.source,label(r.source),...r.references.flatMap(x=>[x,label(x)]),r.rhs||''].join(' ').toLowerCase().includes(q)));}
function render(){const f=filtered(),root=$('bodyRows');root.replaceChildren();page=Math.min(page,Math.max(0,Math.ceil(f.length/pageSize)-1));const slice=f.slice(page*pageSize,(page+1)*pageSize);
for(const x of slice){const tr=make(root,'tr','');oeis(tr,x.source);const refs=make(tr,'td','');for(const [j,id] of x.references.entries()){if(j>0)make(refs,'span',' · ');const a=make(refs,'a',id);a.href='https://oeis.org/'+id;a.target='_blank';a.rel='noopener noreferrer';}
make(tr,'td',x.status==='algebraic_formula_proved'?'Exact formula identity':x.status==='finite_checked_formula_hyperedge'?'Finite term match':x.status==='textual_dependency_unverified'?'Textual reference only':x.status==='parsed_but_out_of_corpus'?'Unresolved references':'Not verified');make(tr,'td',String(x.checked_terms));const td=make(tr,'td','');if(x.rhs){const code=make(td,'code',x.rhs);code.style.whiteSpace='pre-wrap';}else make(td,'small','Raw formula dependency; open OEIS source to review context.');}
$('count').textContent=`${f.length.toLocaleString()} source formula lines`;
$('pageLabel').textContent=`Page ${page+1} of ${Math.max(1,Math.ceil(f.length/pageSize))}`;
$('previous').disabled=page===0;$('next').disabled=(page+1)*pageSize>=f.length;
}
for(const id of ['query','evidence','multi'])$(id).addEventListener('input',()=>{page=0;render()});
$('previous').addEventListener('click',()=>{page--;render()});$('next').addEventListener('click',()=>{page++;render()});render();
'''


def build(database, source, summary, output, proofs=None):
    stats=json.loads(Path(summary).read_text(encoding='utf8'))
    data=[json.loads(line) for line in Path(source).read_text(encoding='utf8').splitlines() if line.strip()]
    proof_ids={json.loads(line)['formula_id'] for line in Path(proofs).read_text(encoding='utf8').splitlines() if line.strip()} if proofs else set()
    rows=[{'source':x['oeis_id'],'references':x['references'],'status':'algebraic_formula_proved' if x.get('formula_id') in proof_ids else x['status'],'checked_terms':x['checked_terms'],'rhs':x['candidate_rhs'],'source_sha256':x['source_text_sha256']} for x in data]
    wanted={x['source'] for x in rows};wanted.update(r for x in rows for r in x['references'])
    names={sid:name for sid,name in database.execute('SELECT oeis_id,name FROM sequences') if sid in wanted}
    payload=json.dumps({'rows':rows,'names':names,'stats':stats},ensure_ascii=False,separators=(',',':'))
    payload=payload.replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Komorebi OEIS Formula Dependency Atlas</title><style>{CSS}</style></head><body><main>
    <small>AUTHOR: KOMOREBI P. · 22 NOVEMBER 2026 · DATA: OEIS FOUNDATION INC. CC BY-SA 4.0</small><h1>OEIS Formula Dependency Hypergraph</h1>
    <p class="intro">Explore dependencies mentioned in OEIS formula lines. Some lines reference multiple sequences; those are multi-input hyperedges, not necessarily true algebraic identities.</p>
    <div class="metrics"><div class="metric"><b>{len(rows):,}</b><small>Referenced formula lines</small></div><div class="metric"><b>{stats['reference_occurrences']:,}</b><small>OEIS ID occurrences</small></div><div class="metric"><b>{stats['multi_input_lines']:,}</b><small>Multi-ID formula lines</small></div><div class="metric"><b>{stats['finite_checked_lines']:,}</b><small>Finite-checked expression links</small></div><div class="metric"><b>{len(proof_ids):,}</b><small>All-index formula identities (conditional)</small></div></div>
    <p class="notice"><strong>Evidence boundary.</strong> Textual mentions are not transfer identities. Finite checks establish agreement only at the stated stored indices. An algebraically certified relation is proved between exact formula definitions for all indices, but full OEIS identification remains finite-checked. Formula text is parsed with a restricted arithmetic grammar, not executed as source code.</p>
    <div class="controls"><label>Search sequence IDs, names or formula<input type="search" id="query" placeholder="A000045 or Fibonacci" autocomplete="off"></label><label>Evidence<select id="evidence"><option value="">All</option><option value="algebraic_formula_proved">All-index formula proof</option><option value="finite_checked_formula_hyperedge">Finite-checked only</option><option value="textual_dependency_unverified">Textual only</option><option value="parsed_but_unverified">Parsed but not verified</option><option value="parsed_but_out_of_corpus">Outside imported corpus</option></select></label><label style="max-width:180px;align-self:end;display:block"><input id="multi" type="checkbox" style="width:auto"> Multiple referenced IDs</label></div>
    <div class="toolbar"><span id="count" aria-live="polite"></span><button id="previous" type="button">Previous</button><span id="pageLabel"></span><button id="next" type="button">Next</button></div>
    <div class="tablebox"><table><thead><tr><th>OEIS formula entry</th><th>Referenced sequences</th><th>Evidence class</th><th>Exact terms checked</th><th>Restricted RHS, when recognized</th></tr></thead><tbody id="bodyRows"></tbody></table></div>
    <p>Source: <a href="https://oeis.org/">OEIS Foundation</a>. Original formula text remains in the attributed SQLite source snapshot; this index preserves formula SHA-256 receipts in its embedded data.</p>
    </main><script id="dataPayload" type="application/json">{payload}</script><script>{JS}</script></body></html>'''
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(page,encoding='utf8')
    return dict(rows=len(rows),finite_checked=stats['finite_checked_lines'],multi_input=stats['multi_input_lines'],proved_formula_hyperedges=len(proof_ids),bytes=output.stat().st_size)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['db','source','summary','output']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--proofs',type=Path)
    args=p.parse_args(argv)
    with sqlite3.connect(args.db) as db:
        print(json.dumps(build(db,args.source,args.summary,args.output,args.proofs),indent=2))
if __name__=='__main__':main()
