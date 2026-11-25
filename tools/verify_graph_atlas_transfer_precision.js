/* Author: Komorebi P. Independent local Smith replay and exact precision-loss certificates. */
'use strict';
function precision(base,lat){
 const check=(a,m)=>{if(!a)throw Error(m)},abs=x=>x<0n?-x:x,gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 const mod=(x,m)=>{x%=m;return x<0n?x+m:x};
 function inv(a,m){let x=1n,z=0n,b=m;while(b){const q=a/b;[a,b]=[b,a-q*b];[x,z]=[z,x-q*z]}check(a===1n,"nonunit inverse");return mod(x,m)}
 const D=BigInt(lat.report.commonDenominator),d=lat.activeBasis.length,m=lat.sourceRows.length,idx=new Map(lat.activeBasis.map((v,i)=>[v,i])),row=new Map(base.transferRows.map(r=>[r.target,r]));
 const A=lat.sourceRows.map(id=>{const r=row.get(id),a=Array(d).fill(0n);for(const t of r.terms)a[idx.get(t.id)]+=BigInt(t.multiplier)*(D/BigInt(r.denominator));return a});
 const H=lat.hermite.map(r=>r.map(BigInt)),U=lat.generatorMatrix.map(r=>r.map(BigInt)),C=lat.reconstructionMatrix.map(r=>r.map(BigInt)),W=lat.oldBasisInIntegralBasis.map(r=>r.map(BigInt));
 // Independently recheck dimensions, all four matrix equations, and
 // negative controls against altered reconstruction coefficients.
 function verifyProduct(X,Y,Z){let count=0;for(let i=0;i<X.length;i++)for(let j=0;j<Y[0].length;j++){let a=0n;for(let k=0;k<Y.length;k++)if(X[i][k]&&Y[k][j])a+=X[i][k]*Y[k][j];if(a!==Z[i][j])return {ok:false,count};count++}return {ok:true,count}}
 const I=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>i===j?1n:0n)),DI=I.map(r=>r.map(v=>v*D));
 const products=[["U A = H",verifyProduct(U,A,H)],["C H = A",verifyProduct(C,H,A)],["U C = I",verifyProduct(U,C,I)],["W H = D I",verifyProduct(W,H,DI)]].map(([name,r])=>({name,...r}));
 check(products.every(r=>r.ok),"integer certificate mismatch");
 const bad=C.map(r=>r.slice());bad[0][0]+=1n;check(!verifyProduct(bad,H,A).ok,"corrupted reconstruction accepted");
 // Independent p-primary Smith test: apply unit-pivot elimination to
 // the scaled ORIGINAL rectangular matrix modulo successively smaller
 // powers of p. No HNF or W input is used in this calculation.
 function peel(A,p,e){
   let M=p**BigInt(e),a=A.map(r=>r.map(v=>mod(v,M))),hist=[],cols=d,rankTotal=0;
   for(let t=0;t<e;t++){
     let k=0;
     while(k<cols){
       let i0=-1,j0=-1;
       for(let i=k;i<a.length&&i0<0;i++)for(let j=k;j<cols;j++)if(a[i][j]%p!==0n){i0=i;j0=j;break}
       if(i0<0)break;
       [a[k],a[i0]]=[a[i0],a[k]];
       for(let i=0;i<a.length;i++)[a[i][k],a[i][j0]]=[a[i][j0],a[i][k]];
       const v=inv(a[k][k],M);for(let j=k;j<cols;j++)a[k][j]=mod(v*a[k][j],M);
       for(let i=k+1;i<a.length;i++){const q=a[i][k];if(q)for(let j=k;j<cols;j++)a[i][j]=mod(a[i][j]-q*a[k][j],M)}
       k++
     }
     hist.push(k);rankTotal+=k;
     a=a.slice(k).map(r=>r.slice(k).map(v=>{check(v%p===0n,"digit peeling failure");return v/p}));cols-=k;M/=p
   }
   hist.push(d-rankTotal);
   // A's local Smith exponents v correspond to e-v in the old-basis
   // inclusion, because D I is contained in its row lattice.
   const exps=[];for(let v=e;v>=0;v--)for(let j=0;j<hist[v];j++)exps.push(e-v);
   return {scaledOriginalValuationHistogram:hist,exps}
 }
 // Construct a primitive witness w in ker(W mod p^e) by exact row
 // and column elimination, tracking the invertible column transform.
 function witness(p,e){
  const M=p**BigInt(e),a=W.map(r=>r.map(x=>mod(x,M))),V=I.map(r=>r.slice());
  const val=x=>{if(!x)return e;let k=0;while(x%p===0n){x/=p;k++}return k};
  let zero=-1;
  for(let k=0;k<d;k++){
   let v=e,i0=-1,j0=-1;
   for(let i=k;i<d;i++){for(let j=k;j<d;j++){const t=val(a[i][j]);if(t<v){v=t;i0=i;j0=j}if(v===0)break}if(v===0)break}
   if(i0<0){zero=k;break}
   [a[k],a[i0]]=[a[i0],a[k]];
   for(let i=0;i<d;i++){[a[i][k],a[i][j0]]=[a[i][j0],a[i][k]];[V[i][k],V[i][j0]]=[V[i][j0],V[i][k]]}
   const b=p**BigInt(v),u=inv(a[k][k]/b,M/b);
   for(let j=k;j<d;j++)a[k][j]=mod(a[k][j]*u,M);
   check(a[k][k]===b,"pivot");
   for(let i=k+1;i<d;i++){const q=a[i][k]/b;for(let j=k;j<d;j++)a[i][j]=mod(a[i][j]-q*a[k][j],M)}
   for(let j=k+1;j<d;j++){const q=a[k][j]/b;check(a[k][j]%b===0n,"divisibility");a[k][j]=0n;for(let i=0;i<d;i++)V[i][j]=mod(V[i][j]-q*V[i][k],M)}
  }
  check(zero>=0,"missing exponent witness");
  const v=V.map(r=>r[zero]),wv=W.map(r=>r.reduce((s,x,j)=>s+x*v[j],0n)),cv=C.map(r=>r.reduce((s,x,j)=>s+x*v[j],0n));
  check(v.some(x=>x%p!==0n)&&wv.every(x=>x%M===0n),"invalid primitive loss witness");
  const visible=cv.findIndex(x=>x%p!==0n);check(visible>=0,"witness invisible in catalogue");
  check(wv.some(x=>x%(M*p)!==0n),"witness unexpectedly loses more than exponent");
  return {integralCoordinateDifference:v.map(String),oldBasisDifference:wv.map(String),visibleRecord:lat.sourceRows[visible],visibleDifference:String(cv[visible])}
 }
 const local=[],precisionTable=[];
 for(const cert of lat.localSmith){
  const p=BigInt(cert.prime),e=cert.exponent,ind=peel(A,p,e);
  check(ind.exps.join()===cert.exponents.join(),"independent Smith mismatch at "+p);
  const sharp=witness(p,e);
  const table=[];
  for(const h of [1,2,4,8,16])for(const k of [...new Set([0,1,Math.max(0,e-1),e])].sort((a,b)=>a-b)){
    const ambiguityExponent=cert.exponents.reduce((s,v)=>s+Math.max(0,Math.min(h,v-k)),0);
    table.push({targetDigits:h,extraBasisDigits:k,ambiguityExponent,compatibleFullVectors:String(p**BigInt(ambiguityExponent))})
  }
  precisionTable.push({prime:String(p),maxExtraDigits:e,unitInvariantCount:272-cert.exponents.filter(x=>x>0).length,table});
  local.push({prime:String(p),maximumLoss:e,independentValuationHistogram:ind.scaledOriginalValuationHistogram,nonzeroExponents:ind.exps.filter(x=>x>0),sharpWitness:sharp})
 }
 return {schemaVersion:1,author:"Komorebi P.",scope:"Exact local reconstruction ambiguity on the admissible integer-coordinate lattice for the retained transfer matrix. Fibers describe compatible mathematical coordinate vectors, not how many actual sequence indices attain those vectors. Integer generators remove precision loss. No complexity or shortest-generator claim.",report:{rank:272,independentPrimeChecks:local.length,exactMatrixEntriesChecked:products.reduce((s,x)=>s+x.count,0),corruptedCertificateRejected:true,sharpLossWitnesses:local.length},products,local,precisionTable,formula:"For b=Wz with z integral, knowledge of b modulo p^(h+k) has exactly p^(sum_i max(0,min(h,e_i-k))) possible reductions of z modulo p^h, whenever the data are compatible. The integer reconstruction C and left inverse U give the same count of compatible full catalogue vectors."}
}
module.exports={precision};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas'),read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));const out=precision(read('COMPLETE_FORMAL_TRANSFER_BASIS.json'),read('INTEGRAL_TRANSFER_LATTICE.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
