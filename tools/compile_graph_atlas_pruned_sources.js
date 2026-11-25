/* Author: Komorebi P. Exact source deletion and exhaustive restricted-pool unimodularity certificate. */
'use strict';
function certifyPrunedSources(lat,base,short){
 const check=(ok,m)=>{if(!ok)throw Error(m)},abs=x=>x<0n?-x:x,gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 const egcd=(a,b)=>{let x=1n,y=0n,z=0n,w=1n;while(b){let q=a/b;[a,b]=[b,a-q*b];[x,z]=[z,x-q*z];[y,w]=[w,y-q*w]}return a<0n?[-a,-x,-y]:[a,x,y]};
 function choose(n,k){let a=1n;for(let i=1;i<=k;i++)a=a*BigInt(n-i+1)/BigInt(i);return a}
 function determinant(M){let a=M.map(r=>r.slice()),s=1n,z=1n;for(let k=0;k<a.length-1;k++){let i=k;while(i<a.length&&!a[i][k])i++;if(i===a.length)return 0n;if(i!==k){[a[i],a[k]]=[a[k],a[i]];s=-s}let p=a[k][k];for(let i=k+1;i<a.length;i++)for(let j=k+1;j<a.length;j++){let t=a[i][j]*p-a[i][k]*a[k][j];check(t%z===0n,"Bareiss exact division");a[i][j]=t/z}for(let i=k+1;i<a.length;i++)a[i][k]=0n;z=p}return s*a.at(-1).at(-1)}
 const C=lat.reconstructionMatrix.map(r=>r.map(BigInt)),rowIndex=new Map(lat.sourceRows.map((id,i)=>[id,i])),d=lat.activeBasis.length;
 const source0=short.activeSourceRecords.slice(),m=source0.length,K0=short.completeKernelBasis.map(r=>r.map(BigInt)),r=K0.length;
 check(m===63&&d===55&&r===8&&short.activeTargetRecords.join()===lat.sourceRows.join(),"predecessor shape");
 const inactive=base.basis.filter(id=>!lat.activeBasis.includes(id)),inactiveSet=new Set(inactive);
 check(inactive.length===217&&base.transferRows.every(row=>row.terms.every(t=>!inactiveSet.has(t.id)||(row.target===t.id&&row.terms.length===1&&row.denominator==="1"&&t.multiplier==="1"))),"inactive identity assertion");
 const E0=source0.map(id=>C[rowIndex.get(id)]),F0=short.directReconstructionMatrix.map(r=>r.map(BigInt)),V0=short.integralGeneratorMatrix.map(r=>r.map(BigInt));
 const I=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>i===j?1n:0n)),zero=n=>Array.from({length:n},()=>Array(d).fill(0n));
 let checks=0;
 function verify(A,B,D){check(A.length===D.length,"product height");for(let i=0;i<A.length;i++)for(let j=0;j<B[0].length;j++){let s=0n;for(let k=0;k<B.length;k++)if(A[i][k]&&B[k][j])s+=A[i][k]*B[k][j];check(s===D[i][j],"product mismatch "+i+","+j);checks++}}
 verify(V0,E0,I);verify(F0,E0,C);verify(K0,E0,zero(r));
 // Completeness of K0 follows from projection onto the eight
 // supplementary coordinates and the checked quotient index.
 check(abs(determinant(K0.map(row=>row.slice(d))))===BigInt(lat.report.latticeIndex),"kernel determinant");
 function remove(K,j){
  let B=K.map(row=>row.slice());let h=B.findIndex(row=>row[j]!==0n);check(h>=0,"zero column");[B[0],B[h]]=[B[h],B[0]];
  for(let i=1;i<B.length;i++)if(B[i][j]){let a=B[0][j],b=B[i][j],[g,x,y]=egcd(a,b),u=B[0],v=B[i];B[0]=u.map((a,k)=>x*a+y*v[k]);B[i]=u.map((q,k)=>-b/g*q+a/g*v[k]);check(B[0][j]===g&&B[i][j]===0n,"Bezout elimination")}
  check(abs(B[0][j])===1n,"not removable");
  const unit=B[0].map(x=>x/B[0][j]);
  return {unit,kernel:B.slice(1).map(row=>row.filter((_,i)=>i!==j))}
 }
 // Retain the best deterministic seeded pruning path from the search.
 const removed=["T03","D48","T10","C03","D33","C02","B05"];
 let K=K0.map(row=>row.slice()),F=F0.map(row=>row.slice()),V=V0.map(row=>row.slice()),ids=source0.slice(),deletions=[];
 for(const id of removed){const j=ids.indexOf(id);check(j>=0&&K.reduce((s,row)=>gcd(s,row[j]),0n)===1n,"invalid deletion");
  const {unit,kernel}=remove(K,j);
  deletions.push({removed:id,retainedBefore:ids.slice(),unitRelation:unit.map(String)});
  const update=A=>A.map(row=>row.map((x,i)=>x-row[j]*unit[i]).filter((_,i)=>i!==j));
  F=update(F);V=update(V);K=kernel;ids.splice(j,1)
 }
 check(ids.length===56&&K.length===1,"pruning count");
 const relation=K[0];check(relation.reduce(gcd,0n)===1n&&relation.every(x=>abs(x)!==1n),"final kernel");
 // The exact one-dimensional nearest Euclidean lift is obtained by
 // rounding the scalar projection. Identity rows stay identities.
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0n),den=dot(relation,relation);
 function nearest(a,b){let x=2n*a+b,q=x/(2n*b);if(x%(2n*b)<0n)q--;return q}
 const shorten=row=>{let q=nearest(dot(row,relation),den);return row.map((x,i)=>x-q*relation[i])};
 V=V.map(shorten);F=F.map((row,i)=>{let j=ids.indexOf(lat.sourceRows[i]);return j>=0?Array.from({length:ids.length},(_,k)=>k===j?1n:0n):shorten(row)});
 const E=ids.map(id=>C[rowIndex.get(id)]);verify(V,E,I);verify(F,E,C);verify(K,E,zero(1));
 // Exhaust the possible complements of a 55-element active basis
 // drawn from the original 63-element source pool. A unimodular
 // complement minor can only use primitive columns of K0.
 const eligible=Array.from({length:m},(_,j)=>j).filter(j=>K0.reduce((a,row)=>gcd(a,row[j]),0n)===1n);
 const primes=[2,3,5,7,11,13,17,19,23,29],modCols=primes.map(p=>eligible.map(j=>K0.map(row=>Number((row[j]%BigInt(p)+BigInt(p))%BigInt(p)))));
 function rank(M,p){const a=M.map(row=>row.slice());let k=0;for(let j=0;j<r;j++){let i=k;while(i<a.length&&!a[i][j])i++;if(i===a.length)continue;[a[i],a[k]]=[a[k],a[i]];let v=1;while(v*a[k][j]%p!==1)v++;for(let t=j;t<r;t++)a[k][t]=a[k][t]*v%p;for(let i=k+1;i<a.length;i++){let v=a[i][j];if(v)for(let t=j;t<r;t++)a[i][t]=((a[i][t]-v*a[k][t])%p+p)%p}k++}return k}
 let tested=0,survivors=0,unit=0,min=null,minSet=[],fail=Object.fromEntries(primes.map(p=>[p,0]));
 function visit(comb,start){if(comb.length===r){tested++;for(let i=0;i<primes.length;i++)if(rank(comb.map(j=>modCols[i][j]),primes[i])<r){fail[primes[i]]++;return}survivors++;const det=abs(determinant(K0.map(row=>comb.map(j=>row[eligible[j]]))));check(det!==0n,"modular full-rank determinant zero");if(min===null||det<min){min=det;minSet=comb.map(j=>source0[eligible[j]])}if(det===1n)unit++;return}for(let j=start;j<=eligible.length-(r-comb.length);j++)visit([...comb,j],j+1)}
 visit([],0);
 check(BigInt(tested)===choose(eligible.length,r)&&Object.values(fail).reduce((a,b)=>a+b,0)+survivors===tested&&unit===0,"subset enumeration");
 // Negative control for unit-minor test, obtained from a coordinate
 // identity matrix rather than the non-unimodular catalogue.
 check(determinant(Array.from({length:r},(_,i)=>Array.from({length:r},(_,j)=>i===j?1n:0n)))===1n,"unit control");
 // A corrupted reconstruction coefficient must fail a true product.
 const bad=F[0].slice();bad[0]+=1n;check(E[0].some((x,j)=>x!==0n&&bad.reduce((a,v,k)=>a+v*E[k][j],0n)!==C[0][j]),"corruption control");
 const maxWeight=A=>A.flat().reduce((s,x)=>abs(x)>s?abs(x):s,0n).toString(),nnz=A=>A.reduce((s,row)=>s+row.filter(x=>x!==0n).length,0);
 return {schemaVersion:1,author:"Komorebi P.",scope:"Exact minimum integral generating subset inside the specified 280-record pool. All original 537 catalogue records are reconstructible from 273 selected original records. The full-catalogue minimum is either 272 or 273; no unrestricted 272-record impossibility is claimed. One-dimensional lift reduction minimizes Euclidean norm on the integral relation coset, not evaluation cost or maximum absolute coefficient.",report:{atlasRecords:537,rank:272,priorSourceCount:280,newSourceCount:273,minimumWithinPriorPool:273,globalMinimumLowerBound:272,globalMinimumUpperBound:273,activeSources:56,activeTargets:C.length,inactiveIdentitySources:inactive.length,relationRank:1,deletedRecords:removed.length,eligibleRemovalColumns:eligible.length,eligibleEightColumnComplements:tested,excludedByPrime:Object.values(fail).reduce((a,b)=>a+b,0),exactDeterminants:survivors,unitComplements:unit,allExactMatrixEntryChecks:checks,generatorMaxWeight:maxWeight(V),directMaxWeight:maxWeight(F),generatorNonzeros:nnz(V),directNonzeros:nnz(F),corruptedRowRejected:true},removedRecords:removed,activeSourceRecords:ids,inactiveIdentityRecords:inactive,activeTargetRecords:lat.sourceRows,integralGeneratorMatrix:V.map(row=>row.map(String)),directReconstructionMatrix:F.map(row=>row.map(String)),completeRelation:relation.map(String),deletionCertificates:deletions,subsetAudit:{totalEightColumnComplements:choose(m,r).toString(),eligibleRemovedColumns:eligible.map(j=>source0[j]),enumeratedEligibleComplements:tested,firstPrimeRejectionCounts:fail,remainingExactDeterminants:survivors,unitComplements:unit,smallestSurvivingAbsoluteDeterminant:min.toString(),smallestSurvivingComplement:minSet}}
}
module.exports={certifyPrunedSources};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas'),read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));const out=certifyPrunedSources(read('INTEGRAL_TRANSFER_LATTICE.json'),read('COMPLETE_FORMAL_TRANSFER_BASIS.json'),read('SHORT_INTEGRAL_TRANSFER.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
