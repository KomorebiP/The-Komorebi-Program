/** Read-only OEIS transfer graph. Never executes source expressions. */
import {transferFormulaLatex,sourceFormulaLatex} from './sequence-network-math.mjs';
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

/** Retrieve the archived OEIS %F text, never a certified formula evaluator. */
export function sourceFormulaRows(data, oeisId, expectedSnapshot) {
  if(data?.schema!==1 || data?.evidence!=='unreviewed_source_text' ||
      data?.license!=='CC-BY-SA-4.0' || data?.snapshot_sha256!==expectedSnapshot)
    throw Error('OEIS source formula provenance could not be verified.');
  const identifier=String(oeisId??'').trim().toUpperCase();
  if(!OEIS.test(identifier))return [];
  const entry=data.entries?.[identifier];
  if(entry && (entry.source!=='https://oeis.org/'+identifier || !Array.isArray(entry.formulas)))
    throw Error('Invalid OEIS source formula entry.');
  return entry?.formulas || [];
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
/** A failed clipboard operation never receives success feedback. */
function copySourceButton(source, caption='Copy original') {
  const button=node('button',caption,'sn-copy');button.type='button';
  button.addEventListener('click',async()=>{
    try {await navigator.clipboard.writeText(source);button.textContent='Copied original';}
    catch {button.textContent='Copy unavailable. Select the original text.';}
  });
  return button;
}
function enhanceEquations(region){
  // Existing site-wide MathJax controller owns the typeset/plain preference.
  window.KomorebiMath?.enhance?.(region);
}
function equation(source, tex, label='Formula'){
  const wrapper=node('div',undefined,'sn-equation');
  const plain=node('p',source,'sn-equation-plain');
  if(tex){plain.dataset.mathLatex=tex;plain.setAttribute('aria-label',label);}
  wrapper.append(plain);return wrapper;
}
const SOURCE_KINDS=Object.freeze({term_candidate:'Term formula',recurrence:'Recurrence',
  generating_function:'Generating function',finite_or_infinite_sum:'Sum or product',
  unclassified:'Other source statement'});
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
  const heading=node('h3');
  heading.append(node('span',KIND[edge.kind] || 'Formula connection','sn-rel-kind'),officialLink(edge.target),document.createTextNode(' ← '));
  edge.inputs.forEach((input,i)=>{if(i)heading.append(document.createTextNode(' + '));heading.append(officialLink(input));});
  li.append(heading);
  const detail=[edge.target,...edge.inputs].map(id=>`${id}: ${names.get(id) || 'OEIS sequence'}`).join(' · ');
  li.append(node('p',detail,'sn-details'));
  li.append(equation(edge.expression,transferFormulaLatex(edge),'Recorded transfer formula'));
  const provenance=node('details',undefined,'sn-original');
  provenance.append(node('summary','Original expression and index conditions'));
  provenance.append(node('pre',edge.expression,'sn-original-text'));
  provenance.append(node('p','Evidence: '+(EVIDENCE[edge.evidence] || 'Unclassified'),'sn-evidence'));
  provenance.append(node('p','Index domain: '+edge.domain,'sn-details'));
  if(edge.kind==='hyperedge' && Object.keys(edge.index_maps || {}).length){
    provenance.append(node('p','Index maps: '+Object.entries(edge.index_maps).map(([id,ranges])=>
      id+': '+ranges.map(pair=>'n ↦ '+pair[0]+'n'+(pair[1]>=0?'+':'')+pair[1]).join(', ')).join(' · '),'sn-details'));
  }
  const controls=node('div',undefined,'sn-actions');
  controls.append(officialLink(edge.target,'View source on OEIS'),siteSearchLink(edge.target),copySourceButton(edge.expression));
  li.append(node('p',EVIDENCE[edge.evidence] || 'Unclassified evidence','sn-evidence'),provenance,controls);
  return li;
}
async function mount() {
  const root=document.querySelector('[data-sequence-network]');
  if(!root) return;
  const input=root.querySelector('#sn-query'), filter=root.querySelector('#sn-filter'),
        status=root.querySelector('#sn-status'), results=root.querySelector('#sn-results'),
        handoffs=root.querySelector('#sn-handoffs'), sourcePanel=root.querySelector('#sn-source-formulas'),
        sourceButton=root.querySelector('#sn-source-load'), sourceStatus=root.querySelector('#sn-source-status'),
        sourceResults=root.querySelector('#sn-source-results'), sourceMore=root.querySelector('#sn-source-more'),
        sourceOptions=root.querySelector('#sn-source-options'),sourceType=root.querySelector('#sn-source-type');
  if(!input || !filter || !status || !results || !handoffs || !sourcePanel ||
      !sourceButton || !sourceStatus || !sourceResults || !sourceMore || !sourceOptions || !sourceType) return;
  try {
    const sources=await Promise.all([
      fetch(new URL('./sequence-network-data.json',import.meta.url)),
      fetch(new URL('./sequence-network-handoffs.json',import.meta.url)),
    ]);
    if(sources.some(r=>!r.ok)) throw Error('Network data could not be loaded.');
    const [data,handoffsData]=await Promise.all(sources.map(r=>r.json()));
    if(data.schema!==1 || handoffsData.schema!==1) throw Error('Unsupported network data revision.');
    const names=new Map(data.records.map(r=>[r.id,r.name]));
    let sourcePromise=null, activeId='', sourceVersion=0, sourceRows=[], sourceShown=0;
    const sourceData=()=>{
      if(!sourcePromise) sourcePromise=fetch(new URL('./sequence-network-formulas.json',import.meta.url))
        .then(response=>{if(!response.ok)throw Error('Source formula archive unavailable.');return response.json();})
        .catch(error=>{sourcePromise=null;throw error;});
      return sourcePromise;
    };
    const renderSource=()=>{
      const selected=sourceType.value==='all'?sourceRows:sourceRows.filter(x=>x.kind===sourceType.value);
      window.KomorebiMath?.clear?.(sourceResults);sourceResults.replaceChildren();
      for(const [offset,item] of selected.slice(0,sourceShown).entries()){
        const li=node('li',undefined,'sn-source-line');
        const header=node('div',undefined,'sn-source-header');
        header.append(node('span',(offset+1)+'. '+(SOURCE_KINDS[item.kind]||item.kind),'sn-source-kind'),copySourceButton(item.text));
        li.append(header,equation(item.text,sourceFormulaLatex(item.text),'Archived OEIS source formula'));
        const raw=node('details',undefined,'sn-original');
        raw.append(node('summary','Read exact original OEIS field'),node('pre',item.text,'sn-original-text'));
        li.append(raw);
        sourceResults.append(li);
      }
      sourceMore.hidden=sourceShown>=selected.length;
      if(!sourceMore.hidden)sourceMore.textContent=`Show more (${selected.length-sourceShown} remaining)`;
      sourceStatus.textContent=`Showing ${Math.min(sourceShown,selected.length)} of ${selected.length} filtered source lines (${sourceRows.length} total). These are OEIS source records, not verified identities.`;
      if(activeId)sourceStatus.append(document.createTextNode(' '),officialLink(activeId,'Full OEIS entry'));
      enhanceEquations(sourceResults);
    };
    sourceType.addEventListener('change',()=>{sourceShown=Math.min(25,sourceRows.length);renderSource();});
    sourceMore.addEventListener('click',()=>{sourceShown=Math.min(sourceRows.length,sourceShown+25);renderSource();});
    sourceButton.addEventListener('click',async()=>{
      const requested=activeId, version=sourceVersion;
      if(!requested)return;
      sourceButton.disabled=true;sourceStatus.textContent='Loading pinned OEIS formula fields…';
      try{
        const archive=await sourceData();
        if(version!==sourceVersion)return;
        sourceRows=sourceFormulaRows(archive,requested,data.oeis.snapshot_sha256);
        sourceType.replaceChildren(node('option','All formula classes'));
        sourceType.firstChild.value='all';
        for(const kind of [...new Set(sourceRows.map(item=>item.kind))].sort()){
          const count=sourceRows.filter(row=>row.kind===kind).length;
          const option=node('option',(SOURCE_KINDS[kind]||kind)+` (${count})`);option.value=kind;sourceType.append(option);
        }
        sourceType.value='all';sourceOptions.hidden=!sourceRows.length;
        sourceShown=Math.min(25,sourceRows.length);
        sourceButton.hidden=true;renderSource();
        if(!sourceRows.length)sourceStatus.textContent='No formula fields retained for this ID in the pinned 99,999-entry snapshot.';

      }catch(error){
        if(version===sourceVersion)sourceStatus.textContent='Source formula text could not load. The original OEIS entry remains available.';
      }finally{if(version===sourceVersion)sourceButton.disabled=false;}
    });
    const rerender=()=>{
      const query=input.value.trim().slice(0,200);
      const requested=OEIS.test(query.toUpperCase())?query.toUpperCase():'';
      if(requested!==activeId){
        activeId=requested;sourceVersion++;sourceRows=[];sourceShown=0;
        sourceResults.replaceChildren();sourceMore.hidden=true;sourceOptions.hidden=true;
        sourceButton.hidden=false;sourceButton.disabled=false;
        sourceStatus.textContent=requested?'Formula text loads only when requested.':'';
      }
      sourcePanel.hidden=!requested;
      const selected=networkSearch(data,query,filter.value,MAX_RESULTS,handoffsData.matches);
      window.KomorebiMath?.clear?.(results);results.replaceChildren();handoffs.replaceChildren();
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
      enhanceEquations(results);
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
