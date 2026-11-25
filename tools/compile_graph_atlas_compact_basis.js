/* Author: Komorebi P. Exact extension of the rational transfer basis with fixed-state array functions. */
'use strict';
function certifyCompactBasis(data,basis,fixed,prior,prior2,prior3,compactModels,arrayModels){
 const check=(a,m)=>{if(!a)throw Error(m)};
 const mul=(a,b)=>{let c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]+=a[i]*b[j];return c};
 function div(a,b){let c=a.slice(),q=Array(a.length-b.length+1).fill(0n);for(let i=q.length-1;i>=0;i--){check(c[i+b.length-1]%b.at(-1)===0n,"noninteger quotient");q[i]=c[i+b.length-1]/b.at(-1);for(let j=0;j<b.length;j++)c[i+j]-=q[i]*b[j]}check(!c.some(x=>x),"nonexact quotient");return q}
 const phis=new Map();function phi(d){if(!phis.has(d)){let q=[1n,...Array(d-1).fill(0n),-1n];for(let i=1;i<d;i++)if(d%i===0)q=div(q,phi(i));phis.set(d,q)}return phis.get(d)}
 const models=new Map();for(const m of data.coreModels){let Q=[1n];for(const [d,e] of m.cyclotomicFactors)for(let i=0;i<e;i++)Q=mul(Q,phi(d));models.set(m.id,{id:m.id,P:[...Array(m.numeratorShift).fill(0n),...m.numerator.map(BigInt)],Q})}
 for(const m of [...fixed.explicit,...prior.results,...prior2.results,...prior3.results])models.set(m.id,{id:m.id,P:m.numerator.map(BigInt),Q:m.denominator.map(BigInt)});
 for(const m of fixed.compact)models.set(m.id,{id:m.id,expr:arrayModels[m.id].expr});
 for(const m of compactModels.records)models.set(m.id,{id:m.id,residues:m.residues});
 const order=[...basis.basis,...compactModels.records.map(m=>m.id)];
 check(new Set(order).size===order.length,"duplicate basis ID");
 function scan(p,N,duplicate=false){
   check(Number.isSafeInteger(p*p),"modulus too large");for(let j=2;j*j<=p;j++)check(p%j!==0,"nonprime");
   const big=BigInt(p),mod=x=>((x%p)+p)%p,cv=x=>Number((x%big+big)%big),inv=a=>{let u=1,v=0,b=p;while(b){let q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"inverse");return mod(u)};
   function seq(P,Q,N){P=P.map(cv);Q=Q.map(cv);check(Q[0]===1,"normalization");const a=new Float64Array(N);for(let n=0;n<N;n++){let t=P[n]||0;for(let k=1;k<Math.min(Q.length,n+1);k++)if(Q[k])t=mod(t-Q[k]*a[n-k]);a[n]=t}return a}
   const strips=new Map(fixed.stripModels.map(m=>[m.diagonal+","+m.width,seq(m.numerator.map(BigInt),m.denominator.map(BigInt),N+4)]));
   function compact(expr,n){if(n===0)return 0;const env={n,h:1+Math.floor(n/2),k:1+Math.ceil(n/2)};function ev(a){const [op,x,y,z]=a;if(op==="var")return env[x];if(op==="const")return Number(x);if(op==="ind")return strips.get(ev(y)+","+ev(x))[ev(z)];if(op==="mul")return mod(ev(x)*ev(y));if(op==="pow"){let r=1,b=ev(x),k=ev(y);while(k--)r=mod(r*b);return r}throw Error("compact op")}return ev(expr)}
   const rows=[],pivots=[],dependent=[],pivotValues=[];
   for(const id of duplicate?[...order,order[0]]:order){
     const m=models.get(id),a=m.residues?Float64Array.from(m.residues[p].slice(0,N)):m.expr?Float64Array.from({length:N},(_,n)=>compact(m.expr,n)):seq(m.P,m.Q,N);
     for(let j=0;j<pivots.length;j++){let c=a[pivots[j]];if(c)for(let k=pivots[j];k<N;k++)a[k]=mod(a[k]-c*rows[j][k])}
     const col=a.findIndex(x=>x);if(col<0){dependent.push(id);continue}
     pivotValues.push(a[col]);const v=inv(a[col]);for(let k=col;k<N;k++)a[k]=mod(a[k]*v);
     let j=pivots.findIndex(k=>k>col);if(j<0)j=pivots.length;pivots.splice(j,0,col);rows.splice(j,0,a)
   }
   return {prime:p,coefficientCount:N,rank:rows.length,pivotIndices:pivots,pivotValues,dependent};
 }
 const N=compactModels.report.coefficientCount;
 const witnesses=[scan(1000003,N),scan(1000033,N)];
 if(witnesses.some(r=>r.rank!==order.length)){return {rankProbe:witnesses.map(w=>({prime:w.prime,rank:w.rank,dependent:w.dependent})),modelCount:order.length};}check(witnesses.every(r=>r.rank===order.length&&r.dependent.length===0),"new functions not all independent");
 const control=scan(1000003,N,true);check(control.rank===order.length&&control.dependent.length===1&&control.dependent[0]===order[0],"duplicate control failed");
 const rows=[...basis.transferRows,...compactModels.records.map(m=>({target:m.id,denominator:"1",terms:[{id:m.id,multiplier:"1"}]}))];
 check(new Set(rows.map(r=>r.target)).size===rows.length,"duplicate row");
 return {schemaVersion:1,author:"Komorebi P.",scope:"Constant rational span of the earlier 488 certified models and 14 additional compact fixed-width binary array rational functions, padded by zero before each original index offset. Every added function is independent of the previous basis and of the others by the modular prefix witnesses. Existing exact spanning identities are retained. Not the full 537-record atlas and not a novelty claim.",report:{previousModels:basis.report.totalModels,previousRank:basis.report.rank,addedModels:compactModels.records.length,totalModels:rows.length,rank:order.length,dependenceDimension:rows.length-order.length,independenceWitnessCount:witnesses.length,duplicateNegativeControlRejected:true},basis:order,transferRows:rows,witnesses,addedBasis:compactModels.records.map(m=>m.id)};
}
module.exports={certifyCompactBasis};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8'),json=f=>JSON.parse(read(f));const g=read('Graph_288_Formulas.md'),l=read('Graph_288_Binomial_Lanes.md'),raw=read('OEIS_168_Array_Formulas.md');require('./verify_graph_formula_atlas_exact.js').audit(g,l);const data=require('./compile_graph_atlas_transfers.js').compile(g,l),engine=require('../website/assets/graph-array-evaluator.js');const out=certifyCompactBasis(data,json('STATE_ENLARGED_TRANSFER_BASIS_V3.json'),json('FIXED_ARRAY_WALK_RATIONAL.json'),json('FIXED_STATE_ARRAY_RATIONAL.json'),json('FIXED_STATE_ARRAY_RATIONAL_V2.json'),json('FIXED_STATE_ARRAY_RATIONAL_V3.json'),json('FIXED_STATE_ARRAY_COMPACT_DEFERRED.json'),engine.compile(raw));if(!out.report)throw Error(JSON.stringify(out));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
