/* Author: Komorebi P. Cyclotomic-annihilator slice certificates for antidiagonal arrays. */
'use strict';
function certifyAntidiagonal(raw,engine,fixed,compressSparse,basis){
 const check=(a,m)=>{if(!a)throw Error(m)};
 const models=engine.compile(raw),ids=[...raw.matchAll(/^### (A\d{6})(?: \*)?\s*\n([\s\S]*?)(?=^### A\d{6}|^## |$(?![\s\S]))/gm)].filter(m=>m[2].includes("antidiagonal")&&!["A202100","A202202"].includes(m[1])).map(m=>m[1]);
 check(ids.length===18,"antidiagonal inventory");
 const strips=new Map(fixed.stripModels.map(m=>[m.diagonal+","+m.width,m]));
 const choose=(n,k)=>{let v=1;for(let i=1;i<=k;i++)v=v*(n-k+i)/i;return v};
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 let referenceChecks=0,referenceSkipped=0;
 function scan(p){
  check(Number.isSafeInteger(p*p),"unsafe field");for(let j=2;j*j<=p;j++)check(p%j!==0,"nonprime");
  const P=BigInt(p),mod=x=>((x%p)+p)%p,cv=x=>Number((BigInt(x)%P+P)%P);
  function inv(a){let u=1,v=0,b=p;while(b){const q=Math.floor(a/b);[a,b]=[b,a%b];[u,v]=[v,u-q*v]}check(a===1,"nonunit");return mod(u)}
  function seq(P,Q,N){P=P.map(cv);Q=Q.map(cv);check(Q[0]===1,"normalization");const a=[];for(let n=0;n<N;n++){let t=P[n]||0;for(let j=1;j<Q.length&&j<=n;j++)t=mod(t-Q[j]*a[n-j]);a.push(t)}return a}
  function bm(a){let C=[1],B=[1],L=0,b=1,k=1;for(let n=0;n<a.length;n++){let d=a[n];for(let j=1;j<=L;j++)d=mod(d+(C[j]||0)*a[n-j]);if(!d){k++;continue}const T=C.slice(),s=mod(d*inv(b));while(C.length<B.length+k)C.push(0);for(let j=0;j<B.length;j++)C[j+k]=mod(C[j+k]-s*B[j]);if(2*L<=n){L=n+1-L;B=T;b=d;k=1}else k++}while(C.length<L+1)C.push(0);return C.slice(0,L+1)}
  function polyMulMod(a,b,Q){const r=Q.length-1,c=Array(2*r-1).fill(0);for(let i=0;i<a.length;i++)if(a[i])for(let j=0;j<b.length;j++)if(b[j])c[i+j]=mod(c[i+j]+a[i]*b[j]);for(let i=c.length-1;i>=r;i--)if(c[i]){const t=c[i];for(let j=1;j<=r;j++)c[i-j]=mod(c[i-j]-t*Q[j])}return c.slice(0,r)}
  function power(a,k,Q){const r=Q.length-1;let b=Array(r).fill(0);b[0]=1;while(k){if(k&1n)b=polyMulMod(b,a,Q);k>>=1n;if(k)a=polyMulMod(a,a,Q)}return b}
  function shift(Q){let r=Q.length-1,a=Array(r).fill(0);if(r===1)a[0]=mod(-Q[1]);else a[1]=1;return a}
  function spec(id,i){
   const a=models[id],h=1+Math.floor(i/2),k=1+Math.ceil(i/2);
   if(a.kind==="reduced"){
    const d=(id==="A202406"||id==="A202601")?0:1;
    if(id==="A202435"||id==="A202601"){
     const q=strips.get(d+","+(i+1)),D=2*(q.denominator.length-1);
     return {D,terms(N){const I=seq(q.numerator,q.denominator,N+4),F=seq([0,1],[1,-1,-1],N+Math.max(i+4,4));return Array.from({length:N},(_,j)=>mod(mod(2*F[i+3]*F[j+3])*I[j+1]))}}
    }
    const a0=strips.get(d+","+h),b0=strips.get(d+","+k),r=a0.denominator.length-1,s=b0.denominator.length-1,D=2*(h===k?choose(r+3,4):choose(r+1,2)*choose(s+1,2));
    return {D,terms(N){const A=seq(a0.numerator,a0.denominator,N+4),B=seq(b0.numerator,b0.denominator,N+4);return Array.from({length:N},(_,j)=>{const u=1+Math.floor(j/2),v=1+Math.ceil(j/2);return mod(mod(A[u]*A[v])*mod(B[u]*B[v]))})}}
   }
   const L=a.kind==="B"?2:a.kind==="A"?a.patterns[0].length:a.parameters[0],w=i+L-1,q=compressSparse({...a,w:["const",String(w)]});
   check(!q.status,"slice quotient deferred "+id);
   return {D:q.states,terms(N){let v=Array(q.states).fill(1),out=[];for(let j=0;j<N;j++){out.push(mod(v.reduce((x,y,k)=>x+q.weights[k]*y,0)));v=q.quotient.map(row=>mod(row.reduce((x,[k,c])=>x+c*v[k],0)))}return out}}
  }
  const rows=[],descriptors=[],slices=[];
  let residualChecks=0;
  for(let i=1;i<=3;i++){
   const specs=ids.map(id=>spec(id,i)),D=Math.max(...specs.map(s=>s.D));
   let L=1n;for(let j=1;j<=2*D;j++)L=L/gcd(L,BigInt(j))*BigInt(j);
   const vectors=[];
   for(let k=0;k<ids.length;k++){
    const s=specs[k],a=s.terms(2*s.D+32),Q=bm(a.slice(0,2*s.D)),r=Q.length-1;
    check(r<=s.D&&r>0,"BM bound "+ids[k]);
    for(let n=r;n<a.length;n++){let t=a[n];for(let j=1;j<=r;j++)t=mod(t+Q[j]*a[n-j]);check(t===0,"BM residual "+ids[k]);residualChecks++}
    for(let j=1;j<=3;j++){const ell=i+j-1,n=ell*(ell-1)/2+i;try{const v=engine.value(models[ids[k]],n);check(a[j]===cv(v),"independent slice "+ids[k]);referenceChecks++}catch(e){if(!String(e.message).includes("work limit"))throw e;referenceSkipped++}}
    let z=power(shift(Q),L,Q);z[0]=mod(z[0]-1);
    const filter=polyMulMod(power(z,BigInt(D),Q),power(shift(Q),BigInt(D),Q),Q);
    const v=Array.from({length:32},(_,j)=>mod(filter.reduce((t,c,k)=>mod(t+c*a[k+j]),0)));
    vectors.push(v);descriptors.push({id:ids[k],slice:i,dimension:s.D,modularOrder:r,recurrence:Q,filter})
   }
   for(let j=0;j<32;j++)rows.push(vectors.map(a=>a[j]));
   slices.push({slice:i,D,shiftPeriod:L.toString()})
  }
  function rank(input){const mat=input.map(r=>r.slice()),permutation=mat.map((_,i)=>i),pivots=[];let rank=0;
   for(let j=0;j<mat[0].length;j++){let k=rank;while(k<mat.length&&!mat[k][j])k++;if(k===mat.length)continue;[mat[k],mat[rank]]=[mat[rank],mat[k]];[permutation[k],permutation[rank]]=[permutation[rank],permutation[k]];const v=inv(mat[rank][j]);for(let k=j;k<mat[0].length;k++)mat[rank][k]=mod(mat[rank][k]*v);for(let k=rank+1;k<mat.length;k++){const c=mat[k][j];if(c)for(let l=j;l<mat[0].length;l++)mat[k][l]=mod(mat[k][l]-c*mat[rank][l])}pivots.push(j);rank++}return {rank,pivotColumns:pivots,minorRows:permutation.slice(0,rank)}}
  const witness=rank(rows);check(witness.rank===18,"incomplete antidiagonal independence");check(rank(rows.map(r=>[...r,r[0]])).rank===18,"duplicate negative control");
  return {prime:p,...witness,residualChecks,slices,descriptors,filteredCoefficientMatrix:rows}
 }
 const witnesses=[scan(1000003),scan(1000033)];
 const added=ids.filter(id=>!basis.basis.includes(id)),rows=[...basis.transferRows,...added.map(id=>({target:id,denominator:"1",terms:[{id,multiplier:"1"}]}))];
 check(added.length===16&&rows.length===533,"formal inventory");
 const unresolved=basis.unresolved.filter(id=>!added.includes(id)),rank=basis.report.formalRank+added.length;
 return {schemaVersion:1,author:"Komorebi P.",scope:"Exact constant rational span of 533 retained formal generating functions. All 20 antidiagonal directions are independent modulo rational generating functions, using a cyclotomic annihilator on fixed-height slices for 18 of them and the balanced-binomial growth argument for two. Four square-array directions remain unresolved. The proof uses exact integer realization dimensions, modular rank witnesses, and the predecessor growth-tier argument.",report:{previousModels:basis.report.formalRepresentedModels,previousRank:basis.report.formalRank,antidiagonalModels:20,filteredIndependentDirections:18,addedModels:added.length,totalModels:rows.length,rank,dependenceDimension:rows.length-rank,fullAtlasRankLowerBound:rank,fullAtlasRankUpperBound:rank+unresolved.length,unresolved:unresolved.length,referenceChecks,referenceSkipped,modularResidualChecks:witnesses.reduce((s,w)=>s+w.residualChecks,0),duplicateNegativeControlRejected:true},basis:[...basis.basis,...added],transferRows:rows,addedBasis:added,unresolved,filteredModels:ids,witnesses}
}
module.exports={certifyAntidiagonal};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8'),json=f=>JSON.parse(read(f));const out=certifyAntidiagonal(read('OEIS_168_Array_Formulas.md'),require('../website/assets/graph-array-evaluator.js'),json('FIXED_ARRAY_WALK_RATIONAL.json'),require('./graph_array_sparse_quotient.js').compressSparse,json('FORMAL_TRANSFER_BASIS.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
