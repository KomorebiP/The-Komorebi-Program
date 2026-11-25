/* Author: Komorebi P. Exact graph atlas transfer compiler.
 * Run: node tools/compile_graph_atlas_transfers.js [output.json]
 * Depends on the all-index audit; reads only the two immutable source catalogues.
 * The generated JSON uses decimal strings for unbounded integers.
 */
'use strict';
function compile(g,l){
  const check=(b,m)=>{if(!b)throw Error(m)};
  const trim=a=>{while(a.length>1&&!a.at(-1))a.pop();return a};
  const zero=a=>a.every(x=>x===0n);
  const equal=(a,b)=>a.length===b.length&&a.every((x,i)=>x===b[i]);
  const add=(a,b,k=1n)=>trim(Array.from({length:Math.max(a.length,b.length)},(_,i)=>(a[i]??0n)+k*(b[i]??0n)));
  function mul(a,b){const c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]+=a[i]*b[j];return trim(c)}
  function div(a,b){check(!zero(b),"division by zero");let r=trim(a.slice()),q=Array(Math.max(1,r.length-b.length+1)).fill(0n);while(!zero(r)&&r.length>=b.length){let i=r.length-b.length,v=r.at(-1);check(v%b.at(-1)===0n,"nonintegral division");v/=b.at(-1);q[i]=v;for(let j=0;j<b.length;j++)r[i+j]-=v*b[j];trim(r)}return [trim(q),r]}
  const exact=(a,b)=>{let [q,r]=div(a,b);check(zero(r),"nonzero remainder");return q};
  const one=d=>[1n,...Array(d-1).fill(0n),-1n];
  const cache=new Map();
  function phi(d){if(!cache.has(d)){let a=one(d);for(let j=1;j<d;j++)if(d%j===0)a=exact(a,phi(j));cache.set(d,a)}return cache.get(d)}
  function denominator(f){let q=[1n];for(const [d,e] of f)for(let i=0;i<e;i++)q=mul(q,phi(d));return q}
  const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
  const period=f=>[...f.keys()].reduce((a,d)=>a/gcd(a,BigInt(d))*BigInt(d),1n).toString();
  const canonicalFactors=f=>[...f].sort((a,b)=>a[0]-b[0]);
  const key=m=>m.p.join(",")+"/"+JSON.stringify(canonicalFactors(m.f));
  function block(s){const a=[];for(const ln of s.trim().split("\n")){const m=ln.match(/^\s*(\d+)-(\d+)\s+(.+)$/);check(m&&Number(m[1])===a.length,"invalid block");a.push(...m[3].split(",").map(BigInt));check(a.length===Number(m[2])+1,"invalid block length")}return a}
  const tidy=s=>s.replace(/\\(?:begin|end)\{aligned\}|\\\\|&|\\times|\s/g,"");
  function parseNumerator(s,b){s=tidy(s).replace(/^R\(x\)=/,"");if(s.startsWith("\\sum")){let a=block(b.match(/```text\n([\s\S]*?)\n```/)[1]);check(a.length===Number(s.match(/\^\{(\d+)\}/)[1])+1,"invalid numerator degree");return trim(a)}let a=[0n];while(s){const m=s.match(/^([+-]?)(\d*)(x(?:\^\{(\d+)\})?)?/);check(m[0]&&(m[2]||m[3]),"invalid numerator");let k=m[3]?Number(m[4]??1):0;while(a.length<=k)a.push(0n);a[k]+=BigInt(m[2]||"1")*(m[1]==="-"?-1n:1n);s=s.slice(m[0].length)}return trim(a)}
  const models=new Map(), laneMap=new Map();
  for(const m of l.matchAll(/^### ([A-Z]+\d+)[^\n]*\n([\s\S]*?)(?=^## |^### |$(?![\s\S]))/gm)){check(!laneMap.has(m[1]),"duplicate lane model");const b=m[2],s=b.match(/Finite polynomial part S \(ascending\): `([^`]+)`/)[1].split(",").map(x=>BigInt(x).toString()),lanes=[...b.matchAll(/\*\*d=(\d+), e=(\d+), h=(\d+)\*\*\s*```text\n([\s\S]*?)\n```/g)].map(a=>({d:Number(a[1]),e:Number(a[2]),h:a[3],c:block(a[4]).map(String)}));laneMap.set(m[1],{s,lanes})}
  for(const m of g.matchAll(/^### ([A-Z]+\d+) — ([^\n]*)\n([\s\S]*?)(?=^## |^### |$(?![\s\S]))/gm)){
    const [,id,title,b]=m;check(!models.has(id),"duplicate rational model");
    const a=[...b.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(x=>x[1]),shift=Number(b.match(/n<(\d+)/)[1]),r=parseNumerator(a[2],b),f=new Map();let t=tidy(a[3]).replace(/^Q\(x\)=/,"");
    while(t){const z=t.match(/^\\Phi_\{(\d+)\}\(x\)(?:\^\{(\d+)\})?/);check(z,"invalid denominator");const d=Number(z[1]),e=Number(z[2]??1);check(!f.has(d),"duplicate factor");f.set(d,e);check(!zero(div(r,phi(d))[1]),"unreduced denominator");t=t.slice(z[0].length)}
    const p=[...Array(shift).fill(0n),...r],q=denominator(f),meta=b.match(/Order (\d+); period (\d+)/);check(q.length-1===Number(meta[1])&&period(f)===meta[2],"order or period mismatch");
    const gf=title.match(/g=(\d+), k=(\d+)/),kf=title.match(/k=(\d+)/);
    models.set(id,{id,title,p,q,f,g:gf?Number(gf[1]):null,k:kf?Number(kf[1]):null,oeis:[...title.matchAll(/\bA\d{6}\b/g)].map(x=>x[0])});
  }
  check(models.size===288&&laneMap.size===288&&[...models.keys()].every(id=>laneMap.has(id)),"inventory mismatch");
  function combine(terms){let f=new Map();for(const [m] of terms)for(const [d,e] of m.f)f.set(d,Math.max(f.get(d)||0,e));let q=denominator(f),p=[0n];for(const [m,c] of terms)p=add(p,mul(m.p,exact(q,m.q)),c);if(zero(p))return {p:[0n],q:[1n],f:new Map()};for(let [d,e] of f){while(e){let [a,r]=div(p,phi(d));if(!zero(r))break;p=a;e--}if(e)f.set(d,e);else f.delete(d)}return {p,q:denominator(f),f}}
  const groups=new Map();for(const m of models.values()){let k=key(m);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(m.id)}
  const equivalent=[...groups.values()].filter(a=>a.length>1);
  const groupFor=new Map();for(const ids of groups.values())for(const id of ids)groupFor.set(id,ids);
  const identities=[];
  function relation(target,sources,type){check(sources.length>0,"empty relation");const r=combine([[models.get(target),-1n],...sources.map(id=>[models.get(id),1n])]);check(zero(r.p),`failed ${target} = ${sources.join("+")}`);identities.push({target,sources,type})}
  const select=(prefix,g,k)=>[...models.values()].filter(m=>new RegExp("^"+prefix+"\\d+$").test(m.id)&&m.g===g&&m.k===k).map(m=>m.id);
  for(const m of models.values()){
    if(/^[GB]\d+$/.test(m.id)&&!(m.g===1&&m.k===0))relation(m.id,select(m.id[0]==="G"?"D":"BD",m.g,m.k),"degree-profile-sum");
    if(/^R\d+$/.test(m.id)&&m.k<=8)relation(m.id,[...models.values()].filter(t=>/^T\d+$/.test(t.id)&&t.k===m.k).map(t=>t.id),"branching-profile-sum");
    if(/^C\d+$/.test(m.id)){const a=select("G",m.g,m.k);if(a.length)relation(m.id,a,"independent-unicyclic-construction")}
    if(/^U\d+$/.test(m.id)){const a=select("G",0,m.k);if(a.length)relation(m.id,a,"unrooted-tree-specialization")}
  }
  const differences=[],zeroDifferences=[];
  for(const m of models.values())if(/^G\d+$|^D\d+$/.test(m.id)){
    const other=models.get(m.id.replace(/^G/,"B").replace(/^D/,"BD"));check(other&&other.title===m.title,"mismatched bipartite pair");
    const r=combine([[m,1n],[other,-1n]]),id="N"+m.id;
    const relation={id,title:"Nonbipartite: "+m.title,positive:m.id,negative:other.id,g:m.g,k:m.k};
    if(zero(r.p)){zeroDifferences.push(relation);continue}
    differences.push({...relation,...r});
  }
  // Check the full profile partition also after taking the bipartite complement.
  const diffById=new Map(differences.map(m=>[m.id,m]));
  let complementSums=0;
  for(const m of differences.filter(m=>/^NG\d+$/.test(m.id)&&!(m.g===1&&m.k===0))){
    const ds=differences.filter(t=>/^ND\d+$/.test(t.id)&&t.g===m.g&&t.k===m.k);
    const r=combine([[m,-1n],...ds.map(t=>[t,1n])]);check(zero(r.p),"complement partition "+m.id);
    identities.push({target:m.id,sources:ds.map(t=>t.id),type:"nonbipartite-degree-profile-sum"});complementSums++;
  }
  const seenAll=new Set(groups.keys()),newKeys=new Set();for(const m of differences){const k=key(m);if(!seenAll.has(k))newKeys.add(k)}
  const encode=m=>{let s=m.p.findIndex(c=>c!==0n);return {id:m.id,title:m.title,g:m.g,k:m.k,numeratorShift:s,numerator:m.p.slice(s).map(String),cyclotomicFactors:canonicalFactors(m.f),minimalEventualOrder:m.q.length-1,leastEventualPeriod:period(m.f)}};
  // Independent coefficient recurrence check: all complement coefficients must agree
  // with subtraction, using each source's own reduced rational denominator.
  function terms(m,N){const a=[];for(let n=0;n<N;n++){let t=m.p[n]??0n;for(let i=1;i<=Math.min(n,m.q.length-1);i++)t-=m.q[i]*a[n-i];check(m.q[0]===1n,"denominator normalization");a.push(t)}return a}
  let coefficientChecks=0;for(const m of differences){const n=80,a=terms(m,n),b=terms(models.get(m.positive),n),c=terms(models.get(m.negative),n);for(let j=0;j<n;j++){check(a[j]===b[j]-c[j]&&a[j]>=0n,"complement coefficient "+m.id);coefficientChecks++}}
  const report={sourceRecords:models.size,sourceDistinctRationalFunctions:groups.size,equivalenceGroups:equivalent.length,equivalentRecords:equivalent.flat().length,duplicateRecords:models.size-groups.size,transferIdentities:identities.length,complementPartitionIdentities:complementSums,nonbipartiteNonzeroModels:differences.length,nonbipartiteZeroModels:zeroDifferences.length,nonbipartiteDistinctRationalFunctions:new Set(differences.map(key)).size,nonbipartiteNewDistinctRationalFunctions:newKeys.size,coefficientChecks};
  return {schemaVersion:1,author:"Komorebi P.",scope:"Exact rational transfers among retained models. Complement counts are conditional on the source combinatorial identifications; no new OEIS bindings.",report,equivalenceGroups:equivalent,transfers:identities,coreModels:[...models.values()].map(m=>({...encode(m),oeis:m.oeis,equivalentTo:groupFor.get(m.id).filter(id=>id!==m.id),residue:laneMap.get(m.id)})),nonbipartiteModels:differences.map(m=>({...encode(m),positive:m.positive,negative:m.negative})),zeroComplements:zeroDifferences};
}

module.exports = { compile };
if (require.main === module) {
  const fs=require('node:fs'),path=require('node:path');
  const root=path.join(__dirname,'..','research','graph-formula-atlas');
  const g=fs.readFileSync(path.join(root,'Graph_288_Formulas.md'),'utf8');
  const l=fs.readFileSync(path.join(root,'Graph_288_Binomial_Lanes.md'),'utf8');
  const {audit}=require('./verify_graph_formula_atlas_exact.js');
  audit(g,l);
  const result=compile(g,l);
  if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result.report,null,2));
}
