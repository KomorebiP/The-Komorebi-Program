import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {networkSearch,networkLink,networkProfile,sourceFormulaRows} from '../website/assets/sequence-network-ui.mjs';
import {formatNetworkMath,algebraLatex} from '../website/assets/sequence-network-format.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const data=JSON.parse(readFileSync(path.join(root,'manifests/sequence-transfer-network.json'),'utf8'));

test('first-class searchable actual OEIS graph',()=>{
  assert.equal(data.edges.length,1559);
  assert.ok(data.records.some(x=>x.id==='A000108'));
  let r=networkSearch(data,'A000108');
  assert.ok(r.total>0);
  assert.ok(r.results.some(x=>x.target==='A000108'||x.inputs.includes('A000108')));
  assert.ok(networkSearch(data,'Catalan').total>0);
  assert.ok(networkSearch(data,'A000108','riordan').total<=r.total);
});
test('archived source formulas have independent provenance and no proof promotion',()=>{
  const source=JSON.parse(readFileSync(path.join(root,'manifests/sequence-network-formula-text.json'),'utf8'));
  assert.equal(source.counts.network_ids,916);
  assert.equal(source.counts.ids_with_formulas,845);
  assert.equal(source.counts.formula_lines,8853);
  const lines=sourceFormulaRows(source,'A000108',data.oeis.snapshot_sha256);
  assert.ok(lines.length>0);
  assert.ok(lines.some(x=>x.text.includes('binomial(2*n')));
  assert.throws(()=>sourceFormulaRows({...source,evidence:'all_index_formula_identity'},'A000108',data.oeis.snapshot_sha256));
  assert.throws(()=>sourceFormulaRows(source,'A000108','modified-snapshot'));
  assert.deepEqual(sourceFormulaRows(source,'bogus',data.oeis.snapshot_sha256),[]);
});
test('local index comparison leads never imply proof',()=>{
  const leads={'KSEQ-01':[{id:'A000108',terms:24}]};
  let r=networkSearch(data,'KSEQ-01','all',60,leads);
  assert.equal(r.localLeads.length,1);
  assert.ok(r.total>0);
  assert.equal(networkLink('KSEQ-01'),'sequence-network.html?q=KSEQ-01#sequence-network');
});
test('invalid identifiers cannot be used as destinations',()=>{
  assert.equal(networkLink('javascript:alert(1)'),'sequence-network.html');
  assert.equal(networkLink('A000108'), 'sequence-network.html?q=A000108#sequence-network');
});
test('no raw source execution or unsafe HTML injection is introduced',()=>{
  let src=readFileSync(path.join(root,'website/assets/sequence-network-ui.mjs'),'utf8');
  assert.doesNotMatch(src,/\b(?:innerHTML|outerHTML|eval|Function)\b/);
  assert.match(src,/textContent/);
});

test('all pinned gauge definitions use a typeset-safe grammar without changing archived strings',()=>{
  const gauges=data.edges.filter(x=>x.kind==='gauge');
  assert.equal(gauges.length,975);
  for(const edge of gauges){
    const old=edge.expression;
    const view=formatNetworkMath(edge);
    assert.ok(view.tex,edge.key+' ratio formula');
    assert.ok(view.definition?.tex,edge.key+' defining factor '+old);
    assert.equal(view.parameters.length,5);
    assert.ok(view.help.includes('dummy variable'));
    assert.equal(edge.expression,old,'formatter must not alter archived evidence');
  }
});
test('formula and quadratic channels render without executing or altering the source',()=>{
  let formatted=0;
  for(const edge of data.edges.filter(x=>x.kind==='hyperedge'||x.kind==='quadratic')){
    const view=formatNetworkMath(edge);
    if(view.tex)formatted++;
    assert.equal(edge.expression,String(edge.expression));
    assert.ok(view.plain);
  }
  assert.ok(formatted>=540,'most exact algebraic edges should typeset');
  const gauge=data.edges.find(x=>x.kind==='gauge'&&x.expression.includes('961*n+962'));
  const f=formatNetworkMath(gauge);
  assert.match(f.definition.tex,/961/);
  assert.match(f.definition.tex,/u/);
  assert.equal(formatNetworkMath(data.edges.find(x=>x.kind==='riordan')).tex,null,
    'a Riordan parameter record must not invent a missing OGF equation');
});
test('bounded arithmetic translator preserves fractions, powers, and rejects unexpected syntax',()=>{
  assert.equal(algebraLatex('A000108(n)/2'),'\\frac{\\mathrm{A000108}\\!\\left(n\\right)}{2}');
  assert.ok(algebraLatex('A000108(n)**2').includes('^{2}'));
  assert.equal(algebraLatex('A000108(n); alert(1)'),null);
  assert.equal(algebraLatex('<script>'),null);
});

test('large sequence-name searches expose every pinned edge instead of silently cutting off at sixty',()=>{
  const limited=networkSearch(data,'binomial');
  const complete=networkSearch(data,'binomial','all',data.edges.length);
  assert.equal(complete.total,331);
  assert.equal(limited.results.length,60,'compatibility default retains prior bounded API');
  assert.equal(complete.results.length,331,'UI may paginate all known results');
  assert.equal(new Set(complete.results.map(edge=>edge.key)).size,331);
  assert.equal(networkSearch(data,'n','all',data.edges.length).results.length,data.edges.length,
    'maximum-size search can be explored incrementally');
});


test('sequence-name matches do not mask independent formula-text matches',()=>{
  const fixture={
    records:[
      {id:'A000001',name:'Numbers featuring 3'},
      {id:'A000002',name:'Another sequence'},
      {id:'A000003',name:'Third collection'}
    ],
    edges:[
      {key:'named',target:'A000001',inputs:[],kind:'hyperedge',expression:'n+1'},
      {key:'expression',target:'A000002',inputs:[],kind:'hyperedge',expression:'3*n'}
    ]
  };
  const matched=networkSearch(fixture,'3','all',fixture.edges.length);
  assert.equal(matched.total,2);
  assert.deepEqual(new Set(matched.results.map(e=>e.key)),new Set(['named','expression']));
  const q='3', named=new Set(data.records.filter(x=>
    x.id.toLowerCase()===q || x.name.toLowerCase().includes(q)).map(x=>x.id));
  const expected=data.edges.filter(e=>[e.target,...e.inputs].some(id=>named.has(id)) ||
    String(e.expression).toLowerCase().includes(q) ||
    String(e.kind).toLowerCase().includes(q));
  assert.equal(networkSearch(data,q,'all',data.edges.length).total,expected.length,
    'no formula-text matches are lost when a sequence name matches');
  assert.equal(networkSearch(data,'binomial','all',data.edges.length).total,331,
    'the previously verified binomial inventory is unchanged');
});


test('exact OEIS identifiers select direct graph incidences, not title references',()=>{
  const catalan=networkProfile(data,'a000108');
  assert.equal(catalan.record.id,'A000108');
  assert.deepEqual([catalan.total,catalan.target,catalan.input],[9,0,9]);
  assert.equal(networkSearch(data,'a000108','all',data.edges.length).total,9);
  assert.equal(networkSearch(data,'text:A000108','all',data.edges.length).total,17);
  assert.equal(networkSearch(data,'A000302','all',data.edges.length).total,17);
  assert.equal(networkSearch(data,'text:A000302','all',data.edges.length).total,61);
  assert.equal(networkSearch(data,'A000217','all',data.edges.length).total,59);
  assert.equal(networkProfile(data,'A000931').record,null);
  assert.equal(networkSearch(data,'A000931','all',data.edges.length).total,0);
  assert.deepEqual(networkSearch(data,'constructor').localLeads,[]);
  assert.deepEqual(networkSearch(data,'toString').localLeads,[]);
  assert.equal(networkProfile(data,'not-an-id'),null);
});

test('every curated identifier has exact role counts and complete unique incident records',()=>{
  for(const record of data.records){
    const id=record.id;
    const expected=data.edges.filter(e=>e.target===id || e.inputs.includes(id));
    const profile=networkProfile(data,id);
    const search=networkSearch(data,id,'all',data.edges.length);
    assert.equal(profile.total,expected.length,id);
    assert.equal(profile.target,expected.filter(e=>e.target===id).length,id);
    assert.equal(profile.input,expected.filter(e=>e.inputs.includes(id)).length,id);
    assert.equal(search.total,expected.length,id);
    assert.deepEqual(new Set(search.results.map(e=>e.key)),new Set(expected.map(e=>e.key)),id);
    for(const kind of ['hyperedge','gauge','riordan','quadratic']){
      assert.equal(networkProfile(data,id,kind).total,expected.filter(e=>e.kind===kind).length,id+' '+kind);
    }
  }
});
