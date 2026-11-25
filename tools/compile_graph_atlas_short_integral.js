/* Author: Komorebi P. Complete-kernel LLL reduction of integral transfer lifts. */
'use strict';
function reduceCompleteKernel(lat,base,opt){
 const check=(x,m)=>{if(!x)throw Error(m)},abs=x=>x<0n?-x:x;
 const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 function egcd(a,b){let x=1n,y=0n,z=0n,w=1n;while(b){let q=a/b;[a,b]=[b,a-q*b];[x,z]=[z,x-q*z];[y,w]=[w,y-q*w]}return a<0n?[-a,-x,-y]:[a,x,y]}
 const floor=(a,b)=>{check(b>0n,"nonpositive denominator");let q=a/b;if(a%b<0n)q--;return q};
 const nearest=(a,b)=>floor(2n*a+b,2n*b);
 const sub=(a,b,q,start=0)=>{if(q)for(let i=start;i<a.length;i++)a[i]-=q*b[i]};
 const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0n);
 const norm=a=>dot(a,a);
 const lin=(a,b,x,y)=>a.map((v,i)=>x*v+y*b[i]);
 const d=lat.activeBasis.length,m=opt.activeSourceRecords.length,r=m-d;
 const oldC=lat.reconstructionMatrix.map(v=>v.map(BigInt)),oldIndex=new Map(lat.sourceRows.map((id,i)=>[id,i])),V=opt.integralGeneratorMatrix.map(v=>v.map(BigInt)),F=opt.directReconstructionMatrix.map(v=>v.map(BigInt));
 const E=opt.activeSourceRecords.map(id=>oldC[oldIndex.get(id)]);
 const idIndex=new Map(lat.activeBasis.map((id,i)=>[id,i])),catalogue=new Map(base.transferRows.map(row=>[row.target,row]));
 const verify=(A,B,C)=>{let n=0;for(let i=0;i<A.length;i++)for(let j=0;j<B[0].length;j++){let s=0n;for(let k=0;k<B.length;k++)if(A[i][k]&&B[k][j])s+=A[i][k]*B[k][j];check(s===C[i][j],"product mismatch");n++}return n};
 const identity=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>i===j?1n:0n));
 verify(V,E,identity);
 // Projection P=I-EV generates the full kernel, not just the
 // sublattice of independent denominator-clearing relations.
 const P=E.map((row,i)=>Array.from({length:m},(_,j)=>(i===j?1n:0n)-row.reduce((s,x,k)=>s+x*V[k][j],0n)));
 const extras=opt.supplementaryRecords.map(id=>catalogue.get(id));
 const H=extras.map((row,i)=>Array.from({length:r},(_,j)=>i===j?BigInt(row.denominator):0n));
 for(const p of P){let v=p.slice(d);for(let i=0;i<r;i++){if(!v[i])continue;let a=H[i][i],b=v[i];if(b%a===0n){sub(v,H[i],b/a,i);continue}const [g,x,y]=egcd(a,b),h=H[i];H[i]=lin(h,v,x,y);v=lin(h,v,-b/g,a/g);check(H[i][i]===g&&v[i]===0n,"kernel HNF pivot");for(let j=i+1;j<r;j++)sub(H[i],H[j],floor(H[i][j],H[j][j]),j)}check(v.every(x=>x===0n),"kernel insertion")}
 for(let i=r-1;i>=0;i--)for(let j=i+1;j<r;j++)sub(H[i],H[j],floor(H[i][j],H[j][j]),j);
 const det=H.reduce((s,row,i)=>s*row[i],1n);check(det===BigInt(lat.report.latticeIndex),"kernel index mismatch");
 // Recover the unique old-basis coefficients for each projected
 // relation, using exact common-denominator arithmetic.
 const D=BigInt(lat.report.commonDenominator);
 const A=extras.map(row=>{let a=Array(d).fill(0n);for(const t of row.terms)a[idIndex.get(t.id)]+=BigInt(t.multiplier)*(D/BigInt(row.denominator));return a});
 const K=H.map(row=>{let v=Array.from({length:d},(_,i)=>-row.reduce((s,x,k)=>s+x*A[k][i],0n));check(v.every(x=>x%D===0n),"nonintegral kernel lift");return [...v.map(x=>x/D),...row]});
 const zeros=Array.from({length:r},()=>Array(d).fill(0n));
 verify(K,E,zeros);
 // Exact rational arithmetic for Gram-Schmidt and LLL (delta=3/4).
 const rat=(a,b=1n)=>{if(!a)return [0n,1n];if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
 const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const minus=(a,b)=>rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
 const less=(a,b)=>a[0]*b[1]<b[0]*a[1];
 function gram(B){
  const mu=Array.from({length:r},()=>Array.from({length:r},()=>[0n,1n])),length=[];
  for(let i=0;i<r;i++){for(let j=0;j<i;j++){let x=rat(dot(B[i],B[j]));for(let k=0;k<j;k++)x=minus(x,mul(mul(mu[i][k],mu[j][k]),length[k]));mu[i][j]=div(x,length[j])}let v=rat(norm(B[i]));for(let j=0;j<i;j++)v=minus(v,mul(mul(mu[i][j],mu[i][j]),length[j]));check(v[0]>0n,"dependent kernel");length.push(v)}
  return {mu,length}
 }
 const B=K.map(row=>row.slice());let g=gram(B),k=1,swaps=0,sizeReductions=0,iterations=0;
 while(k<r){
  check(++iterations<=10000,"LLL budget");
  for(let j=k-1;j>=0;j--){const [a,b]=g.mu[k][j],q=nearest(a,b);if(q){sub(B[k],B[j],q);sizeReductions++;g=gram(B)}}
  const mu=g.mu[k][k-1],threshold=mul(minus([3n,4n],mul(mu,mu)),g.length[k-1]);
  if(!less(g.length[k],threshold))k++;
  else{[B[k],B[k-1]]=[B[k-1],B[k]];swaps++;g=gram(B);k=Math.max(1,k-1)}
 }
 for(let i=1;i<r;i++){for(let j=0;j<i;j++)check(2n*abs(g.mu[i][j][0])<=g.mu[i][j][1],"size condition");check(!less(g.length[i],mul(minus([3n,4n],mul(g.mu[i][i-1],g.mu[i][i-1])),g.length[i-1])),"Lovasz condition")}
 // Nearest-plane lift reduction, followed by monotone local descent.
 function nearestPlane(v){
  let x=v.slice();
  const dotStar=[];
  for(let j=0;j<r;j++){let s=rat(dot(x,B[j]));for(let i=0;i<j;i++)s=minus(s,mul(g.mu[j][i],dotStar[i]));dotStar.push(s)}
  for(let j=r-1;j>=0;j--){const a=div(dotStar[j],g.length[j]),q=nearest(a[0],a[1]);if(q){sub(x,B[j],q);for(let i=0;i<=j;i++)dotStar[i]=minus(dotStar[i],mul(rat(q),i===j?g.length[i]:mul(g.mu[j][i],g.length[i])))}}
  if(norm(x)>norm(v))x=v.slice();
  for(let pass=0;pass<32;pass++){let changed=false;for(const row of B){const q=nearest(dot(x,row),norm(row));if(q){const y=x.map((a,j)=>a-q*row[j]);if(norm(y)<norm(x)){x=y;changed=true}}}if(!changed)break}
  return x
 }
 const newV=V.map(nearestPlane),newF=F.map((row,i)=>{const j=opt.activeSourceRecords.indexOf(lat.sourceRows[i]);return j>=0?Array.from({length:m},(_,k)=>k===j?1n:0n):nearestPlane(row)});
 const n1=verify(newV,E,identity),n2=verify(newF,E,oldC),n3=verify(B,E,zeros),n4=verify(P,E,Array.from({length:m},()=>Array(d).fill(0n)));
 // Check that the reduced kernel basis has the same lattice determinant.
 function determinant(M){const a=M.map(r=>r.slice());let sign=1n,prev=1n;for(let k=0;k<a.length-1;k++){let i=k;while(i<a.length&&!a[i][k])i++;if(i===a.length)return 0n;if(i!==k){[a[i],a[k]]=[a[k],a[i]];sign=-sign}const p=a[k][k];for(let i=k+1;i<a.length;i++)for(let j=k+1;j<a.length;j++){let t=a[i][j]*p-a[i][k]*a[k][j];check(t%prev===0n,"Bareiss");a[i][j]=t/prev}for(let i=k+1;i<a.length;i++)a[i][k]=0n;prev=p}return sign*a.at(-1).at(-1)}
 check(abs(determinant(B.map(row=>row.slice(d))))===det,"reduced kernel determinant mismatch");
 const digits=A=>Math.max(...A.flat().map(x=>abs(x).toString().length)),nnz=A=>A.reduce((s,r)=>s+r.filter(x=>x!==0n).length,0),maxWeight=A=>A.flat().reduce((s,x)=>abs(x)>s?abs(x):s,0n).toString();
 const bad=newF[0].slice();bad[0]+=1n;check(E[0].some((x,j)=>x!==0n&&bad.reduce((s,v,k)=>s+v*E[k][j],0n)!==oldC[0][j]),"corruption not detected");
 return {schemaVersion:1,author:"Komorebi P.",scope:"Exact complete-kernel reduction of the minimum eight-record augmentation. The kernel is saturated, and the reduced basis satisfies exact LLL conditions. Shorter lifts are heuristic, not a proof of shortest possible formulas. The 217 inactive identity directions are unchanged.",report:{records:base.transferRows.length,rank:base.basis.length,sourceRecords:base.basis.length+r,kernelRank:r,kernelIndex:String(det),oldGeneratorMaxDigits:digits(V),newGeneratorMaxDigits:digits(newV),oldGeneratorMaxWeight:maxWeight(V),newGeneratorMaxWeight:maxWeight(newV),oldDirectMaxDigits:digits(F),newDirectMaxDigits:digits(newF),oldDirectMaxWeight:maxWeight(F),newDirectMaxWeight:maxWeight(newF),generatorNonzeroEntries:nnz(newV),directNonzeroEntries:nnz(newF),lllSwaps:swaps,lllSizeReductions:sizeReductions,exactMatrixEntryChecks:n1+n2+n3+n4,corruptedRowRejected:true},activeSourceRecords:opt.activeSourceRecords,activeTargetRecords:opt.activeTargetRecords,integralGeneratorMatrix:newV.map(r=>r.map(String)),directReconstructionMatrix:newF.map(r=>r.map(String)),completeKernelBasis:B.map(r=>r.map(String)),kernelProjectionHNF:H.map(r=>r.map(String))}
}
module.exports={reduceCompleteKernel};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas'),read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));const out=reduceCompleteKernel(read('INTEGRAL_TRANSFER_LATTICE.json'),read('COMPLETE_FORMAL_TRANSFER_BASIS.json'),read('OPTIMIZED_INTEGRAL_TRANSFER.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
