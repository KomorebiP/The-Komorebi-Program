/* Author: Komorebi P. Exact integral row lattice and local Smith invariants. */
'use strict';
function lattice(data){
 const check=(x,m)=>{if(!x)throw Error(m)},abs=a=>a<0n?-a:a;
 const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a};
 const egcd=(a,b)=>{let x=1n,y=0n,z=0n,w=1n;while(b){const q=a/b;[a,b]=[b,a-q*b];[x,z]=[z,x-q*z];[y,w]=[w,y-q*w]}return a<0n?[-a,-x,-y]:[a,x,y]};
 const floor=(a,b)=>{let q=a/b;if(a%b<0n)q--;return q};
 const basis=data.basis,rows=data.transferRows,active=basis.filter(id=>rows.some(r=>r.target!==id&&r.terms.some(t=>t.id===id&&BigInt(t.multiplier)!==0n))),aset=new Set(active),d=active.length,index=new Map(active.map((id,i)=>[id,i]));
 const selected=rows.filter(r=>!basis.includes(r.target)||aset.has(r.target)),m=selected.length,selIndex=new Map(selected.map((r,i)=>[r.target,i])),rowSet=new Set(basis);
 for(const r of rows){check(BigInt(r.denominator)>0n,"invalid denominator");check(r.terms.every(t=>rowSet.has(t.id)),"unknown basis ID");if(rowSet.has(r.target))check(r.denominator==="1"&&r.terms.length===1&&r.terms[0].id===r.target&&r.terms[0].multiplier==="1","basis row not identity");let g=BigInt(r.denominator);for(const t of r.terms)g=gcd(g,BigInt(t.multiplier));check(g===1n,"unreduced row")}
 let D=1n;for(const r of rows){const q=BigInt(r.denominator);D=D/gcd(D,q)*q}
 const A=selected.map(r=>{let a=Array(d).fill(0n);for(const t of r.terms){check(index.has(t.id),"unexpected inactive coefficient");a[index.get(t.id)]+=BigInt(t.multiplier)*(D/BigInt(r.denominator))}return a});
 const H=active.map((id,i)=>Array.from({length:d},(_,j)=>i===j?D:0n)),U=active.map(id=>Array.from({length:m},(_,j)=>j===selIndex.get(id)?1n:0n));
 let insertions=0,gcdUpdates=0,divisibleEliminations=0;
 function sub(a,b,q,start=0){if(q!==0n)for(let j=start;j<a.length;j++)a[j]-=q*b[j]}
 function lin(a,b,x,y){return a.map((v,i)=>x*v+y*b[i])}
 for(let k=0;k<m;k++){if(aset.has(selected[k].target))continue;let r=A[k].slice(),v=Array(m).fill(0n);v[k]=1n;insertions++;for(let i=0;i<d;i++){if(r[i]===0n)continue;const a=H[i][i],b=r[i];if(b%a===0n){const q=b/a;sub(r,H[i],q,i);sub(v,U[i],q);divisibleEliminations++;continue}const [g,x,y]=egcd(a,b);check(g>0n&&x*a+y*b===g,"Bezout failure");const h=H[i],u=U[i];H[i]=lin(h,r,x,y);U[i]=lin(u,v,x,y);r=lin(h,r,-b/g,a/g);v=lin(u,v,-b/g,a/g);check(H[i][i]===g&&r[i]===0n,"pivot update failure");gcdUpdates++;for(let j=i+1;j<d;j++){const q=floor(H[i][j],H[j][j]);sub(H[i],H[j],q,j);sub(U[i],U[j],q)}}check(r.every(x=>x===0n),"row insertion incomplete")}
 for(let i=d-1;i>=0;i--)for(let j=i+1;j<d;j++){const q=floor(H[i][j],H[j][j]);sub(H[i],H[j],q,j);sub(U[i],U[j],q)}
 function solve(a){let v=a.slice(),c=[];for(let i=0;i<d;i++){check(v[i]%H[i][i]===0n,"nonintegral reconstruction");let q=v[i]/H[i][i];c.push(q);sub(v,H[i],q,i)}check(v.every(x=>x===0n),"nonzero residual");return c}
 const C=A.map(solve),W=active.map((_,i)=>solve(Array.from({length:d},(_,j)=>i===j?D:0n)));
 let forwardChecks=0,reverseChecks=0;
 for(let i=0;i<d;i++){check(H[i][i]>0n&&H[i].slice(0,i).every(x=>x===0n),"HNF shape");for(let j=i+1;j<d;j++)check(H[i][j]>=0n&&H[i][j]<H[j][j],"HNF reduction");for(let j=0;j<d;j++){let v=0n;for(let k=0;k<m;k++)v+=U[i][k]*A[k][j];check(v===H[i][j],"U A != H");forwardChecks++}}
 for(let i=0;i<m;i++)for(let j=0;j<d;j++){let v=0n;for(let k=0;k<d;k++)v+=C[i][k]*H[k][j];check(v===A[i][j],"C H != A");reverseChecks++}
 let t=D,primes=[];for(let p=2n;p*p<=t;p++){let e=0;while(t%p===0n){t/=p;e++}if(e)primes.push([p,e])}if(t>1n)primes.push([t,1]);
 const mod=(a,m)=>{a%=m;return a<0n?a+m:a};
 function localSmith(p,e){
  const M=p**BigInt(e),a=W.map(r=>r.map(x=>mod(x,M))),exponents=[];
  const val=x=>{if(x===0n)return e;let v=0;while(x%p===0n){x/=p;v++}return v};
  for(let k=0;k<d;k++){
   let best=e,i0=-1,j0=-1;
   for(let i=k;i<d;i++){for(let j=k;j<d;j++){const v=val(a[i][j]);if(v<best){best=v;i0=i;j0=j}if(best===0)break}if(best===0)break}
   if(i0<0){while(exponents.length<d)exponents.push(e);break}
   [a[k],a[i0]]=[a[i0],a[k]];for(let i=0;i<d;i++)[a[i][k],a[i][j0]]=[a[i][j0],a[i][k]];
   const power=p**BigInt(best),unit=a[k][k]/power,mm=M/power,[gg,u0]=egcd(unit,mm),u=mod(u0,M);
   check(gg===1n&&gcd(u,M)===1n,"nonunit Smith pivot");
   for(let j=k;j<d;j++)a[k][j]=mod(a[k][j]*u,M);
   check(a[k][k]===power,"pivot normalization");
   for(let i=k+1;i<d;i++){check(a[i][k]%power===0n,"valuation failure");const q=a[i][k]/power;for(let j=k;j<d;j++)a[i][j]=mod(a[i][j]-q*a[k][j],M)}
   for(let j=k+1;j<d;j++){check(a[k][j]%power===0n,"column valuation failure");a[k][j]=0n}
   exponents.push(best)
  }
  return {prime:String(p),exponent:e,exponents,histogram:Object.fromEntries(Array.from({length:e+1},(_,i)=>[i,exponents.filter(v=>v===i).length]).filter(x=>x[1]))}
 }
 const locals=primes.map(([p,e])=>localSmith(p,e)),invariants=Array.from({length:d},(_,i)=>locals.reduce((a,r)=>a*BigInt(r.prime)**BigInt(r.exponents[i]),1n));
 let det=1n;for(let i=0;i<d;i++)det*=W[i][i];
 check(invariants.reduce((a,b)=>a*b,1n)===det,"Smith determinant mismatch");check(invariants.every((v,i)=>i===0||v%invariants[i-1]===0n),"Smith divisibility");
 // Independent inverse certificate for the old-coordinate inclusion and
 // its exponent bound. W H = D I and U C = I.
 for(let i=0;i<d;i++)for(let j=0;j<d;j++){let v=0n,z=0n;for(let k=0;k<d;k++)v+=W[i][k]*H[k][j];for(let k=0;k<m;k++)z+=U[i][k]*C[k][j];check(v===(i===j?D:0n)&&z===(i===j?1n:0n),"two-sided inclusion certificate")}
 return {schemaVersion:1,author:"Komorebi P.",scope:"Integral row lattice generated by the retained rational transfer matrix; all arithmetic uses exact integers. Nonunit Smith factors describe the inclusion of the original basis lattice, not the Smith form of the rational matrix itself. Inactive identity coordinates are unchanged.",report:{records:rows.length,rank:basis.length,activeBasisColumns:d,untouchedBasisColumns:basis.length-d,scaledRows:m,commonDenominator:String(D),latticeIndex:String(det),nonunitInvariantFactors:invariants.filter(x=>x>1n).length,forwardChecks,reverseChecks,gcdUpdates,divisibleEliminations,insertions,largestIntegralGeneratorWeightDigits:Math.max(...U.flat().map(v=>abs(v).toString().length)),largestReconstructionWeightDigits:Math.max(...C.flat().map(v=>abs(v).toString().length))},activeBasis:active,sourceRows:selected.map(r=>r.target),hermite:H.map(r=>r.map(String)),generatorMatrix:U.map(r=>r.map(String)),reconstructionMatrix:C.map(r=>r.map(String)),oldBasisInIntegralBasis:W.map(r=>r.map(String)),localSmith:locals,invariantFactors:invariants.map(String)}
}
module.exports={lattice};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const input=JSON.parse(fs.readFileSync(path.join(dir,'COMPLETE_FORMAL_TRANSFER_BASIS.json'),'utf8'));const out=lattice(input);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify({report:out.report,invariantFactors:out.invariantFactors,localSmith:out.localSmith},null,2));}
