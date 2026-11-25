/* Author: Komorebi P. Exact enlarged constant rational transfer basis. */
'use strict';
function enlarge(data,basis,fixed,arrayModels){
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a};
  const mul=(a,b)=>{const c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]+=a[i]*b[j];return c};
  function div(a,b){check(a.length>=b.length,"division degree");const c=a.slice(),q=Array(a.length-b.length+1).fill(0n);for(let i=q.length-1;i>=0;i--){check(c[i+b.length-1]%b.at(-1)===0n,"nonintegral quotient");q[i]=c[i+b.length-1]/b.at(-1);for(let j=0;j<b.length;j++)c[i+j]-=q[i]*b[j]}check(!c.some(x=>x),"nonexact quotient");return q}
  const phis=new Map();function phi(d){if(!phis.has(d)){let q=[1n,...Array(d-1).fill(0n),-1n];for(let i=1;i<d;i++)if(d%i===0)q=div(q,phi(i));phis.set(d,q)}return phis.get(d)}
  const byId=new Map(data.coreModels.map(m=>[m.id,m]));
  function rational(m){let q=[1n];for(const [d,e] of m.cyclotomicFactors)for(let j=0;j<e;j++)q=mul(q,phi(d));return {id:m.id,P:[...Array(m.numeratorShift).fill(0n),...m.numerator.map(BigInt)],Q:q}}
  const original=basis.basis.map(id=>rational(byId.get(id)));
  const explicit=fixed.explicit.map(m=>({id:m.id,P:m.numerator.map(BigInt),Q:m.denominator.map(BigInt)}));
  const compact=fixed.compact.map(m=>({id:m.id,expr:arrayModels[m.id].expr}));
  const all=[...original,...explicit,...compact],ids0=original.map(m=>m.id),N=800;
  const strips=new Map(fixed.stripModels.map(m=>[m.diagonal+","+m.width,{P:m.numerator.map(BigInt),Q:m.denominator.map(BigInt)}]));
  let common=[1n];for(const [d,e] of basis.commonCyclotomicFactors)for(let i=0;i<e;i++)common=mul(common,phi(d));
  const polys=new Map(original.map(m=>[m.id,mul(m.P,div(common,m.Q))]));
  const baseDim=Math.max(...[...polys.values()].map(a=>a.length));
  function modular(models,p,N){
    check(Number.isSafeInteger(p*p),"modulus too large");for(let i=2;i*i<=p;i++)check(p%i!==0,"nonprime");
    const big=BigInt(p),mod=x=>((x%p)+p)%p,cv=x=>Number((x%big+big)%big);
    const inv=a=>{let u=1,v=0,b=p;while(b){const q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"nonunit");return mod(u)};
    function seq(P,Q,N){P=P.map(cv);Q=Q.map(cv);const a=new Float64Array(N);check(Q[0]===1,"denominator normalization");for(let n=0;n<N;n++){let t=P[n]||0;for(let k=1;k<Math.min(Q.length,n+1);k++)if(Q[k])t=mod(t-Q[k]*a[n-k]);a[n]=t}return a}
    const stripSeq=new Map([...strips].map(([k,s])=>[k,seq(s.P,s.Q,N+4)]));
    function evalCompact(expr,n){if(n===0)return 0;const env={n,h:1+Math.floor(n/2),k:1+Math.ceil(n/2)};
      function ev(a){const [op,x,y,z]=a;if(op==="var")return env[x];if(op==="const")return Number(x);if(op==="ind")return stripSeq.get(ev(y)+","+ev(x))[ev(z)];if(op==="mul")return mod(ev(x)*ev(y));if(op==="pow"){let r=1,b=ev(x),k=ev(y);while(k--)r=mod(r*b);return r}if(op==="add")return mod(ev(x)+ev(y));throw Error("unsupported compact expression")}
      return ev(expr)}
    const bases=[],pivots=[],repr=[],ids=[],deps=[];
    for(const m of models){
      const a=m.expr?Float64Array.from({length:N},(_,n)=>evalCompact(m.expr,n)):seq(m.P,m.Q,N),acc=new Float64Array(models.length);
      for(let j=0;j<pivots.length;j++){const col=pivots[j],c=a[col];if(c){for(let k=col;k<N;k++)a[k]=mod(a[k]-c*bases[j][k]);for(let k=0;k<ids.length;k++)acc[k]=mod(acc[k]+c*repr[j][k])}}
      const col=a.findIndex(x=>x!==0);
      if(col<0){deps.push({id:m.id,terms:Array.from(acc.slice(0,ids.length)).map((x,i)=>[ids[i],x]).filter(x=>x[1])});continue}
      const v=inv(a[col]);for(let k=col;k<N;k++)a[k]=mod(a[k]*v);const r=new Float64Array(models.length);for(let k=0;k<ids.length;k++)r[k]=mod(-acc[k]*v);r[ids.length]=v;ids.push(m.id);
      let pos=pivots.findIndex(k=>k>col);if(pos<0)pos=pivots.length;pivots.splice(pos,0,col);bases.splice(pos,0,a);repr.splice(pos,0,r)
    }
    return {p,ids,pivots,deps,inv}
  }
  const first=modular(all,1000003,N);
  const deps=first.deps.map(m=>m.id),targets=explicit.filter(m=>deps.includes(m.id));
  check(deps.length===targets.length,"compact dependency requires separate proof");
  for(const d of first.deps)check(d.terms.every(([id])=>ids0.includes(id)),"new-basis dependency requires separate proof");
  for(const m of targets)polys.set(m.id,mul(m.P,div(common,m.Q)));
  const dim=Math.max(baseDim,...targets.map(m=>polys.get(m.id).length));
  function verify(target,D,terms){const t=polys.get(target),r=Array(dim).fill(0n);for(const {id,multiplier} of terms){check(ids0.includes(id),"not original basis");const a=polys.get(id),c=BigInt(multiplier);for(let i=0;i<a.length;i++)if(a[i])r[i]+=c*a[i]}return r.every((x,i)=>x===D*(t[i]??0n))}
  function sqrt(n){if(n<2n)return n;let x=1n<<BigInt(Math.ceil(n.toString(2).length/2));while(true){let y=(x+n/x)>>1n;if(y>=x)return x;x=y}}
  function rat(r,M){const B=sqrt(M/2n);let a=M,b=r,u=0n,v=1n;while(b>B){if(!b)return null;const q=a/b;[a,b]=[b,a-q*b];[u,v]=[v,u-q*v]}if(v===0n)return null;if(v<0n){v=-v;b=-b}return v<=B&&gcd(b,v)===1n&&(b-r*v)%M===0n?[b,v]:null}
  const primes=[1000003,1000033,1000037,1000039,1000081,1000099,1000117,1000121,1000133,1000151,1000159,1000171,1000183,1000187,1000193,1000199];
  let M=1n,attempts=[],certs=[],crt=new Map(deps.map(id=>[id,Array(ids0.length).fill(0n)]));
  for(const p of primes){
    const r=modular([...original,...targets],p,Math.max(dim,606));
    if(r.ids.join()!==ids0.join()||r.deps.length!==deps.length){attempts.push({p,skipped:true});continue}
    const P=BigInt(p),iv=BigInt(r.inv(Number(M%P)));
    for(const d of r.deps){const v=new Map(d.terms),a=crt.get(d.id);for(let j=0;j<a.length;j++)a[j]+=M*((((BigInt(v.get(ids0[j])||0)-a[j]%P)*iv)%P+P)%P)}
    M*=P;certs=[];
    for(const [id,a] of crt){let D=1n,terms=[],valid=true;
      for(let j=0;j<a.length;j++)if(a[j]){const f=rat(a[j],M);if(!f){valid=false;break}D=D/gcd(D,f[1])*f[1];terms.push([ids0[j],...f])}
      if(!valid)continue;
      const t=terms.map(([id,n,d])=>({id,multiplier:String(n*(D/d))}));
      if(verify(id,D,t))certs.push({target:id,denominator:String(D),terms:t})
    }
    attempts.push({prime:p,modulusDigits:String(M).length,certified:certs.length});if(certs.length===deps.length)break
  }
  check(certs.length===deps.length,"incomplete exact certificates");
  const second=modular(all,1000033,N);
  check(first.ids.join()===second.ids.join(),"unstable modular basis");
  check(first.ids.length+certs.length===all.length,"dimension mismatch");
  const control=certs[0],bad=control.terms.map((r,i)=>({...r,multiplier:String(BigInt(r.multiplier)+(i===0?1n:0n))}));
  check(!verify(control.target,BigInt(control.denominator),bad),"corrupt identity accepted");
  const added=first.ids.slice(ids0.length),rows=[...basis.transferRows,...added.map(id=>({target:id,denominator:"1",terms:[{id,multiplier:"1"}]})),...certs];
  return {schemaVersion:1,author:"Komorebi P.",scope:"Constant rational linear span of 363 graph/tree core and complement models, 40 fixed-width reduced arrays, and four graph-walk functions. Original index conventions; zero padding before array/walk offsets. Compact tensor models certified by modular coefficient independence and prior finite-state realization; no expanded polynomial requirement. Not a claim about remaining atlas models or literature priority.",report:{originalModels:basis.report.totalModels,explicitAddedModels:explicit.length,compactAddedModels:compact.length,totalModels:rows.length,originalRank:ids0.length,rank:first.ids.length,newIndependentDirections:added.length,newDependentModels:certs.length,dependenceDimension:rows.length-first.ids.length,polynomialCoordinateCount:dim,negativeControlRejected:true},basis:first.ids,addedBasis:added,newDependencies:certs,transferRows:rows,witnesses:[{prime:first.p,coefficientCount:N,pivotIndices:first.pivots},{prime:second.p,coefficientCount:N,pivotIndices:second.pivots}],attempts}
}
module.exports={enlarge};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8');const g=read('Graph_288_Formulas.md'),l=read('Graph_288_Binomial_Lanes.md');require('./verify_graph_formula_atlas_exact.js').audit(g,l);const data=require('./compile_graph_atlas_transfers.js').compile(g,l);const basis=require('./compile_graph_atlas_basis.js').exactSpan(data);const engine=require('../website/assets/graph-array-evaluator.js');const raw=read('OEIS_168_Array_Formulas.md');const fixed=require('./compile_graph_array_rational.js').compileFixed(raw,engine,require('../website/assets/graph-supplement-evaluator.js'));const out=enlarge(data,basis,fixed,engine.compile(raw));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
