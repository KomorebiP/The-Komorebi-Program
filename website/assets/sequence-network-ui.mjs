/** Read-only OEIS transfer graph. Never executes source expressions. */
const OEIS = /^A\d{6}$/;
const MAX_RESULTS = 60;
const EVIDENCE = Object.freeze({
  all_index_formula_identity: 'Algebraic identity of extracted formula expressions',
  all_index_formula_identity_on_tail: 'Algebraic formula identity on the stated nonsingular tail',
  conditional_exact_ogf_identity: 'Exact formal OGF transform, conditional on the recorded premises',
  exact_quadratic_algebra: 'Exact quadratic-channel algebra for the stated definitions',
});
const KIND = Object.freeze({hyperedge:'Formula identity',gauge:'Gauge transfer',riordan:'Riordan transform',quadratic:'Quadratic channel'});

export function networkSearch(data, rawQuery, category='all', limit=MAX_RESULTS, localMatches={}) {
  const q=String(rawQuery??'').trim().slice(0,200);
  const key=q.toLocaleLowerCase();
  if (!key) return {total:0, results:[], localLeads:[], resolved:[]};
  const localLeads=(localMatches[q] || localMatches[q.toUpperCase()] || []).filter(x=>OEIS.test(x.id));
  const matching=new Set(localLeads.map(x=>x.id));
  for(const record of data.records || []) {
    if(record.id.toLowerCase()===key || record.name.toLocaleLowerCase().includes(key)) matching.add(record.id);
  }
  const candidates=[];
  for(const edge of data.edges || []) {
    if(category!=='all' && edge.kind!==category) continue;
    const incident=[edge.target,...edge.inputs];
    if(incident.some(id=>matching.has(id)) || (!matching.size && (
        String(edge.expression).toLocaleLowerCase().includes(key) ||
        String(edge.kind).toLocaleLowerCase().includes(key)))) candidates.push(edge);
  }
  const exact=q.toUpperCase();
  candidates.sort((a,b)=>{
    const score=e=> e.target===exact?0:e.inputs.includes(exact)?1:e.kind==='hyperedge'?2:e.kind==='gauge'?3:4;
    return score(a)-score(b) || a.key.localeCompare(b.key);
  });
  return {total:candidates.length,results:candidates.slice(0,Math.max(0,Math.min(limit,200))),localLeads,resolved:[...matching].sort()};
}

export function networkLink(value) {
  const id=String(value??'').trim();
  if(!/^[A-Za-z][A-Za-z0-9_:-]{0,100}$/.test(id)) return 'sequence-network.html';
  return 'sequence-network.html?q='+encodeURIComponent(id)+'#sequence-network';
}

function node(tag, value, className) {
  const el=document.createElement(tag);
  if (value!==undefined) el.textContent=String(value);
  if (className) el.className=className;
  return el;
}
function officialLink(id, label) {
  const a=node('a',label || id);
  a.href=OEIS.test(id)?'https://oeis.org/'+id:'sequence-library.html';
  return a;
}
function siteSearchLink(id) {
  const a=node('a','Search the local Sequence Library');
  a.href='sequence-library.html?q='+encodeURIComponent('oeis:'+id)+'#library-search';
  return a;
}
function explainEdge(edge, names) {
  const li=node('li',undefined,'sn-result');
  const kind=node('span',KIND[edge.kind] || 'Formula connection','sn-rel-kind');
  const heading=node('h3');heading.append(kind,officialLink(edge.target),document.createTextNode(' ← '));
  edge.inputs.forEach((input,i)=>{if(i)heading.append(document.createTextNode(' + '));heading.append(officialLink(input));});
  li.append(heading);
  const detail=[edge.target,...edge.inputs].map(id=>`${id}: ${names.get(id) || 'OEIS sequence'}`).join(' · ');
  li.append(node('p',detail,'sn-details'));
  li.append(node('p',edge.expression,'sn-statement'));
  li.append(node('p',EVIDENCE[edge.evidence] || 'Unclassified evidence','sn-evidence'));
  li.append(node('p','Domain: '+edge.domain,'sn-details'));
  if(edge.kind==='hyperedge' && Object.keys(edge.index_maps || {}).length){
    li.append(node('p','Index maps: '+Object.entries(edge.index_maps).map(([id,ranges])=>
      id+': '+ranges.map(pair=>'n ↦ '+pair[0]+'n'+(pair[1]>=0?'+':'')+pair[1]).join(', ')).join(' · '),'sn-details'));
  }
  const controls=node('div',undefined,'sn-actions');
  controls.append(officialLink(edge.target,'View target on OEIS'),siteSearchLink(edge.target));
  li.append(controls);
  return li;
}
async function mount() {
  const root=document.querySelector('[data-sequence-network]');
  if(!root) return;
  const input=root.querySelector('#sn-query'), filter=root.querySelector('#sn-filter'),
        status=root.querySelector('#sn-status'), results=root.querySelector('#sn-results'),
        handoffs=root.querySelector('#sn-handoffs');
  if(!input || !filter || !status || !results || !handoffs) return;
  try {
    const sources=await Promise.all([
      fetch(new URL('./sequence-network-data.json',import.meta.url)),
      fetch(new URL('./sequence-network-handoffs.json',import.meta.url)),
    ]);
    if(sources.some(r=>!r.ok)) throw Error('Network data could not be loaded.');
    const [data,handoffsData]=await Promise.all(sources.map(r=>r.json()));
    if(data.schema!==1 || handoffsData.schema!==1) throw Error('Unsupported network data revision.');
    const names=new Map(data.records.map(r=>[r.id,r.name]));
    const rerender=()=>{
      const query=input.value.trim().slice(0,200);
      const selected=networkSearch(data,query,filter.value,MAX_RESULTS,handoffsData.matches);
      results.replaceChildren();handoffs.replaceChildren();
      if(!query){
        status.textContent=`${data.edges.length.toLocaleString()} archived formula-transfer records covering ${data.records.length.toLocaleString()} OEIS IDs. Enter an ID or name to explore.`;
        const suggestions=node('p','Examples: A000108 (Catalan), A000129 (Pell), A000217 (triangular).');
        handoffs.append(suggestions);return;
      }
      if(selected.localLeads.length){
        const aside=node('aside',undefined,'sn-handoff');
        aside.append(node('p',`Local ID ${query}: finite OEIS matches, not all-index identifications. Open a reference to explore its formula network.`));
        selected.localLeads.slice(0,8).forEach(hit=>{
          const a=node('a',`${hit.id} (${hit.terms} matching terms)`);a.href=networkLink(hit.id);aside.append(a);
        });handoffs.append(aside);
      }
      status.textContent=`${selected.total.toLocaleString()} archived connections found${selected.total>MAX_RESULTS?` · displaying first ${MAX_RESULTS}`:''}.`;
      for(const edge of selected.results)results.append(explainEdge(edge,names));
      if(!selected.total){
        results.append(node('li','No archived transfer in this curated index. Search the main OEIS reference database for additional sequences or formulas.','sn-no-results'));
      }
    };
    const fromUrl=new URLSearchParams(location.search).get('q') || '';
    input.value=fromUrl.slice(0,200);
    root.querySelector('#sn-form').addEventListener('submit',event=>{
      event.preventDefault();
      const q=input.value.trim().slice(0,200),url=new URL(location.href);
      if(q)url.searchParams.set('q',q);else url.searchParams.delete('q');
      history.replaceState(null,'',url);
      rerender();
    });
    filter.addEventListener('change',rerender);
    rerender();
  } catch(error) {
    status.textContent='This archived index could not load. The main Sequence Library and OEIS reference search remain available.';
    console.warn('Sequence network index unavailable:',error);
  }
}
if(typeof document!=='undefined') void mount();
