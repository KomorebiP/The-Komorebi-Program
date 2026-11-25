/* Author: Komorebi P. Exact archived walk and labeled-graph parity formulas. */
function supplementalEngine(){
  'use strict';
  const models={
    A094233:{kind:"cycle9",min:0,max:10000},
    A005023:{kind:"path8",min:1,max:10000},
    A095933:{kind:"antipodal10",min:2,max:10000},
    A226493:{kind:"complete4",min:1,max:10000},
    A054939:{kind:"evenConnected",min:1,max:128},
    A054940:{kind:"oddConnected",min:1,max:128}
  };
  function C(n){
    let v=Array(9).fill(0n);v[0]=1n;
    for(let k=0;k<n;k++)v=v.map((_,i)=>v[(i+1)%9]+v[(i+8)%9]);
    return v[0];
  }
  function lucas(m){let a=2n,b=1n;for(let j=0;j<m;j++)[a,b]=[b,a+b];return a}
  function choose(n,k){let c=1n;for(let j=1;j<=k;j++)c=c*BigInt(n-k+j)/BigInt(j);return c}
  function total(n){return 1n<<BigInt(n*(n-1)/2)}
  function connected(n){
    const a=[0n];
    for(let m=1;m<=n;m++){
      let c=total(m);
      for(let k=1;k<m;k++)c-=choose(m-1,k-1)*a[k]*total(m-k);
      a.push(c)
    }
    return a[n]
  }
  function value(id,n){
    const m=models[id];
    if(!m||!Number.isSafeInteger(n)||n<m.min||n>m.max)throw Error(m?`Enter an integer index from ${m.min} to ${m.max}.`:"Unknown graph formula");
    let a;
    switch(m.kind){
      case "cycle9":a=C(n);break;
      case "path8":a=(C(2*n+9)-4n*C(2*n+7))/2n;break;
      case "antipodal10":a=2n*(4n**BigInt(n)-lucas(2*n+1))/5n;break;
      case "complete4":a=3n**BigInt(n)+(n%2?-3n:3n);break;
      default:{
        let f=1n;for(let k=1;k<n;k++)f*=BigInt(k);
        if(!(n%2))f=-f;
        const c=connected(n);
        a=(c+(m.kind==="evenConnected"?f:-f))/2n;
      }
    }
    return a.toString()
  }
  function verify(){
    const rows=[];
    function walk(size,start,stop,len,adj){
      let a=Array(size).fill(0n);a[start]=1n;
      for(let i=0;i<len;i++){
        const b=Array(size).fill(0n);
        for(let j=0;j<size;j++)for(let k=0;k<size;k++)if(adj(j,k))b[k]+=a[j];
        a=b
      }
      return a[stop]
    }
    function compare(id,n,expected){
      const actual=value(id,n);if(actual!==String(expected))throw Error(`${id}(${n}): ${actual} != ${expected}`);
      rows.push({id,n,value:actual})
    }
    for(let n=0;n<16;n++)compare("A094233",n,walk(9,0,0,n,(a,b)=>Math.abs(a-b)===1||Math.abs(a-b)===8));
    for(let n=1;n<=16;n++)compare("A005023",n,walk(8,0,7,2*n+7,(a,b)=>Math.abs(a-b)===1));
    for(let n=2;n<18;n++)compare("A095933",n,walk(10,0,5,2*n+1,(a,b)=>Math.abs(a-b)===1||Math.abs(a-b)===9));
    for(let n=1;n<=16;n++){let t=0n;for(let j=0;j<4;j++)t+=walk(4,j,j,n,(a,b)=>a!==b);compare("A226493",n,t)}
    for(let n=1;n<=6;n++){
      const edges=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)edges.push([i,j]);
      const counts=[0n,0n];
      for(let mask=0;mask<2**edges.length;mask++){
        const adj=Array(n).fill(0);let parity=0;
        edges.forEach(([i,j],k)=>{if(mask&(1<<k)){adj[i]|=1<<j;adj[j]|=1<<i;parity^=1}});
        let reached=1,old=0;
        while(old!==reached){old=reached;for(let i=0;i<n;i++)if(old&(1<<i))reached|=adj[i]}
        if(reached===(1<<n)-1)counts[parity]++
      }
      compare("A054939",n,counts[0]);compare("A054940",n,counts[1])
    }
    // Independent parity-resolved component recursion, without the signed EGF.
    const all=n=>n<2?[1n,0n]:[total(n)/2n,total(n)/2n],cp=[[0n,0n]];
    for(let n=1;n<=32;n++){
      const c=all(n);
      for(let k=1;k<n;k++){
        const b=all(n-k),s=choose(n-1,k-1);
        c[0]-=s*(cp[k][0]*b[0]+cp[k][1]*b[1]);
        c[1]-=s*(cp[k][1]*b[0]+cp[k][0]*b[1])
      }
      cp.push(c);compare("A054939",n,c[0]);compare("A054940",n,c[1])
    }
    let rejections=0;
    for(const [id,m] of Object.entries(models))for(const n of [m.min-1,m.max+1,1.5]){try{value(id,n)}catch(e){rejections++;continue}throw Error("Invalid index accepted")}
    return {models,rows,report:{models:6,walkChecks:64,exhaustiveGraphChecks:12,parityRecurrenceChecks:64,independentComparisons:rows.length,invalidIndexRejections:rejections}}
  }
  return {models,value,verify}
}
const graphSupplementEngine=supplementalEngine();
if(typeof window!=='undefined')window.graphSupplementEngine=graphSupplementEngine;
if(typeof module!=='undefined'&&module.exports){module.exports=graphSupplementEngine;if(require.main===module){const out=graphSupplementEngine.verify();if(process.argv[2])require('node:fs').writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2))}}
