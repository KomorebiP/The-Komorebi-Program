/* Author: Komorebi P. Compile array formula syntax and independently check the row-transfer evaluator by a cell-frontier recurrence. */
'use strict';
function verify(engine,raw){
  const models=engine.compile(raw),limitMessage="reference limit";
  function ref(model,n){
    let i=n,j=1,s=1;while(i>s){i-=s;s++}j=s+1-i;
    const h=t=>1+Math.floor(t/2),k=t=>1+Math.ceil(t/2),env={n,i,j,h:h(n),k:k(n),h_i:h(i),k_i:k(i),h_j:h(j),k_j:k(j)};
    let work=0;
    function scan(w,H,b,D,valid){
      if(w>H)[w,H]=[H,w];
      const depth=D(w),mod=b**depth;if(!Number.isSafeInteger(mod))throw Error(limitMessage);
      const pow=Array.from({length:depth},(_,j)=>b**j);
      let states=new Map([[0,1n]]);
      for(let pos=0;pos<w*H;pos++){
        const row=Math.floor(pos/w),col=pos%w,next=new Map();
        for(const [code,count] of states){
          const prev=lag=>Math.floor(code/pow[lag-1])%b;
          for(let x=0;x<b;x++){
            if(++work>5000000)throw Error(limitMessage);
            if(valid(x,prev,row,col,w)){
              const key=(code*b+x)%mod;
              next.set(key,(next.get(key)??0n)+count);
              if(next.size>100000)throw Error(limitMessage)
            }
          }
        }
        states=next
      }
      return [...states.values()].reduce((a,b)=>a+b,0n)
    }
    const ind=(w,H,d)=>scan(w,H,2,w=>w+(d?1:0),(x,prev,r,c,w)=>!x||(!(c&&prev(1))&&!(r&&prev(w))&&!(d&&r&&c&&prev(w+1))));
    function words(w,H,patterns,d){
      const L=patterns[0].length,forbidden=new Set(patterns);
      return scan(w,H,2,w=>(L-1)*(w+(d?1:0)),(x,prev,r,c,w)=>{
        function test(step){let word="";for(let j=L-1;j>0;j--)word+=prev(j*step);return !forbidden.has(word+x)}
        return (c<L-1||test(1))&&(r<L-1||test(w))&&(!d||r<L-1||c<L-1||test(w+1))
      })
    }
    const ev=a=>{const [op,x,y,z]=a;
      if(op==="var")return BigInt(env[x]);if(op==="const")return BigInt(x);
      if(op==="add")return ev(x)+ev(y);if(op==="mul")return ev(x)*ev(y);if(op==="pow")return ev(x)**ev(y);
      if(op==="choose"){let A=Number(ev(x)),B=Number(ev(y));const row=[1n,...Array(B).fill(0n)];for(let j=1;j<=A;j++)for(let k=Math.min(B,j);k>0;k--)row[k]+=row[k-1];return row[B]}
      if(op==="fib"){let f=[0n,1n],n=Number(ev(x));for(let j=2;j<=n;j++)f[j]=f[j-1]+f[j-2];return f[n]}
      if(op==="ind")return ind(Number(ev(x)),Number(ev(z)),Number(ev(y)));
      throw Error("reference expression "+op)
    };
    if(model.kind==="reduced")return ev(model.expr).toString();
    const w=Number(ev(model.w)),m=env[model.exponent];
    if(model.kind==="B"){const [b,t]=model.parameters;return scan(w,m+1,b,w=>w+1,(x,prev,r,c,w)=>!r||!c||x+prev(1)+prev(w)+prev(w+1)>=t).toString()}
    if(model.kind==="A")return words(w,m+model.patterns[0].length-1,model.patterns,model.diagonal).toString();
    if(model.kind==="C"){const [L,K]=model.parameters,patterns=[];for(let a=0;a<2**L;a++){const s=a.toString(2).padStart(L,"0");if(s.split("1").length-1>K)patterns.push(s)}return words(w,m+L-1,patterns,0).toString()}
    throw Error("reference kind")
  }
  const firstTerms={},checks=[],limits=[],referenceLimits=[];
  for(const [id,model] of Object.entries(models))for(let n=1;n<=3;n++){
    let v;try{v=engine.value(model,n)}catch(e){if(!e.message.includes("work limit"))throw e;limits.push({id,n});continue}
    if(n===1)firstTerms[id]=v;
    let expected;try{expected=ref(model,n)}catch(e){if(e.message!==limitMessage)throw e;referenceLimits.push({id,n});continue}
    if(v!==expected)throw Error(`${id} n=${n}: ${v} != ${expected}`);
    checks.push({id,n,value:v})
  }
  if(Object.keys(firstTerms).length!==168||checks.filter(c=>c.n===1).length!==168)throw Error("Incomplete first-term audit");
  let resourceGuard=false;try{engine.value(models.A202720,2,1)}catch(e){if(!e.message.includes("work limit"))throw e;resourceGuard=true}
  let invalidIndexRejected=false;try{engine.value(models.A202092,0)}catch(e){if(!e.message.includes("integer index"))throw e;invalidIndexRejected=true}
  if(!resourceGuard||!invalidIndexRejected)throw Error("Missing negative control");
  return {schemaVersion:1,author:"Komorebi P.",scope:"Exact evaluations of retained formula definitions; independent cell-frontier comparison, not a fresh OEIS-term retrieval. Browser budgets may reject expensive inputs.",report:{models:Object.keys(models).length,reducedModels:Object.values(models).filter(m=>m.kind==="reduced").length,firstTermChecks:checks.filter(c=>c.n===1).length,independentComparisons:checks.length,browserLimits:limits.length,referenceLimits:referenceLimits.length,resourceGuard,invalidIndexRejected},models,checks,limits,referenceLimits}
}
module.exports={verify};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const engine=require('../website/assets/graph-array-evaluator.js');const raw=fs.readFileSync(path.join(__dirname,'..','research','graph-formula-atlas','OEIS_168_Array_Formulas.md'),'utf8');const result=verify(engine,raw);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result)+'\n');console.log(JSON.stringify(result.report,null,2))}
