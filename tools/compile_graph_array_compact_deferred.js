/* Author: Komorebi P. Compact fixed-width rational realizations and exact finite-field moments. */
'use strict';
function compileCompactDeferred(raw,engine,prior,compressSparse,N=256,primes=[1000003,1000033]){
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const models=engine.compile(raw),records=[],spectral=[],checks={independentArrayComparisons:0,resourceSkipped:0,exactSparseFirstTermChecks:0,specializedControls:0};
  for(const p of primes){check(Number.isSafeInteger(p*1000000),"unsafe modulus");for(let d=2;d*d<=p;d++)check(p%d!==0,"nonprime")}
  function rowsFor(w,L){const rows=[];for(let x=0;x<2**w;x++){let good=true;for(let j=0;j<=w-L;j++)if(((x>>j)&((1<<L)-1))===(1<<L)-1){good=false;break}if(good)rows.push(x)}return rows}
  // C_{w,L,L-1} forbids the all-one word. For each suffix h, aggregate
  // first-row weights by restriction to the intersection of rows in h.
  function disjoint(model){
    const w=Number(model.w[1]),L=model.parameters[0],rows=rowsFor(w,L),R=rows.length,U=R**(L-2),size=R*U,cache=new Map(),suffix=[];
    for(let h=0;h<U;h++){
      let t=h,mask=(1<<w)-1;for(let j=0;j<L-2;j++){mask&=rows[t%R];t=Math.floor(t/R)}
      if(!cache.has(mask)){
        const bits=[];for(let j=0;j<w;j++)if(mask&(1<<j))bits.push(j);
        const map=Int32Array.from(rows,x=>bits.reduce((a,b,k)=>a+(((x>>b)&1)<<k),0));
        cache.set(mask,{map,dim:1<<bits.length,bitCount:bits.length})
      }suffix.push(cache.get(mask))
    }
    function moments(p){
      let v=new Float64Array(size).fill(1),next=new Float64Array(size),out=[0];
      for(let n=1;n<N;n++){
        let total=0;
        for(let h=0;h<U;h++){
          const {map,dim,bitCount}=suffix[h],hist=new Float64Array(dim);
          for(let a=0;a<R;a++)hist[map[a]]+=v[a*U+h];
          for(let i=0;i<dim;i++)hist[i]%=p;
          for(let k=0;k<bitCount;k++)for(let i=0;i<dim;i++)if(i&(1<<k)){let x=hist[i]+hist[i^(1<<k)];hist[i]=x>=p?x-p:x}
          for(let a=0;a<R;a++){const x=hist[(dim-1)^map[a]];next[h*R+a]=x;total+=x}
        }
        out.push(total%p);[v,next]=[next,v]
      }return out
    }
    // Independent direct all-edge enumeration at small width for the same L.
    const small=rowsFor(Math.min(w,4),L),r=small.length,u=r**(L-2);
    let comparisons=0;
    for(let h=0;h<u;h++){let mask=(1<<Math.min(w,4))-1,t=h;for(let j=0;j<L-2;j++){mask&=small[t%r];t=Math.floor(t/r)}
      const bits=[];for(let j=0;j<Math.min(w,4);j++)if(mask&(1<<j))bits.push(j);
      const proj=x=>bits.reduce((a,b,k)=>a+(((x>>b)&1)<<k),0),d=1<<bits.length,weight=small.map((_,i)=>BigInt(1+i*i+h)),hist=Array(d).fill(0n);
      for(let j=0;j<r;j++)hist[proj(small[j])]+=weight[j];
      for(let k=0;k<bits.length;k++)for(let j=0;j<d;j++)if(j&(1<<k))hist[j]+=hist[j^(1<<k)];
      for(const c of small){let ref=0n;for(let j=0;j<r;j++)if(!(small[j]&mask&c))ref+=weight[j];check(ref===hist[(d-1)^proj(c)],"subset-zeta control");comparisons++}
    }
    checks.specializedControls+=comparisons;
    return {method:"suffix-intersection subset zeta",rawStates:size,realizationDimension:size,horizontalRows:R,suffixCount:U,distinctSuffixMasks:cache.size,moments}
  }
  function quotient(model){
    const q=compressSparse(model,{maxRows:4096,maxStates:50000,maxEdges:1500000});
    check(!q.status,"unexpected sparse quotient deferral "+JSON.stringify(q));
    const {states:S,weights,quotient}=q;
    const starts=new Int32Array(S+1),dest=[],mult=[];
    for(let j=0;j<S;j++){starts[j]=dest.length;for(const [k,c] of quotient[j]){dest.push(k);mult.push(c)}}starts[S]=dest.length;
    const to=Int32Array.from(dest),count=Int32Array.from(mult),W=Int32Array.from(weights);
    function moments(p){
      let v=new Float64Array(S).fill(1),next=new Float64Array(S),out=[0];
      for(let n=1;n<N;n++){
        let t=0;for(let j=0;j<S;j++){let x=0;for(let i=starts[j];i<starts[j+1];i++)x+=count[i]*v[to[i]];x%=p;next[j]=x;t+=W[j]*x}
        out.push(t%p);[v,next]=[next,v]
      }return out
    }
    // Exact first moment from original edge count; independent of recurrence.
    const edgeCheck=weights.reduce((a,w,j)=>a+BigInt(w)*quotient[j].reduce((s,e)=>s+BigInt(e[1]),0n),0n);
    check(edgeCheck===BigInt(q.rawEdges),"edge count mismatch");checks.exactSparseFirstTermChecks++;
    return {method:"sparse equitable quotient",rawStates:q.raw,realizationDimension:S,quotientEdges:q.edges,rawEdges:q.rawEdges,moments}
  }
  for(const d of prior.deferred){
    const model=models[d.id];check(model&&model.w[0]==="const","invalid deferred model");
    if(model.kind==="B"&&model.parameters[0]===4){spectral.push({id:d.id,width:Number(model.w[1]),rawStates:4**Number(model.w[1]),method:"Perron growth separation"});continue}
    const spec=model.kind==="C"&&model.parameters[1]===model.parameters[0]-1?disjoint(model):quotient(model);
    const {moments,...descriptor}=spec;
    const residues=Object.fromEntries(primes.map(p=>[String(p),moments(p)]));
    for(const n of [1,2]){
      let expected;try{expected=BigInt(engine.value(model,n))}catch(e){if(!String(e.message).includes("work limit"))throw e;checks.resourceSkipped++;continue}
      for(const p of primes)check(residues[p][n]===Number(expected%BigInt(p)),"array evaluator disagreement "+d.id+" "+n);
      checks.independentArrayComparisons++
    }
    records.push({id:d.id,offset:1,...descriptor,residues})
  }
  check(records.length===14&&spectral.length===4,"deferred inventory mismatch");
  return {schemaVersion:1,author:"Komorebi P.",scope:"Compact all-index finite-state rational realizations for the remaining fixed-width arrays. Residues are exact finite-field moments, used only for independence witnesses. No claim of expanded scalar denominator or minimal realization dimension.",report:{compactBinaryModels:records.length,spectralQuaternaryModels:spectral.length,coefficientCount:N,primes,...checks},records,spectral}
}
module.exports={compileCompactDeferred};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas'),read=f=>fs.readFileSync(path.join(dir,f),'utf8');const out=compileCompactDeferred(read('OEIS_168_Array_Formulas.md'),require('../website/assets/graph-array-evaluator.js'),JSON.parse(read('FIXED_STATE_ARRAY_RATIONAL_V3.json')),require('./graph_array_sparse_quotient.js').compressSparse);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
