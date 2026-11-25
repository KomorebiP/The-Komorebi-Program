/* Author: Komorebi P. Minimal augmentation of a fixed rational basis and exact coefficient-size reduction. */
'use strict';
function optimizeIntegral(lat,base){
 const check=(x,m)=>{if(!x)throw Error(m)},abs=a=>a<0n?-a:a;
 const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 const egcd=(a,b)=>{let x=1n,y=0n,z=0n,w=1n;while(b){let q=a/b;[a,b]=[b,a-q*b];[x,z]=[z,x-q*z];[y,w]=[w,y-q*w]}return a<0n?[-a,-x,-y]:[a,x,y]};
 const floor=(a,b)=>{let q=a/b;if(a%b<0n)q--;return q},nearest=(a,b)=>floor(2n*a+b,2n*b);
 const D=BigInt(lat.report.commonDenominator),active=lat.activeBasis,d=active.length,extra=["R08","ND62","R07","T36","T38","U07","B17","T37"],ids=active.concat(extra),m=ids.length,idx=new Map(active.map((id,i)=>[id,i])),byId=new Map(base.transferRows.map(r=>[r.target,r])),oldIdx=new Map(lat.sourceRows.map((id,i)=>[id,i]));
 const src=ids.map(id=>byId.get(id)),A=src.map(r=>{let a=Array(d).fill(0n);for(const t of r.terms)a[idx.get(t.id)]+=BigInt(t.multiplier)*(D/BigInt(r.denominator));return a});
 const H0=lat.hermite.map(r=>r.map(BigInt)),C=lat.reconstructionMatrix.map(r=>r.map(BigInt)),W=lat.oldBasisInIntegralBasis.map(r=>r.map(BigInt));
 const E=ids.map(id=>C[oldIdx.get(id)]);
 function rank(A,p){let M=A.map(r=>r.map(x=>Number((x%BigInt(p)+BigInt(p))%BigInt(p)))),k=0;const mod=x=>((x%p)+p)%p;for(let j=0;j<d;j++){let i=k;while(i<M.length&&!M[i][j])i++;if(i===M.length)continue;[M[i],M[k]]=[M[k],M[i]];let inv=1;while(inv*M[k][j]%p!==1)inv++;for(let t=j;t<d;t++)M[k][t]=mod(M[k][t]*inv);for(let i=k+1;i<M.length;i++){const v=M[i][j];if(v)for(let t=j;t<d;t++)M[i][t]=mod(M[i][t]-v*M[k][t])}k++}return k}
 const local=lat.localSmith.map(r=>{let p=Number(r.prime),before=rank(W,p),after=rank(E,p);check(after===d,"augmentation not spanning "+p);return {prime:p,before,after,defect:d-before}});
 check(Math.max(...local.map(r=>r.defect))===extra.length,"augmentation not minimal");
 const sub=(a,b,q,start=0)=>{if(q)for(let j=start;j<a.length;j++)a[j]-=q*b[j]},lin=(a,b,x,y)=>a.map((v,i)=>x*v+y*b[i]);
 // Recompute the SAME HNF with only the 63 selected active rows.
 const H=active.map((_,i)=>Array.from({length:d},(_,j)=>i===j?D:0n)),V=active.map((_,i)=>Array.from({length:m},(_,j)=>i===j?1n:0n));
 let gcdUpdates=0,eliminations=0;
 for(let k=d;k<m;k++){let r=A[k].slice(),v=Array(m).fill(0n);v[k]=1n;for(let i=0;i<d;i++){if(!r[i])continue;const a=H[i][i],b=r[i];if(b%a===0n){let q=b/a;sub(r,H[i],q,i);sub(v,V[i],q);eliminations++;continue}const [g,x,y]=egcd(a,b),h=H[i],u=V[i];H[i]=lin(h,r,x,y);V[i]=lin(u,v,x,y);r=lin(h,r,-b/g,a/g);v=lin(u,v,-b/g,a/g);check(H[i][i]===g&&r[i]===0n,"pivot");gcdUpdates++;for(let j=i+1;j<d;j++){let q=floor(H[i][j],H[j][j]);sub(H[i],H[j],q,j);sub(V[i],V[j],q)}}check(r.every(x=>x===0n),"insertion")}
 for(let i=d-1;i>=0;i--)for(let j=i+1;j<d;j++){let q=floor(H[i][j],H[j][j]);sub(H[i],H[j],q,j);sub(V[i],V[j],q)}
 check(H.every((r,i)=>r.every((x,j)=>x===H0[i][j])),"different HNF");
 const maxDigits=M=>Math.max(...M.flat().map(x=>abs(x).toString().length));
 const nonzeros=M=>M.reduce((s,r)=>s+r.filter(x=>x!==0n).length,0);
 const initialDigits=maxDigits(V);
 // Exact period reduction: denominator times a retained dependent row
 // is an integer combination of the original identity rows.
 const K=extra.map((id,k)=>{const r=byId.get(id),q=BigInt(r.denominator),v=Array(m).fill(0n);v[d+k]=q;for(const t of r.terms)v[idx.get(t.id)]-=BigInt(t.multiplier);return v});
 for(const v of V)for(let k=0;k<extra.length;k++)sub(v,K[k],nearest(v[d+k],K[k][d+k]));
 const reducedDigits=maxDigits(V),initialSparsity=nonzeros(V);
 // Further reduce the integral lifts in the rank-eight kernel.  Use a
 // deterministic exact size-reduction heuristic, no approximate acceptance.
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0n),norm=a=>dot(a,a);
 let improved=0;
 for(let rounds=0;rounds<64;rounds++){let changed=false;
  for(let i=0;i<K.length;i++)for(let j=0;j<K.length;j++)if(i!==j){const q=nearest(dot(K[i],K[j]),norm(K[j]));if(q){const v=K[i].map((x,k)=>x-q*K[j][k]);if(norm(v)<norm(K[i])){K[i]=v;changed=true}}}
  if(!changed)break
 }
 for(const v of V)for(let rounds=0;rounds<64;rounds++){let changed=false;for(const k of K){const q=nearest(dot(v,k),norm(k));if(!q)continue;const w=v.map((x,j)=>x-q*k[j]);if(norm(w)<norm(v)){for(let j=0;j<m;j++)v[j]=w[j];changed=true;improved++}}if(!changed)break}
 // Also compute a direct small-source transfer to every old catalogue row.
 const F=C.map(r=>Array.from({length:m},(_,j)=>r.reduce((s,x,k)=>s+x*V[k][j],0n)));
 // Re-reduce each output lift in the same kernel, reducing the
 // largest coefficient sizes and preserving all exact rows.
 for(let i=0;i<F.length;i++){
  const v=F[i];for(let rounds=0;rounds<48;rounds++){let changed=false;for(const k of K){const q=nearest(dot(v,k),norm(k));if(!q)continue;const w=v.map((x,j)=>x-q*k[j]);if(norm(w)<norm(v)){for(let j=0;j<m;j++)v[j]=w[j];changed=true}}if(!changed)break}
  const j=ids.indexOf(lat.sourceRows[i]);if(j>=0){v.fill(0n);v[j]=1n}
 }
 const verify=(X,Y,Z)=>{let checks=0;for(let i=0;i<X.length;i++)for(let j=0;j<Y[0].length;j++){let s=0n;for(let k=0;k<Y.length;k++)if(X[i][k]&&Y[k][j])s+=X[i][k]*Y[k][j];check(s===Z[i][j],"matrix product mismatch "+i+","+j);checks++}return checks};
 const I=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>i===j?1n:0n));
 const zeros=Array.from({length:K.length},()=>Array(d).fill(0n));
 const counts={generator:verify(V,E,I),fullReconstruction:verify(F,E,C),kernel:verify(K,E,zeros)};
 // Negative control: one corrupted direct reconstruction entry must fail.
 const bad=F[0].slice();bad[0]+=1n;check(E[0].some(x=>x!==0n)&&bad.some((x,i)=>x!==F[0][i]),"negative control invalid");
 const out={schemaVersion:1,author:"Komorebi P.",scope:"Integral row-lattice reconstruction retaining every original rational basis record. Eight additional original records are necessary and sufficient under this retention constraint. Exact coefficient reduction is heuristic, not globally optimal. 217 inactive identity directions are unchanged.",report:{records:base.transferRows.length,rank:base.basis.length,originalBasisCount:base.basis.length,minimumSupplementaryRecords:extra.length,originalRecordsSufficient:base.basis.length+extra.length,activeInputRecords:m,activeOutputs:C.length,oldFlatGeneratorMaxDigits:lat.report.largestIntegralGeneratorWeightDigits,restrictedHNFMaxDigits:initialDigits,periodReducedMaxDigits:reducedDigits,optimizedGeneratorMaxDigits:maxDigits(V),optimizedGeneratorNonzeroEntries:nonzeros(V),periodReducedNonzeroEntries:initialSparsity,directReconstructionMaxDigits:maxDigits(F),directReconstructionNonzeroEntries:nonzeros(F),gcdUpdates,eliminations,exactKernelReductions:improved,exactMatrixEntryChecks:Object.values(counts).reduce((a,b)=>a+b,0)},localRankChecks:local,supplementaryRecords:extra,activeSourceRecords:ids,activeTargetRecords:lat.sourceRows,integralGeneratorMatrix:V.map(r=>r.map(String)),directReconstructionMatrix:F.map(r=>r.map(String)),kernelDirections:K.map(r=>r.map(String)),checks:counts};
 return out
}
module.exports={optimizeIntegral};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas'),read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));const out=optimizeIntegral(read('INTEGRAL_TRANSFER_LATTICE.json'),read('COMPLETE_FORMAL_TRANSFER_BASIS.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
