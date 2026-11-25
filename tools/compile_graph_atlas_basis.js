/* Author: Komorebi P. Certified rational transfer basis for the graph atlas.
 * Run: node tools/compile_graph_atlas_basis.js [output.json]
 * Modular rank provides the lower bound; every reconstructed spanning row is
 * checked over the integers after clearing the common polynomial denominator.
 * No probabilistic acceptance, floating-point coefficient approximation or
 * combinatorial priority claim. All unbounded integers are decimal strings.
 */
'use strict';
function exactSpan(data){
  const models=data.coreModels, check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const maxFactors=new Map();for(const r of models)for(const [d,e] of r.cyclotomicFactors)maxFactors.set(d,Math.max(e,maxFactors.get(d)||0));
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a};
  const mul=(a,b)=>{const c=Array(a.length+b.length-1).fill(0n);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]+=a[i]*b[j];return c};
  const polys=new Map();
  function exact(a,b){const r=a.slice(),q=Array(a.length-b.length+1).fill(0n),t=b.at(-1);for(let i=q.length-1;i>=0;i--){check(r[i+b.length-1]%t===0n,"inexact quotient");const c=r[i+b.length-1]/t;q[i]=c;for(let j=0;j<b.length;j++)r[i+j]-=c*b[j]}check(!r.some(x=>x),"nonzero remainder");return q}
  function phi(d){if(!polys.has(d)){let a=[1n,...Array(d-1).fill(0n),-1n];for(let k=1;k<d;k++)if(d%k===0)a=exact(a,phi(k));polys.set(d,a)}return polys.get(d)}
  let Q=[1n];for(const [d,e] of maxFactors)for(let i=0;i<e;i++)Q=mul(Q,phi(d));
  function numerator(r){const f=new Map(r.cyclotomicFactors);let a=[...Array(r.numeratorShift).fill(0n),...r.numerator.map(BigInt)];for(const [d,e] of f)check(e<=(maxFactors.get(d)||0),"denominator not covered");for(const [d,e] of maxFactors)for(let i=f.get(d)||0;i<e;i++)a=mul(a,phi(d));return a}
  const nums=models.map(numerator),extra=data.nonbipartiteModels.map(numerator);
  const dim=Math.max(...nums.concat(extra).map(a=>a.length));for(const a of nums.concat(extra))while(a.length<dim)a.push(0n);
  const order=models.map((r,i)=>i).sort((a,b)=>models[a].minimalEventualOrder-models[b].minimalEventualOrder||models[a].id.localeCompare(models[b].id,"en"));
  function modular(p){
    check(p>1&&Number.isSafeInteger(p*p),"unsafe modular arithmetic");
    for(let i=2;i*i<=p;i++)check(p%i!==0,"nonprime modulus");
    const P=BigInt(p),mod=x=>((x%p)+p)%p;
    const inv=a=>{let u=1,v=0,b=p;while(b){const q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"not invertible");return mod(u)};
    const basis=[],basisIds=[],dependent=new Map(),pivots=[],reps=[];
    for(const i of order){
      let row=Float64Array.from(nums[i],x=>Number((x%P+P)%P)),acc=new Float64Array(models.length);
      for(let j=0;j<pivots.length;j++){const col=pivots[j],x=row[col];if(x){const br=basis[j],rr=reps[j];for(let k=col;k<dim;k++)row[k]=mod(row[k]-x*br[k]);for(let k=0;k<basisIds.length;k++)acc[k]=mod(acc[k]+x*rr[k])}}
      let col=row.findIndex(x=>x!==0);
      if(col===-1){dependent.set(i,Array.from(acc.slice(0,basisIds.length)));continue}
      let v=inv(row[col]);for(let k=col;k<dim;k++)row[k]=mod(row[k]*v);
      let rr=new Float64Array(models.length);for(let k=0;k<basisIds.length;k++)rr[k]=mod(-acc[k]*v);rr[basisIds.length]=v;basisIds.push(i);
      let pos=pivots.findIndex(k=>k>col);if(pos<0)pos=pivots.length;pivots.splice(pos,0,col);basis.splice(pos,0,row);reps.splice(pos,0,rr)
    }
    return {basisIds,dependent,inv,pivots};
  }
  function sqrt(n){if(n<2n)return n;let x=1n<<BigInt(Math.ceil(n.toString(2).length/2));while(true){let y=(x+n/x)>>1n;if(y>=x)return x;x=y}}
  function rat(r,M){const B=sqrt(M/2n);let a=M,b=r,u=0n,v=1n;while(b>B){if(!b)return null;const q=a/b;[a,b]=[b,a-q*b];[u,v]=[v,u-q*v]}if(v===0n)return null;if(v<0n){v=-v;b=-b}if(v>B||gcd(b,v)!==1n||(b-r*v)%M!==0n)return null;return [b,v]}
  let M=1n,crts=new Map(),basisIds,certs=[],attempts=[],independenceWitness;
  const primes=[1000003,1000033,1000037,1000039,1000081,1000099,1000117,1000121,1000133,1000151,1000159,1000171,1000183,1000187,1000193,1000199];
  function verifyTerms(a,D,terms){
    const v=Array(dim).fill(0n);
    for(const [j,s] of terms){const b=nums[j];for(let k=0;k<dim;k++)if(b[k])v[k]+=s*b[k]}
    return v.every((x,k)=>x===D*a[k])
  }
  for(const p of primes){
    const P=BigInt(p),r=modular(p);
    if(!basisIds){basisIds=r.basisIds;independenceWitness={prime:p,pivotColumns:r.pivots};for(const [i,c] of r.dependent)crts.set(i,Array(c.length).fill(0n))}
    if(r.basisIds.join(",")!==basisIds.join(",")){attempts.push({p,skipped:"pivot change"});continue}
    const iv=BigInt(r.inv(Number(M%P)));
    for(const [i,c] of r.dependent){const a=crts.get(i);for(let k=0;k<a.length;k++){const q=((BigInt(c[k])-a[k]%P)*iv%P+P)%P;a[k]+=M*q}}
    M*=P;
    const failed=[];certs=[];
    for(const [i,c] of crts){
      const terms=[];let D=1n,ok=true;
      for(let k=0;k<c.length;k++)if(c[k]){const t=rat(c[k],M);if(!t){ok=false;break}terms.push([basisIds[k],...t]);D=D/gcd(D,t[1])*t[1]}
      if(!ok){failed.push(i);continue}
      const scaled=terms.map(([j,n,d])=>[j,n*(D/d)]);
      if(!verifyTerms(nums[i],D,scaled)){failed.push(i);continue}
      certs.push({target:models[i].id,denominator:String(D),terms:scaled.map(([j,s])=>({id:models[j].id,multiplier:String(s)}))})
    }
    attempts.push({p,modulusDigits:String(M).length,rank:basisIds.length,certified:certs.length,failed:failed.length});
    if(!failed.length)break
  }
  check(certs.length+basisIds.length===models.length,"incomplete exact spanning certificate");
  const basis=basisIds.map(i=>models[i].id);
  const index=new Map(models.map((m,i)=>[m.id,i]));
  const rows=new Map([...basis.map(id=>[id,{target:id,denominator:"1",terms:[{id,multiplier:"1"}]}]),...certs.map(c=>[c.target,c])]);
  const complementCertificates=[];
  for(let i=0;i<data.nonbipartiteModels.length;i++){
    const m=data.nonbipartiteModels[i],a=rows.get(m.positive),b=rows.get(m.negative);
    check(a&&b,"missing parent");
    const A=BigInt(a.denominator),B=BigInt(b.denominator);let D=A/gcd(A,B)*B;
    const c=new Map();
    for(const [r,s] of [[a,D/A],[b,-D/B]])for(const t of r.terms)c.set(t.id,(c.get(t.id)||0n)+s*BigInt(t.multiplier));
    let divisor=D;for(const v of c.values())divisor=gcd(divisor,v);
    D/=divisor;const terms=[...c].filter(([id,v])=>v!==0n).map(([id,v])=>({id,multiplier:String(v/divisor)}));
    check(verifyTerms(extra[i],D,terms.map(t=>[index.get(t.id),BigInt(t.multiplier)])),"complement certificate "+m.id);
    const row={target:m.id,denominator:String(D),terms};rows.set(m.id,row);complementCertificates.push(row)
  }
  // Reject a deliberately altered exact identity.
  const t=certs[0];const altered=t.terms.map((c,i)=>[index.get(c.id),BigInt(c.multiplier)+(i===0?1n:0n)]);
  check(!verifyTerms(nums[index.get(t.target)],BigInt(t.denominator),altered),"corrupted certificate accepted");
  return {schemaVersion:1,author:"Komorebi P.",scope:"Rational linear span of the retained core and derived nonbipartite generating functions. Does not certify combinatorial bijections, independent OEIS bindings, or computational optimality.",report:{originalModels:models.length,complementModels:extra.length,totalModels:rows.size,rank:basis.length,coreDependenceDimension:certs.length,combinedDependenceDimension:rows.size-basis.length,commonDenominatorDegree:Q.length-1,polynomialCoordinateCount:dim,negativeControlRejected:true},basis,commonCyclotomicFactors:[...maxFactors].sort((a,b)=>a[0]-b[0]),independenceWitness,attempts,transferRows:[...models.map(m=>rows.get(m.id)),...complementCertificates]};
}
module.exports={exactSpan};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const g=fs.readFileSync(path.join(dir,'Graph_288_Formulas.md'),'utf8'),l=fs.readFileSync(path.join(dir,'Graph_288_Binomial_Lanes.md'),'utf8');require('./verify_graph_formula_atlas_exact.js').audit(g,l);const data=require('./compile_graph_atlas_transfers.js').compile(g,l);const out=exactSpan(data);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out.report,null,2));}
