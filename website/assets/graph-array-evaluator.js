/* Author: Komorebi P. Exact constrained-array evaluator. All arithmetic on counts uses BigInt. */
function arrayEngine(){
  'use strict';
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const limit=()=>{throw Error("This exact calculation exceeds the browser work limit. Use a smaller index or the archived formula offline.")};
  function parseExpression(source){
    const cleaned=source.replace(/\\begin\{aligned\}|\\end\{aligned\}|\\\\\[-1pt\]|\\quad|\\bigl|\\bigr|\\,|\\times|&|\s/g,"").replace(/\\mathcalI/g,"I").replace(/\\binom/g,"binom");
    const re=/binom|[0-9]+|[hk]_[ij]|[nhkijFI]|[{}()+^_]/gy,t=[];
    while(re.lastIndex<cleaned.length){const start=re.lastIndex,m=re.exec(cleaned);check(m,"Unexpected expression syntax at "+cleaned.slice(start,start+40));t.push(m[0])}
    let p=0;const pop=x=>{check(t[p]===x,"Expected "+x+"; found "+t[p]);p++};
    const atomStart=x=>x!==undefined&&/^(?:binom|\d+|[nhkijFI]|[hk]_[ij]|\(|\{)$/.test(x);
    function group(){const x=t[p];check(x==="("||x==="{","Expected group");p++;const a=sum();pop(x==="("?")":"}");return a}
    function atom(){
      const x=t[p++];check(x!==undefined,"Missing expression atom");
      if(x==="("||x==="{"){p--;return group()}
      if(x==="binom")return ["choose",group(),group()];
      if(x==="F"){pop("_");return ["fib",group()]}
      if(x==="I"){pop("_");const w=group();pop("^");const d=group();return ["ind",w,d,group()]}
      if(/^\d+$/.test(x))return ["const",x];
      check(/^(?:[nhkij]|[hk]_[ij])$/.test(x),"Unexpected atom "+x);return ["var",x];
    }
    function power(){const a=atom();if(t[p]!=="^")return a;p++;return ["pow",a,t[p]==="{"?group():atom()]}
    function product(){let a=power();while(atomStart(t[p]))a=["mul",a,power()];return a}
    function sum(){let a=product();while(t[p]==="+"){p++;a=["add",a,product()]}return a}
    const a=sum();check(p===t.length,"Unparsed expression suffix "+t.slice(p));return a
  }
  function parseRecord(id,body){
    const m=body.match(/\\\[a\(n\)=([\s\S]*?)\\\]/);
    check(m,"Missing array formula "+id);const s=m[1];
    if(s.includes("\\mathbf1")){
      const a=s.match(/^\\mathbf1\^T\\bigl\(\\mathcal ([ABC])_\{([^}]+)\}(?:\^\{\((\d);([01,]+)\)\})?\\bigr\)\^\{([ni])\}\\mathbf1$/);
      check(a,"Unrecognized matrix formula "+id);
      const [,kind,args,d,words,exponent]=a;
      if(kind==="A"){
        check(d!==undefined&&words,"Missing forbidden words");
        const patterns=words.split(",");check(patterns.every(x=>x.length===patterns[0].length),"Pattern length mismatch");
        return {kind,w:parseExpression(args),exponent,diagonal:Number(d),patterns};
      }
      const fields=args.split(",");check(fields.length===3&&fields.slice(1).every(x=>/^\d+$/.test(x))&&!words,"Invalid matrix parameters");
      return {kind,w:parseExpression(fields[0]),exponent,parameters:fields.slice(1).map(Number)};
    }
    return {kind:"reduced",expr:parseExpression(s)}
  }
  function envFor(n){
    check(Number.isSafeInteger(n)&&n>=1&&n<=10000,"Enter an integer index from 1 to 10000.");
    let ell=1;while(ell*(ell+1)/2<n)ell++;
    const i=n-ell*(ell-1)/2,j=ell+1-i,h=t=>1+Math.floor(t/2),k=t=>1+Math.ceil(t/2);
    return Object.fromEntries(Object.entries({n,i,j,h:h(n),k:k(n),h_i:h(i),k_i:k(i),h_j:h(j),k_j:k(j)}).map(([a,b])=>[a,BigInt(b)]))
  }
  function value(model,n,workLimit=3000000){
    const env=envFor(n);let work=0;
    const tick=(x=1)=>{work+=x;if(work>workLimit)limit()};
    function number(x,max=10002){check(typeof x==="bigint"&&x>=0n,"Invalid nonnegative parameter");if(x>BigInt(max))limit();return Number(x)}
    function choose(a,b){check(a>=0n&&b>=0n&&b<=a,"Invalid binomial");if(b>a-b)b=a-b;number(b,10000);let z=1n;for(let i=1n;i<=b;i++){tick();z=z*(a-b+i)/i}return z}
    function fib(a){let k=number(a),x=0n,y=1n;while(k--){tick();[x,y]=[y,x+y]}return x}
    const oriented=(w,h)=>w>h?[h,w]:[w,h];
    function ind(w,h,d){
      check(d===0||d===1,"Invalid diagonal flag");
      [w,h]=oriented(w,h);if(w===0)return 1n;if(w>12||w*h>20000)limit();
      const masks=[];for(let a=0;a<2**w;a++){tick();if(!(a&(a<<1)))masks.push(a)}
      const edges=masks.map(a=>masks.map((b,j)=>{tick();return !(a&b)&&(!d||!((a<<1)&b))?j:-1}).filter(j=>j>=0));
      let counts=Array(masks.length).fill(1n);
      for(let i=1;i<h;i++){const next=Array(masks.length).fill(0n);for(let a=0;a<masks.length;a++)if(counts[a])for(const b of edges[a]){tick();next[b]+=counts[a]}counts=next}
      return counts.reduce((a,b)=>a+b,0n)
    }
    function evalExpr(a){
      const [op,x,y,z]=a;
      if(op==="const")return BigInt(x);
      if(op==="var"){check(env[x]!==undefined,"Unknown variable");return env[x]}
      if(op==="fib")return fib(evalExpr(x));
      if(op==="ind")return ind(number(evalExpr(x)),number(evalExpr(z)),number(evalExpr(y),1));
      if(op==="add")return evalExpr(x)+evalExpr(y);
      if(op==="mul")return evalExpr(x)*evalExpr(y);
      if(op==="pow")return evalExpr(x)**BigInt(number(evalExpr(y),16));
      if(op==="choose")return choose(evalExpr(x),evalExpr(y));
      throw Error("Unknown exact expression operator");
    }
    function rowsOf(w,b,ok){
      if(w>20||b**w>4096)limit();
      const out=[];for(let a=0;a<b**w;a++){tick(w);let k=a,r=[];for(let j=0;j<w;j++){r.push(k%b);k=Math.floor(k/b)}if(ok(r))out.push(r)}return out
    }
    function block(w,h,b,t){
      [w,h]=oriented(w,h);if(w*h>20000)limit();
      const rows=rowsOf(w,b,()=>true),N=rows.length;if(h===1)return BigInt(N);
      const edges=rows.map(a=>rows.map((v,j)=>{tick(w);for(let k=0;k<w-1;k++)if(a[k]+a[k+1]+v[k]+v[k+1]<t)return -1;return j}).filter(j=>j>=0));
      let counts=Array(N).fill(1n);
      for(let i=1;i<h;i++){const next=Array(N).fill(0n);for(let a=0;a<N;a++)if(counts[a])for(const b of edges[a]){tick();next[b]+=counts[a]}counts=next}
      return counts.reduce((a,b)=>a+b,0n)
    }
    function words(w,h,patterns,d){
      [w,h]=oriented(w,h);const L=patterns[0].length,forbidden=new Set(patterns);
      check((L===3||L===4)&&(d===0||d===1),"Unsupported window");
      if(w*h>20000)limit();
      const bad=(r,start)=>forbidden.has(r.slice(start,start+L).join(""));
      const rows=rowsOf(w,2,r=>{for(let i=0;i<=w-L;i++)if(bad(r,i))return false;return true}),N=rows.length;
      if(h<L)return BigInt(N)**BigInt(h);
      if(!N)return 0n;
      if(N**(L-1)>Number.MAX_SAFE_INTEGER)limit();
      let states=new Map([[0,1n]]);
      const mod=N**(L-2);
      for(let y=0;y<h;y++){
        const next=new Map();
        for(const [code,count] of states){
          const prev=[];let c=code;
          for(let j=0;j<Math.min(y,L-1);j++){prev.unshift(rows[c%N]);c=Math.floor(c/N)}
          for(let i=0;i<N;i++){
            tick(w*(d?2:1));const r=rows[i];let good=true;
            if(y>=L-1){const stack=[...prev,r];
              for(let col=0;col<w;col++){let s="";for(let k=0;k<L;k++)s+=stack[k][col];if(forbidden.has(s)){good=false;break}}
              if(good&&d)for(let col=0;col<=w-L;col++){let s="";for(let k=0;k<L;k++)s+=stack[k][col+k];if(forbidden.has(s)){good=false;break}}
            }
            if(good){const key=(code%mod)*N+i;next.set(key,(next.get(key)??0n)+count);if(next.size>50000)limit()}
          }
        }
        states=next;if(!states.size)return 0n
      }
      let count=0n;for(const v of states.values())count+=v;return count
    }
    if(model.kind==="reduced")return evalExpr(model.expr).toString();
    const w=number(evalExpr(model.w)),m=number(env[model.exponent]);
    if(model.kind==="B")return block(w,m+1,...model.parameters).toString();
    if(model.kind==="A")return words(w,m+model.patterns[0].length-1,model.patterns,model.diagonal).toString();
    if(model.kind==="C"){const [L,K]=model.parameters,p=[];for(let a=0;a<2**L;a++){const s=a.toString(2).padStart(L,"0");if([...s].filter(x=>x==="1").length>K)p.push(s)}return words(w,m+L-1,p,0).toString()}
    throw Error("Unknown array model");
  }
  function compile(raw){
    const result={};for(const m of raw.matchAll(/^### (A\d{6})(?: \*)?\s*\n([\s\S]*?)(?=^### A\d{6}|^## |$(?![\s\S]))/gm)){check(!result[m[1]],"Duplicate array record");result[m[1]]=parseRecord(m[1],m[2])}
    check(Object.keys(result).length===168,"Array inventory mismatch");return result;
  }
  return {compile,parseRecord,value}
}
const graphArrayEngine=arrayEngine();
if(typeof module!=='undefined'&&module.exports)module.exports=graphArrayEngine;
if(typeof window!=='undefined')window.graphArrayEngine=graphArrayEngine;
