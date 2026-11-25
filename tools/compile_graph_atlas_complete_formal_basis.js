/* Author: Komorebi P. Exact uniform seam probability certificate and complete rank-272 formal transfer matrix. */
'use strict';
function certifyFinalBoundary(basis){
  const check=(ok,m)=>{if(!ok)throw Error(m)};
  const S=1000000000n,ceilDiv=(a,b)=>(a+b-1n)/b;
  // Odds R_G(v) = Z(G-N[v])/Z(G-v) in the unit-activity hard-core model.
  // Delete v, partition its remaining neighborhood into cliques of size
  // one or two, and telescope the partition-function ratios.
  function makeCalculator(adj){
    const removed=new Uint8Array(adj.length);
    let calls=0;
    function odds(v,d){
      check(!removed[v],"recursion entered a removed vertex");calls++;
      if(!d)return [0n,S];
      removed[v]=1;
      let lo=S,hi=S;const used=[];
      for(const u of adj[v])if(!removed[u]){
        const partner=adj[v].find(t=>t!==u&&!removed[t]&&adj[u].includes(t));
        let a;
        if(partner!==undefined){
          removed[partner]=1;a=odds(u,d-1);removed[partner]=0;
          removed[u]=1;const b=odds(partner,d-1);
          removed[partner]=1;used.push(partner);
          a=[a[0]+b[0],a[1]+b[1]];
        }else{a=odds(u,d-1);removed[u]=1}
        lo=lo*S/(S+a[1]);hi=ceilDiv(hi*S,S+a[0]);used.push(u);
      }
      for(const u of used)removed[u]=0;removed[v]=0;
      check(lo>=0n&&lo<=hi&&hi<=S,"invalid odds interval");
      return [lo,hi];
    }
    function occ(v,d){const [l,h]=odds(v,d);return [l*S/(S+l),ceilDiv(h*S,S+h)]}
    function joint(u,v,d){
      check(u!==v&&!adj[u].includes(v),"joint endpoints must be distinct and nonadjacent");
      const a=occ(u,d);removed[u]=1;for(const t of adj[u])removed[t]=1;
      const b=occ(v,d);removed[u]=0;for(const t of adj[u])removed[t]=0;
      return [a[0]*b[0]/S,ceilDiv(a[1]*b[1],S)];
    }
    return {occ,joint,calls:()=>calls}
  }
  // Infinite local seam template, restricted to a patch that contains
  // every nontruncated recursion neighborhood at the required depth.
  // Coordinates are (column,row). Add seam edges in increasing row order,
  // horizontal first, NW-SE diagonal second.
  function seamGraph(D,narrow,afterHorizontal){
    const xmin=narrow?0:-D-3,xmax=D+4,ymin=-D-4,ymax=D+4,W=xmax-xmin+1;
    const id=(x,y)=>(y-ymin)*W+x-xmin,adj=Array.from({length:W*(ymax-ymin+1)},()=>[]);
    for(let y=ymin;y<=ymax;y++)for(let x=xmin;x<=xmax;x++)for(const [dx,dy] of [[1,0],[0,1],[1,1]]){
      const a=x+dx,b=y+dy;
      if(a>xmax||b>ymax)continue;
      if(x===0&&a===1&&!(y<0||(afterHorizontal&&y===0&&b===0)))continue;
      const u=id(x,y),v=id(a,b);adj[u].push(v);adj[v].push(u)
    }
    for(const row of adj)row.sort((a,b)=>a-b);
    return {adj,u:id(0,0),v:id(1,afterHorizontal?1:0)};
  }
  const D=8,records=[];
  for(const narrow of [true,false]){
    let lo=S,hi=S;const edges=[];
    for(const afterHorizontal of [false,true]){
      const {adj,u,v}=seamGraph(D,narrow,afterHorizontal),c=makeCalculator(adj),[l,h]=c.joint(u,v,D);
      lo=lo*(S-h)/S;hi=ceilDiv(hi*(S-l),S);
      edges.push({edge:afterHorizontal?"diagonal":"horizontal",jointLower:String(l),jointUpper:String(h),recursiveCalls:c.calls()})
    }
    records.push({type:narrow?"one-column":"two-wide",lower:String(lo),upper:String(hi),edges})
  }
  const [narrow,wide]=records;
  check(BigInt(narrow.upper)===872727237n&&BigInt(wide.lower)===883255784n,"independent C++ interval comparison");
  check(BigInt(wide.lower)>BigInt(narrow.upper),"seam separation failed");
  const U=873n,L=883n;
  check(BigInt(narrow.upper)*1000n<=U*S&&BigInt(wide.lower)*1000n>=L*S&&U<L,"rounded strict inequality");
  // Independent exhaustive controls on all simple graphs through five
  // vertices. Compare each interval against exact independent-set counts
  // rather than a second implementation of the recursive formula.
  let graphs=0,occupancyChecks=0,jointChecks=0;
  for(let n=1;n<=5;n++){
    const pairs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)pairs.push([u,v]);
    for(let mask=0;mask<2**pairs.length;mask++){
      const adj=Array.from({length:n},()=>[]);
      for(let j=0;j<pairs.length;j++)if(mask&(1<<j)){const [u,v]=pairs[j];adj[u].push(v);adj[v].push(u)}
      for(const row of adj)row.sort((a,b)=>a-b);
      let z=0n,ones=Array(n).fill(0n),both=Array(pairs.length).fill(0n);
      for(let b=0;b<2**n;b++){
        if(pairs.some(([u,v],j)=>(mask&(1<<j))&&(b&(1<<u))&&(b&(1<<v))))continue;
        z++;for(let u=0;u<n;u++)if(b&(1<<u))ones[u]++;
        for(let j=0;j<pairs.length;j++){const [u,v]=pairs[j];if((b&(1<<u))&&(b&(1<<v)))both[j]++}
      }
      const c=makeCalculator(adj);graphs++;
      for(let d=0;d<=n;d++){
        for(let u=0;u<n;u++){const [a,b]=c.occ(u,d);check(a*z<=ones[u]*S&&ones[u]*S<=b*z,"occupancy control");occupancyChecks++}
        for(let j=0;j<pairs.length;j++)if(!(mask&(1<<j))){
          const [u,v]=pairs[j],[a,b]=c.joint(u,v,d);check(a*z<=both[j]*S&&both[j]*S<=b*z,"joint control");jointChecks++
        }
      }
    }
  }
  const id="A202427";
  check(basis.report.totalModels===536&&basis.report.rank===271&&basis.unresolved.join()===id,"predecessor inventory");
  check(basis.transferRows.length===536&&basis.basis.length===271&&!basis.basis.includes(id),"predecessor dimensions");
  const rows=[...basis.transferRows,{target:id,denominator:"1",terms:[{id,multiplier:"1"}]}],ids=[...basis.basis,id];
  check(new Set(rows.map(r=>r.target)).size===537&&new Set(ids).size===272,"complete inventory");
  const idSet=new Set(ids);
  for(const r of rows){check(BigInt(r.denominator)>0n&&r.terms.every(t=>idSet.has(t.id)),"invalid transfer row "+r.target)}
  return {schemaVersion:1,author:"Komorebi P.",scope:"Complete constant rational linear span of the 537 retained mathematical generating-function definitions, using the predecessor index and zero-padding conventions. Rank 272 follows from the written uniform seam comparison and predecessor exact spanning/independence certificates. No new OEIS bindings, claims of literature priority, or Lean verification. The last 18 fixed-state models retain compact rational realizations without certified minimal scalar denominator expansions.",report:{previousModels:536,previousRank:271,totalModels:537,rank:272,dependenceDimension:265,rationalModels:506,rationalRank:241,nonrationalModels:31,nonrationalQuotientRank:31,unresolved:0,exhaustiveControlGraphs:graphs,occupancyChecks,jointChecks},basis:ids,transferRows:rows,addedBasis:[id],unresolved:[],boundaryCertificate:{scale:String(S),depth:D,records,roundedNarrowUpper:{numerator:String(U),denominator:"1000"},roundedWideLower:{numerator:String(L),denominator:"1000"},ratioLowerBase:{numerator:String(L),denominator:String(U)},interiorMargin:D+5,proof:"For all sufficiently large m, A202427/A202484 >= c (883/873)^(2m), with c>0 independent of m. See COMPLETE_RANK_272_PROOF.md."}};
}
module.exports={certifyFinalBoundary};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const prior=JSON.parse(fs.readFileSync(path.join(dir,'SQUARE_SEPARATED_TRANSFER_BASIS.json'),'utf8'));const out=certifyFinalBoundary(prior);if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify({report:out.report,boundaryCertificate:out.boundaryCertificate},null,2));}
