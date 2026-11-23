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
