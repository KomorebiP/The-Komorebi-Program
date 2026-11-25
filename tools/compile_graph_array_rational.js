/* Author: Komorebi P. Certified fixed-width array and graph-walk rational functions.
 * Run: node tools/compile_graph_array_rational.js [output.json]
 * Strip residuals plus Cayley-Hamilton certify all indices. Symmetric powers,
 * tensor products, Newton identities and exact gcd reconstruction certify
 * the explicit rational functions and reduced denominators.
 */
'use strict';
function compileFixed(raw,engine,supplement){
  const check=(a,m)=>{if(!a)throw Error(m)};
  const trim=a=>{while(a.length>1&&a.at(-1)===0n)a.pop();return a};
  const mul=(a,b)=>{const c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]+=a[i]*b[j];return trim(c)};
  function power(a,k){let b=[1n];while(k--)b=mul(b,a);return b}
  const evenExpand=a=>a.flatMap((v,i)=>i===a.length-1?[v]:[v,0n]);
  const choose=(n,k)=>{let c=1n;for(let j=1;j<=k;j++)c=c*BigInt(n-k+j)/BigInt(j);return c};
  const parseList=s=>s.slice(1,-1).split(",").map(BigInt);
  const strips=new Map();let stripChecks=0;
  for(const m of raw.matchAll(/^### d=(\d), w=(\d+)\nP: `(\[[^\n]+\])`\nQ: `(\[[^\n]+\])`/gm)){
    const d=Number(m[1]),w=Number(m[2]),P=parseList(m[3]),Q=parseList(m[4]),r=Q.length-1;
    check(Q[0]===1n&&P.length<=r,"nonproper strip function");
    const masks=[];for(let a=0;a<2**w;a++)if(!(a&(a<<1)))masks.push(a);
    const neighbors=masks.map(a=>masks.map((b,j)=>!(a&b)&&(!d||!((a<<1)&b))?j:-1).filter(j=>j>=0));
    let v=Array(masks.length).fill(0n);v[0]=1n;let a=[];
    for(let n=0;n<r+masks.length;n++){
      a.push(v.reduce((x,y)=>x+y,0n));let x=a[n];for(let k=1;k<=Math.min(r,n);k++)x+=Q[k]*a[n-k];
      check(x===(P[n]??0n),"strip residual "+d+","+w+","+n);stripChecks++;
      const next=Array(masks.length).fill(0n);for(let j=0;j<v.length;j++)if(v[j])for(const k of neighbors[j])next[k]+=v[j];v=next;
    }
    strips.set(d+","+w,{P,Q,a,states:masks.length});
  }
  check(strips.size===18,"strip count");
  function I(d,w,n){const s=strips.get(d+","+w);check(s,"missing strip");while(s.a.length<=n){const j=s.a.length;let x=s.P[j]??0n;for(let k=1;k<s.Q.length;k++)x-=s.Q[k]*s.a[j-k];s.a.push(x)}return s.a[n]}
  const fibs=[0n,1n];function F(n){while(fibs.length<=n)fibs.push(fibs.at(-1)+fibs.at(-2));return fibs[n]}
  function evalReduced(model,n){
    const h=1+Math.floor(n/2),k=1+Math.ceil(n/2),env={n,h,k};
    function ev(a){const [op,x,y,z]=a;if(op==="const")return BigInt(x);if(op==="var")return BigInt(env[x]);if(op==="add")return ev(x)+ev(y);if(op==="mul")return ev(x)*ev(y);if(op==="pow")return ev(x)**ev(y);if(op==="choose")return choose(Number(ev(x)),Number(ev(y)));if(op==="fib")return F(Number(ev(x)));if(op==="ind")return I(Number(ev(y)),Number(ev(x)),Number(ev(z)));throw Error("unknown expression")}
    return ev(model.expr);
  }
  function sums(Q,N){const s=[BigInt(Q.length-1)];for(let m=1;m<=N;m++){let x=m<Q.length?BigInt(m)*Q[m]:0n;for(let j=1;j<=Math.min(m-1,Q.length-1);j++)x+=Q[j]*s[m-j];s.push(-x)}return s}
  function fromSums(s,N){const q=[1n];for(let m=1;m<=N;m++){let x=0n;for(let j=1;j<=m;j++)x+=q[m-j]*s[j];check(x%BigInt(m)===0n,"Newton nonintegrality");q.push(-x/BigInt(m))}check(q.at(-1)!==0n,"unexpected zero eigenvalue");return q}
  function symmetricSums(Q,k,N){const s=sums(Q,k*N),result=[choose(Q.length-2+k,k)];for(let j=1;j<=N;j++){const h=[1n];for(let m=1;m<=k;m++){let x=0n;for(let a=1;a<=m;a++)x+=s[a*j]*h[m-a];check(x%BigInt(m)===0n,"symmetric Newton nonintegrality");h.push(x/BigInt(m))}result.push(h[k])}return result}
  function productDen(factors){const N=factors.reduce((a,f)=>a*Number(choose(f.Q.length-2+f.power,f.power)),1);
    const p=Array(N+1).fill(1n);for(const f of factors){const s=symmetricSums(f.Q,f.power,N);for(let j=0;j<=N;j++)p[j]*=s[j]}return fromSums(p,N)
  }
  const primes=[1000003,1000033,1000037,1000039,1000081,1000099,1000117,1000121,1000133,1000151,1000159,1000171,1000183,1000187,1000193,1000199];
  function inv(a,p){let u=1,v=0,b=p;while(b){const q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"nonunit");return ((u%p)+p)%p}
  function modGcd(P,Q,p){
    const mod=x=>((x%p)+p)%p,big=BigInt(p),conv=a=>a.map(x=>Number((x%big+big)%big)),clean=a=>{while(a.length>1&&!a.at(-1))a.pop();return a};
    let a=clean(conv(P)),b=clean(conv(Q));if(b.length!==Q.length||a.length!==P.length)return null;
    while(b.some(x=>x)){const r=a.slice(),v=inv(b.at(-1),p);for(let i=r.length-b.length;i>=0;i--){const c=mod(r[i+b.length-1]*v);for(let j=0;j<b.length;j++)r[i+j]=mod(r[i+j]-c*b[j])}a=b;b=clean(r)}
    if(!a[0])return null;const t=inv(a[0],p);return a.map(x=>mod(x*t))
  }
  function divide(A,B){
    if(B[0]!==1n||A.length<B.length)return null;
    const q=Array(A.length-B.length+1).fill(0n);
    for(let i=0;i<q.length;i++){let v=A[i];for(let j=1;j<=Math.min(i,B.length-1);j++)v-=B[j]*q[i-j];q[i]=v}
    const a=mul(q,B);return a.length===A.length&&a.every((x,i)=>x===A[i])?q:null
  }
  function reduce(P,Q){
    let M=1n,coeff=null,degree=Infinity;
    for(const p of primes){
      for(let j=2;j*j<=p;j++)check(p%j!==0,"nonprime modulus");
      const g=modGcd(P,Q,p);if(!g||g.length-1>degree)continue;
      if(g.length===1)return {P,Q,cancelled:[1n],prime:p};
      if(g.length-1<degree){degree=g.length-1;M=1n;coeff=Array(g.length).fill(0n)}
      const big=BigInt(p),i=BigInt(inv(Number(M%big),p));
      for(let j=0;j<coeff.length;j++)coeff[j]+=M*((((BigInt(g[j])-coeff[j]%big)*i)%big+big)%big);
      M*=big;const candidate=coeff.map(x=>x>M/2n?x-M:x);
      const a=divide(P,candidate),b=divide(Q,candidate);if(!a||!b)continue;
      const remaining=modGcd(a,b,p);if(remaining&&remaining.length===1)return {P:a,Q:b,cancelled:candidate,prime:p};
    }
    throw Error("gcd reconstruction not certified");
  }
  let referenceChecks=0,coefficientChecks=0;
  function make(id,offset,q,dimension,term,kind,descriptor){
    const bound=q.length-1,stop=offset+bound+12,terms=[];for(let n=0;n<=stop;n++)terms.push(n<offset?0n:term(n));
    const P=[];for(let n=0;n<=stop;n++){let x=0n;for(let j=0;j<=Math.min(bound,n);j++)x+=q[j]*terms[n-j];if(n<offset+bound)P.push(x);else{check(x===0n,"recurrence residual "+id+" "+n);coefficientChecks++}}
    const r=reduce(trim(P),q);
    return {id,offset,kind,descriptor,universalOrder:dimension,denominatorDegree:r.Q.length-1,minimalOrderCertified:true,coprimeWitnessPrime:r.prime,cancelledFactor:r.cancelled.map(String),numerator:r.P.map(String),denominator:r.Q.map(String)};
  }
  const models=engine.compile(raw),explicit=[],compact=[];
  const records=[...raw.matchAll(/^### (A\d{6})(?: \*)?\s*\n([\s\S]*?)(?=^### A\d{6}|^## |$(?![\s\S]))/gm)].filter(x=>x[2].includes("fixed width")&&!x[2].includes("Finite-state transfer.")&&!x[2].includes("Block transfer."));
  for(const [,id,body] of records){
    const w=Number(body.match(/fixed width (\d+)/)[1]),model=models[id];check(model.kind==="reduced","not reduced");
    for(let n=1;n<=3;n++){check(String(evalReduced(model,n))===engine.value(model,n),"independent evaluator mismatch "+id);referenceChecks++}
    let q,kind,dim,descriptor;
    if(body.includes("Elementary binomial formula")){
      kind="polynomial";dim=w+1;q=power([1n,-1n],dim);descriptor={width:w,degree:w};
    }else if(id>="A202093"&&id<="A202099"){
      kind="parity-polynomial";dim=2*(2*w+1);q=evenExpand(power([1n,-1n],2*w+1));descriptor={width:w,laneDegree:2*w};
    }else if(body.includes("Boundary factorization")){
      const d=id>="A202594"?0:1,r=w-1,s=strips.get(d+","+r);
      kind="fibonacci-strip-product";dim=2*(s.Q.length-1);descriptor={width:w,diagonal:d,stripWidth:r,stripOrder:s.Q.length-1};
      q=productDen([{Q:[1n,-1n,-1n],power:1},{Q:s.Q,power:1}]);
    }else{
      const d=id>="A202485"?1:0,u=Math.floor(w/2),v=Math.ceil(w/2);
      const factors=u===v?[{Q:strips.get(d+","+u).Q,power:4,width:u}]:[{Q:strips.get(d+","+u).Q,power:2,width:u},{Q:strips.get(d+","+v).Q,power:2,width:v}];
      const N=factors.reduce((a,f)=>a*Number(choose(f.Q.length-2+f.power,f.power)),1);
      kind="parity-symmetric-tensor";dim=2*N;descriptor={width:w,diagonal:d,laneDimension:N,factors:factors.map(f=>({width:f.width,power:f.power,stripOrder:f.Q.length-1}))};
      if(N>400){compact.push({id,offset:1,kind,descriptor,universalOrder:dim,reason:"Expansion exceeds the retained 400-dimensional lane threshold. Exact symmetric-power tensor recurrence is specified."});continue}
      q=evenExpand(productDen(factors));
    }
    explicit.push(make(id,1,q,dim,n=>evalReduced(model,n),kind,descriptor));
  }
  function walkQ(n,adj,square=false){
    let A=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>adj(i,j)?1n:0n));
    function matmul(a,b){return a.map(r=>b[0].map((_,j)=>r.reduce((s,x,k)=>s+x*b[k][j],0n)))}
    if(square)A=matmul(A,A);let T=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?1n:0n)),s=[BigInt(n)];
    for(let k=1;k<=n;k++){T=matmul(T,A);s.push(T.reduce((a,r,i)=>a+r[i],0n))}
    const q=[1n];for(let m=1;m<=n;m++){let x=0n;for(let j=1;j<=m;j++)x+=q[m-j]*s[j];check(x%BigInt(m)===0n,"walk Newton nonintegrality");q.push(-x/BigInt(m))}return q
  }
  const walks=[
    ["A094233",0,walkQ(9,(i,j)=>Math.abs(i-j)===1||Math.abs(i-j)===8)],
    ["A005023",1,walkQ(8,(i,j)=>Math.abs(i-j)===1,true)],
    ["A095933",2,mul([1n,-4n],[1n,-3n,1n])],
    ["A226493",1,mul([1n,-3n],[1n,1n])]
  ];
  for(const [id,offset,q] of walks)explicit.push(make(id,offset,q,q.length-1,n=>BigInt(supplement.value(id,n)),"graph-walk",{}));
  check(records.length===40,"fixed reduced count");
  return {schemaVersion:1,author:"Komorebi P.",scope:"All-index rational identities for retained definitions, zero padded before original offsets. No new OEIS matches or priority claims. Universal tensor orders are bounds; explicit reduced denominator degrees are certified minimal eventual scalar recurrence orders.",report:{fixedReducedArrayModels:records.length,explicitArrayModels:explicit.length-4,compactArrayModels:compact.length,explicitWalkModels:4,stripAllIndexCertificates:strips.size,stripResidualChecks:stripChecks,independentArrayChecks:referenceChecks,recurrenceResidualChecks:coefficientChecks,minimalDenominatorsCertified:explicit.length},stripModels:[...strips].map(([key,s])=>({diagonal:Number(key[0]),width:Number(key.slice(2)),numerator:s.P.map(String),denominator:s.Q.map(String),stateDimension:s.states})),explicit,compact};
}
module.exports={compileFixed};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const raw=fs.readFileSync(path.join(__dirname,'..','research','graph-formula-atlas','OEIS_168_Array_Formulas.md'),'utf8');const engine=require('../website/assets/graph-array-evaluator.js'),supplement=require('../website/assets/graph-supplement-evaluator.js');const out=compileFixed(raw,engine,supplement);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
