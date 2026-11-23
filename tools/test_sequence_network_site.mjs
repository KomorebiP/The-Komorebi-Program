import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {networkSearch,networkLink,sourceFormulaRows} from '../website/assets/sequence-network-ui.mjs';
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
