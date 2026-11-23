import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {networkSearch,networkLink,sourceFormulaRows} from '../website/assets/sequence-network-ui.mjs';
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

import {exactFormulaLatex,sourceFormulaLatex,transferFormulaLatex} from '../website/assets/sequence-network-math.mjs';
test('typeset simple exact OEIS formulas with proper structure and original identifiers',()=>{
  const catalan=exactFormulaLatex('a(n) = binomial(2*n, n)/(n+1) = A000984(n)/(n+1).');
  assert.match(catalan,/\\binom\{2\\cdot n\}\{n\}/);
  assert.match(catalan,/\\frac/);
  assert.match(catalan,/\\mathrm\{A000984\}/);
  assert.match(sourceFormulaLatex('G.f.: x / (1 - x - x^2).'),/\\text\{OGF: \}/);
  assert.match(sourceFormulaLatex('F(n) = ((1+sqrt(5))^n - (1-sqrt(5))^n)/(2^n*sqrt(5)).'),/\\sqrt\{5\}/);
});
test('original archived prose and suspicious formulas cannot be silently typeset',()=>{
  const samples=['a(n) = arbitraryFunction(n)', 'a(n) = 4^n. - _A mathematician_, 2022',
    'a(n)=eval(alert(1))','a(n) = \\write18{touch hacked}', 'a(n)=<script>alert(1)</script>',
    'a(n) = Sum_{k=0..n} a(k)'];
  for(const formula of samples)assert.equal(sourceFormulaLatex(formula),null,formula);
});
test('math presentation derives from actual stored transfer edges, not substitute theorems',()=>{
  const selections=['hyperedge','gauge','riordan','quadratic'];
  for(const kind of selections){
    const edge=data.edges.find(e=>e.kind===kind);
    const latex=transferFormulaLatex(edge);
    assert.ok(latex,kind);
    assert.equal(latex.includes('\\href'),false);
  }
  const malformed={kind:'hyperedge',target:'<script>',inputs:['A000108'],expression:'1'};
  assert.equal(transferFormulaLatex(malformed),null);
  assert.equal(exactFormulaLatex('a(n)=A000984(n)\\require{html}'),null);
});
test('typesetting is optional and original source remains on the Network page',()=>{
  const ui=readFileSync(path.join(root,'website/assets/sequence-network-ui.mjs'),'utf8');
  const css=readFileSync(path.join(root,'website/assets/sequence-network.css'),'utf8');
  assert.match(ui,/dataset\.mathLatex=tex/);
  assert.match(ui,/Original expression and index conditions/);
  assert.match(ui,/Read exact original OEIS field/);
  assert.match(ui,/sourceType\.addEventListener/);
  assert.match(ui,/sourceResults\.replaceChildren/);
  assert.doesNotMatch(ui,/\b(?:innerHTML|outerHTML|eval|Function)\b/);
  assert.match(css,/overflow-x:auto/);
  assert.match(css,/sn-source-options/);
});
