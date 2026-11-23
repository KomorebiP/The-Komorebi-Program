'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'sequence-sparse-transfer-atlas-v1.4.html'),'utf8');
const data=html.match(/<script id="atlas-data" type="application\/json">([\s\S]*?)<\/script>/);
const code=html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(data&&code);
const rows=JSON.parse(data[1]);
assert.equal(rows.length,153);
assert.equal(rows.filter(x=>x.type==='sparse').length,110);
assert.equal(rows.filter(x=>x.type==='riordan').length,41);
assert.equal(rows.filter(x=>x.type==='quadratic').length,2);
function el(tag='div'){
  const e={tagName:tag,textContent:'',children:[],value:'',listeners:{},
    appendChild(c){this.children.push(c)},
    replaceChildren(){this.children.length=0},
    addEventListener(k,fn){this.listeners[k]=fn}};
  return e;
}
const elements={
  'atlas-data':{textContent:data[1]},
  query:el('input'), kind:el('select'), records:el('tbody'), count:el('strong')
};
elements.kind.value='all';
const document={getElementById:id=>elements[id],createElement:el,createTextNode:text=>({textContent:text})};
vm.runInNewContext(code[1],{document,JSON,String,console});
assert.equal(elements.count.textContent,'153 shown');
assert.equal(elements.records.children.length,153);
elements.kind.value='riordan';elements.kind.listeners.change();
assert.equal(elements.records.children.length,41);
elements.query.value='A000079';elements.query.listeners.input();
assert.ok(elements.records.children.length>0);
for(const tr of elements.records.children)
  assert.ok(tr.children[0].children.every(n=>n.tagName==='a'||typeof n.textContent==='string'));
console.log('Sparse atlas offline DOM smoke test: passed');
