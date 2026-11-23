/** Read-only OEIS transfer graph. Never executes source expressions. */
import {formatNetworkMath} from './sequence-network-format.mjs';
const OEIS = /^A\d{6}$/;
const MAX_RESULTS = 60;
const PAGE_SIZE = 12;
const EVIDENCE = Object.freeze({
  all_index_formula_identity: 'Algebraic identity of extracted formula expressions',
  all_index_formula_identity_on_tail: 'Algebraic formula identity on the stated nonsingular tail',
  conditional_exact_ogf_identity: 'Exact formal OGF transform, conditional on the recorded premises',
  exact_quadratic_algebra: 'Exact quadratic-channel algebra for the stated definitions',
});
const KIND = Object.freeze({hyperedge:'Formula identity',gauge:'Gauge transfer',riordan:'Riordan transform',quadratic:'Quadratic channel'});

/** Count direct incidences, not mentions in a different sequence's title. */
export function networkProfile(data, rawId, category='all') {
  const id=String(rawId??'').trim().toUpperCase();
  if(!OEIS.test(id))return null;
  const record=(data.records || []).find(r=>r.id===id) || null;
  let total=0, target=0, input=0;
  for(const edge of data.edges || []){
    if(category!=='all' && edge.kind!==category)continue;
    const isTarget=edge.target===id, isInput=edge.inputs.includes(id);
    if(isTarget || isInput)total++;
    if(isTarget)target++;
    if(isInput)input++;
  }
  return {id,record,total,target,input};
}

export function networkSearch(data, rawQuery, category='all', limit=MAX_RESULTS, localMatches={}) {
  const q=String(rawQuery??'').trim().slice(0,200);
  const textMode=/^text:/i.test(q);
  const term=textMode?q.slice(5).trim():q;
  const key=term.toLocaleLowerCase();
  if (!key) return {total:0, results:[], localLeads:[], resolved:[]};
  const exact=term.toUpperCase();
  const exactId=!textMode && OEIS.test(exact);
  const leadValue=Object.hasOwn(localMatches,term)?localMatches[term]:
    Object.hasOwn(localMatches,exact)?localMatches[exact]:[];
  const localLeads=(!textMode&&!exactId&&Array.isArray(leadValue)?leadValue:[])
    .filter(x=>x && OEIS.test(x.id));
  const matching=new Set(localLeads.map(x=>x.id));
  if(exactId){if((data.records || []).some(r=>r.id===exact))matching.add(exact);}
  else for(const record of data.records || []) {
    if(record.id.toLowerCase()===key || record.name.toLocaleLowerCase().includes(key)) matching.add(record.id);
  }
  const candidates=[];
  for(const edge of data.edges || []) {
    if(category!=='all' && edge.kind!==category) continue;
    const incident=[edge.target,...edge.inputs];
    // Exact IDs mean incidence. The explicit text: mode also searches names
    // and formulas, without turning a textual mention into a direct edge.
    if(incident.some(id=>matching.has(id)) || (!exactId && (
       String(edge.expression).toLocaleLowerCase().includes(key) ||
       String(edge.kind).toLocaleLowerCase().includes(key)))) candidates.push(edge);
  }
  candidates.sort((a,b)=>{
    const score=e=> e.target===exact?0:e.inputs.includes(exact)?1:e.kind==='hyperedge'?2:e.kind==='gauge'?3:4;
    return score(a)-score(b) || a.key.localeCompare(b.key);
  });
  return {total:candidates.length,results:candidates.slice(0,Math.max(0,Math.min(limit,(data.edges || []).length))),localLeads,resolved:[...matching].sort()};
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
function officialLink(id, label) {
  const a=node('a',label || id);
  a.href=OEIS.test(id)?'https://oeis.org/'+id:'sequence-library.html';
  return a;
}
function sequenceNetworkLink(id, label) {
  const a=node('a',label || id);
  a.href=networkLink(id);
  a.setAttribute('aria-label',label || 'Explore '+id+' direct connections');
  return a;
}
function siteSearchLink(id) {
  const a=node('a','Search '+id+' in the local Sequence Library');
  a.href='sequence-library.html?q='+encodeURIComponent('oeis:'+id)+'#library-search';
  return a;
}
function readableDomain(domain) {
  const text=String(domain||'');
  const tail=/^local n>=(\d+) with nonsingular ratio denominator$/.exec(text);
  if(tail)return 'Local indices n ≥ '+tail[1]+', where the required denominator is nonzero.';
  if(text==='all local n>=0')return 'All local indices n ≥ 0.';
  if(text==='all integer n>=0 for quadratic channel definition')
    return 'All integer indices n ≥ 0 under the quadratic-channel definition.';
  if(text==='formal generating series under source and target OGF premises')
    return 'Conditional on the recorded ordinary generating functions of both sequences.';
  return text;
}
function equation(plain, tex, label, className='sn-statement') {
  const el=node('div',plain,className);
  el.setAttribute('aria-label',label+': '+plain);
  if(tex)el.setAttribute('data-math-latex',tex);
  return el;
}
function explainEdge(edge, names) {
  const li=node('li',undefined,'sn-result');
  li.setAttribute('aria-label','Archived transfer: '+edge.target+' from '+edge.inputs.join(', '));
  const kind=node('span',KIND[edge.kind] || 'Formula connection','sn-rel-kind');
  const heading=node('h3');heading.append(kind,sequenceNetworkLink(edge.target),document.createTextNode(' ← '));
  edge.inputs.forEach((input,i)=>{if(i)heading.append(document.createTextNode(', '));heading.append(sequenceNetworkLink(input));});
  li.append(heading);

  const formatted=formatNetworkMath(edge);
  const block=node('section',undefined,'sn-formula-block');
  block.append(node('h4',edge.kind==='riordan'?'Recorded transform':'Transfer formula','sn-formula-label'));
  block.append(equation(formatted.plain,formatted.tex,'Transfer formula'));
  if(formatted.definition){
    block.append(node('p','Defining factor','sn-formula-label'));
    block.append(equation(formatted.definition.plain,formatted.definition.tex,'Definition of L','sn-definition'));
  }
  if(formatted.parameters?.length){
    const parameters=node('dl',undefined,'sn-parameters');
    for(const [name,value] of formatted.parameters){
      const item=node('div',undefined,'sn-parameter');
      item.append(node('dt',name),node('dd',value));parameters.append(item);
    }
    block.append(parameters);
  }
  if(formatted.help)block.append(node('p',formatted.help,'sn-help'));
  li.append(block);

  const evidence=node('p',undefined,'sn-evidence');
  evidence.append(node('strong','Evidence: '),document.createTextNode(EVIDENCE[edge.evidence] || 'Unclassified evidence'));
  li.append(evidence);
  li.append(node('p','Valid domain: '+readableDomain(edge.domain),'sn-domain'));

  const details=node('details',undefined,'sn-record-details');
  details.append(node('summary','Original archive expression, sequence titles, and provenance'));
  const detailList=node('dl',undefined,'sn-source-names');
  for(const id of [edge.target,...edge.inputs]){
    const item=node('div');
    const description=node('dd',names.get(id) || 'OEIS sequence');
    description.append(document.createTextNode(' · '),officialLink(id,'View '+id+' on OEIS'));
    item.append(node('dt',id===edge.target?'Target '+id:'Input '+id),description);
    detailList.append(item);
  }
  details.append(detailList);
  details.append(node('p','Exact source expression (unchanged):','sn-original-label'),
                 node('pre',edge.expression,'sn-original'));
  if(edge.kind==='hyperedge' && Object.keys(edge.index_maps || {}).length){
    details.append(node('p','Index maps: '+Object.entries(edge.index_maps).map(([id,ranges])=>
      id+': '+ranges.map(pair=>'n ↦ '+pair[0]+'n'+(pair[1]>=0?'+':'')+pair[1]).join(', ')).join(' · '),'sn-details'));
  }
  details.append(node('p','Original domain: '+edge.domain,'sn-details'));
  details.append(node('p','Source receipt: '+edge.source_receipt,'sn-receipt'),
                 node('p','Proof reference: '+edge.proof_ref,'sn-receipt'));
  li.append(details);

  const controls=node('div',undefined,'sn-actions');
  controls.append(officialLink(edge.target,'View '+edge.target+' on OEIS'),siteSearchLink(edge.target));
  li.append(controls);
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
        more=root.querySelector('#sn-show-more');
  if(!input || !filter || !status || !results || !handoffs || !sourcePanel ||
      !sourceButton || !sourceStatus || !sourceResults || !sourceMore || !more) return;
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
    const renderSource=(focusAdded=false)=>{
      // Append new archive lines instead of rebuilding the reader's existing
      // list. This preserves selection, screen-reader position and disclosure.
      const start=sourceResults.children.length;
      for(const item of sourceRows.slice(start,sourceShown)){
        const li=node('li',undefined,'sn-source-line');
        li.append(node('p',item.kind,'sn-source-kind'),node('pre',item.text,'sn-source-expression'));
        sourceResults.append(li);
      }
      sourceMore.hidden=sourceShown>=sourceRows.length;
      if(!sourceMore.hidden)sourceMore.textContent=`Show more formulas (${sourceRows.length-sourceShown} remaining)`;
      if(focusAdded && sourceShown>start){
        const firstAdded=sourceResults.children[start];
        firstAdded.tabIndex=-1;
        firstAdded.focus();
      }
    };
    sourceMore.addEventListener('click',()=>{sourceShown=Math.min(sourceRows.length,sourceShown+25);renderSource(true);});
    sourceButton.addEventListener('click',async()=>{
      const requested=activeId, version=sourceVersion;
      if(!requested)return;
      const focusWasOnButton=document.activeElement===sourceButton;
      sourceButton.disabled=true;sourceStatus.textContent='Loading pinned OEIS formula fields…';
      try{
        const archive=await sourceData();
        if(version!==sourceVersion)return;
        sourceRows=sourceFormulaRows(archive,requested,data.oeis.snapshot_sha256);
        sourceShown=Math.min(25,sourceRows.length);
        sourceButton.hidden=true;renderSource();
        sourceStatus.textContent=sourceRows.length
          ? `${sourceRows.length} source formula lines. These are unreviewed OEIS records, not proven sequence identities.`
          : names.has(requested)
            ? 'No source formula fields were retained for this curated ID in the pinned 99,999-entry snapshot.'
            : 'This ID is outside the curated source-formula archive. Its full OEIS entry remains available.';
        const external=officialLink(requested,'Read the full source entry on OEIS');
        sourceStatus.append(document.createTextNode(' '),external);
        // The load button disappears after success. Retain the reader's focus
        // unless they have already moved elsewhere during the asynchronous load.
        if(focusWasOnButton && (document.activeElement===sourceButton ||
            document.activeElement===document.body || document.activeElement===document.documentElement)){
          const destination=sourceResults.firstElementChild || sourceStatus;
          destination.tabIndex=-1;destination.focus();
        }
      }catch(error){
        if(version===sourceVersion)sourceStatus.textContent='Source formula text could not load. The original OEIS entry remains available.';
      }finally{if(version===sourceVersion)sourceButton.disabled=false;}
    });
    let current=null, shown=0;
    const showNext=(focusAdded=false)=>{
      if(!current)return;
      const end=Math.min(current.results.length,shown+PAGE_SIZE);
      const added=[];
      for(const edge of current.results.slice(shown,end)){
        const item=explainEdge(edge,names);
        results.append(item);
        added.push(item);
      }
      shown=end;
      const remaining=current.results.length-shown;
      more.hidden=remaining===0;
      if(remaining)more.textContent='Show next '+Math.min(PAGE_SIZE,remaining)+' connections ('+remaining+' remaining)';
      status.textContent=current.total.toLocaleString()+' archived connections found · showing '+shown+' of '+current.total.toLocaleString()+'.';
      // When the button disappears after the final batch, retain a meaningful
      // keyboard and screen-reader position at the newly revealed records.
      if(focusAdded && added.length){added[0].tabIndex=-1;added[0].focus();}
      if(!current.total && shown===0){
        results.append(node('li','No archived transfer in this curated index. Search the main OEIS reference database for additional sequences or formulas.','sn-no-results'));
      }
    };
    more.addEventListener('click',()=>showNext(true));
    const rerender=()=>{
      const query=input.value.trim().slice(0,200);
      const requested=OEIS.test(query.toUpperCase())?query.toUpperCase():'';
      if(requested!==activeId){
        activeId=requested;sourceVersion++;sourceRows=[];sourceShown=0;
        sourceResults.replaceChildren();sourceMore.hidden=true;
        sourceButton.hidden=false;sourceButton.disabled=false;
        sourceStatus.textContent=requested?'Formula text loads only when requested.':'';
      }
      sourcePanel.hidden=!requested;
      window.KomorebiMath?.clear?.(results);
      results.replaceChildren();handoffs.replaceChildren();
      current=null;shown=0;more.hidden=true;
      if(!query){
        status.textContent=data.edges.length.toLocaleString()+' archived formula-transfer records covering '+data.records.length.toLocaleString()+' OEIS IDs. Enter an ID or name to explore.';
        handoffs.append(node('p','Examples: A000108 (Catalan), A000129 (Pell), A000217 (triangular).'));
        return;
      }
      const selected=networkSearch(data,query,filter.value,data.edges.length,handoffsData.matches);
      if(selected.localLeads.length){
        const aside=node('aside',undefined,'sn-handoff');
        aside.append(node('p','Local ID '+query+': finite OEIS matches, not all-index identifications. Open a reference to explore its formula network.'));
        selected.localLeads.slice(0,8).forEach(hit=>{
          const a=node('a',hit.id+' ('+hit.terms+' matching terms)');a.href=networkLink(hit.id);aside.append(a);
        });handoffs.append(aside);
      }
      const profile=networkProfile(data,query,filter.value);
      if(profile){
        const panel=node('section',undefined,'sn-handoff sn-profile');
        const heading=node('h3',profile.id+' · direct transfer connections');
        heading.id='sn-profile-title';panel.setAttribute('aria-labelledby',heading.id);
        panel.append(heading);
        if(profile.record){
          panel.append(node('p',profile.record.name));
          panel.append(node('p',profile.total.toLocaleString()+' distinct direct records under the selected relation class · '+
            profile.target.toLocaleString()+' as target · '+profile.input.toLocaleString()+' as input. A record can have both roles.'));
        }else{
          panel.append(node('p','This identifier is outside the curated transfer graph. The full OEIS entry remains available.'));
        }
        const links=node('div',undefined,'sn-quicklinks');
        const archived=node('a','Jump to archived formula text');archived.href='#sn-source-formulas';
        links.append(officialLink(profile.id,'View '+profile.id+' on OEIS'),archived,
          sequenceNetworkLink('text:'+profile.id,'Search broader text mentions of '+profile.id));
        panel.append(links);handoffs.append(panel);
      }
      current=selected;
      showNext();
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
