/* Author: Komorebi P. Continuation of equitable-quotient scalar rational compiler, preserving the first 51 certificates. */
'use strict';
function compileStateRationalV3(raw,engine,prior,compressSparse){
  const remaining=new Set(prior.deferred.map(r=>r.id));
  if(prior.failures.length)throw Error('Predecessor contains unresolved reconstruction failures');
  const check=(a,msg)=>{if(!a)throw Error(msg)};
  const trim=a=>{while(a.length>1&&a.at(-1)===0n)a.pop();return a};
  const primes=[];for(let p=10000019;primes.length<192;p+=2){let good=true;for(let i=3;i*i<=p;i+=2)if(p%i===0){good=false;break}if(good)primes.push(p)}
  function field(p){const mod=x=>((x%p)+p)%p,B=BigInt(p),cv=x=>Number((x%B+B)%B);
    const inv=a=>{let u=1,v=0,b=p;while(b){const q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"nonunit");return mod(u)};return {mod,cv,inv}}
  function bm(s,p){const {mod,cv,inv}=field(p);s=s.map(cv);let C=[1],B=[1],L=0,b=1,k=1;
    for(let n=0;n<s.length;n++){let d=s[n];for(let j=1;j<=L;j++)d=mod(d+(C[j]||0)*s[n-j]);if(d===0){k++;continue}
      const T=C.slice(),a=mod(d*inv(b));while(C.length<B.length+k)C.push(0);for(let j=0;j<B.length;j++)C[j+k]=mod(C[j+k]-a*B[j]);
      if(2*L<=n){L=n+1-L;B=T;b=d;k=1}else k++
    }
    while(C.length<L+1)C.push(0);return {L,C:C.slice(0,L+1)}
  }
  function coprime(P,Q,p){const {mod,cv,inv}=field(p),clean=a=>{while(a.length>1&&a.at(-1)===0)a.pop();return a};
    let a=clean(P.map(cv)),b=clean(Q.map(cv));if(a.length!==P.length||b.length!==Q.length)return false;
    while(b.some(x=>x)){const r=a.slice(),v=inv(b.at(-1));for(let i=r.length-b.length;i>=0;i--){const c=mod(r[i+b.length-1]*v);if(c)for(let j=0;j<b.length;j++)r[i+j]=mod(r[i+j]-c*b[j])}a=b;b=clean(r)}return a.length===1}
  const models=engine.compile(raw),results=[],deferred=[],failures=[];let residualChecks=0,referenceChecks=0;
  for(const [id,model] of Object.entries(models)){
    if(!remaining.has(id))continue;
    check(model.kind!=="reduced"&&model.w[0]==="const","invalid predecessor deferred ID");
    const q=compressSparse(model);
    if(q.status){deferred.push({id,...q});continue}
    const {raw:rawStates,states:S,edges,rounds,weights,quotient,width}=q;
    if(S>900||S*edges>6000000){deferred.push({id,raw:rawStates,states:S,edges,width,status:"quotient budget"});continue}
    const W=weights.map(BigInt),K=quotient.map(r=>r.map(([j,c])=>[j,BigInt(c)])),a=[];
    let v=Array(S).fill(1n);
    for(let n=0;n<=2*S;n++){a.push(v.reduce((x,y,j)=>x+y*W[j],0n));if(n<2*S)v=K.map(row=>row.reduce((x,[j,c])=>x+c*v[j],0n))}
    for(let n=1;n<=Math.min(2,S);n++){try{const value=engine.value(model,n);check(String(a[n])===value,"independent evaluation "+id);referenceChecks++}catch(e){if(!String(e.message).includes("work limit"))throw e}}
    let L=-1,M=1n,C=null,done=false;
    for(let pi=0;pi<primes.length;pi++){
      const p=primes[pi];
      const f=bm(L<0||pi%16===0?a:a.slice(0,Math.min(a.length,2*L+2)),p);if(f.L<L)continue;
      check(f.L<=S,"BM dimension exceeds quotient");
      if(f.L>L){L=f.L;M=1n;C=Array(L+1).fill(0n)}
      const {inv}=field(p),P=BigInt(p),iv=BigInt(inv(Number(M%P)));
      for(let j=0;j<=L;j++)C[j]+=M*((((BigInt(f.C[j])-C[j]%P)*iv)%P+P)%P);
      M*=P;
      const candidate=C.map(x=>x>M/2n?x-M:x);
      if(candidate[0]!==1n)continue;
      function residual(n){let r=a[n];for(let j=1;j<=L;j++)if(candidate[j])r+=candidate[j]*a[n-j];return r}
      let ok=true;for(let n=L;n<L+S;n++)if(residual(n)!==0n){ok=false;break}if(!ok)continue;
      const Q=trim(candidate.slice()),num=[];
      for(let n=0;n<L;n++){let r=a[n];for(let j=1;j<=Math.min(n,L);j++)r+=candidate[j]*a[n-j];num.push(r)}
      while(num.length<Q.length)num.push(0n);
      for(let j=0;j<Q.length;j++)num[j]-=a[0]*Q[j];const Pn=trim(num);
      if(!coprime(Pn,Q,p))continue;
      residualChecks+=S;
      results.push({id,offset:1,width,kind:model.kind,rawStates,quotientStates:S,quotientEdges:edges,partitionRounds:rounds,recurrenceStart:L,denominatorDegree:Q.length-1,minimalOrderCertified:true,coprimeWitnessPrime:p,crtModulusDigits:String(M).length,numerator:Pn.map(String),denominator:Q.map(String),initialZeroPowerCount:String(a[0])});
      done=true;break
    }
    if(!done)failures.push({id,rawStates,quotientStates:S,status:"CRT or minimality not certified within prime budget"})
  }
  const considered=results.length+deferred.length+failures.length;
  check(considered===remaining.size,"deferred state inventory");
  return {schemaVersion:1,author:"Komorebi P.",scope:"Fixed-width finite-state and block array models, padded by zero at n=0. Equitable partition M U = U K; weights count classes. Residuals are certified by Cayley-Hamilton on K. Exact reduced denominators certify minimal eventual orders. Retained combinatorial interpretations and OEIS evidence unchanged. Resource limits are explicit.",report:{previousCertified:prior.report.previousCertified+prior.results.length,attemptedDeferred:considered,certifiedRationalModels:results.length,resourceDeferred:deferred.length,reconstructionFailures:failures.length,exactResidualChecks:residualChecks,independentArrayChecks:referenceChecks,totalOriginalStates:results.reduce((a,r)=>a+r.rawStates,0),totalQuotientStates:results.reduce((a,r)=>a+r.quotientStates,0)},results,deferred,failures}
}
module.exports={compileStateRationalV3};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const raw=fs.readFileSync(path.join(dir,'OEIS_168_Array_Formulas.md'),'utf8');const prior=JSON.parse(fs.readFileSync(path.join(dir,'FIXED_STATE_ARRAY_RATIONAL_V2.json'),'utf8'));const out=compileStateRationalV3(raw,require('../website/assets/graph-array-evaluator.js'),prior,require('./graph_array_sparse_quotient.js').compressSparse);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
