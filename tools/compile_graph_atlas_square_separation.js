/* Author: Komorebi P. Exact strip entropy and square-array separation certificates. */
'use strict';
function certifySquareSeparation(raw,engine,basis){
  const check=(a,m)=>{if(!a)throw Error(m)};
  const models=engine.compile(raw);
  // Independently build the exact transfer matrices for two hard-core
  // constraints. Use integer power iteration only to propose positive
  // comparison vectors; certify the final row inequalities exactly.
  function strip(w,kind,steps,num,den,direction){
    const rows=[];for(let a=0;a<2**w;a++)if(!(a&(a<<1))&&(kind!=="distance2"||!(a&(a<<2))))rows.push(a);
    const R=rows.length,edges=[];
    if(kind==="triangular"){
      for(const a of rows){const e=[];for(let j=0;j<R;j++)if(!(a&rows[j])&&!((a<<1)&rows[j]))e.push(j);edges.push(Int32Array.from(e))}
    }else{
      const pairs=[],index=new Int32Array(R*R).fill(-1);
      for(let i=0;i<R;i++)for(let j=0;j<R;j++)if(!(rows[i]&rows[j])){index[i*R+j]=pairs.length;pairs.push([i,j])}
      for(const [i,j] of pairs){const e=[];for(let k=0;k<R;k++)if(!((rows[i]|rows[j])&rows[k])){const t=index[j*R+k];check(t>=0,"invalid pair");e.push(t)}edges.push(Int32Array.from(e))}
    }
    const S=edges.length,scale=1000000;let v=new Float64Array(S).fill(scale),z;
    for(let it=0;it<steps;it++){
      z=Float64Array.from(edges,e=>e.reduce((s,j)=>s+v[j],0));
      check(z.every(Number.isSafeInteger),"unsafe moment");
      if(it<steps-1){const max=Math.max(...z);check(max>0&&Number.isSafeInteger(max*scale),"unsafe normalization");v=Float64Array.from(z,x=>Math.max(1,Math.floor(x*scale/max)))}
    }
    let minMargin=Infinity;
    for(let j=0;j<S;j++){
      const left=den*z[j],right=num*v[j];check(Number.isSafeInteger(left)&&Number.isSafeInteger(right)&&v[j]>0,"unsafe comparison");
      const margin=direction==="upper"?right-left:left-right;
      check(margin>=0,"row comparison failed "+kind+" "+w+" "+j);minMargin=Math.min(minMargin,margin)
    }
    return {kind,width:w,states:S,edges:edges.reduce((s,e)=>s+e.length,0),steps,numerator:num,denominator:den,direction,minMargin,positiveVector:Array.from(v)}
  }
  const c3=strip(12,"distance2",9,226,5,"upper");
  const triUpper=strip(10,"triangular",6,3199,100,"upper");
  const triLower=strip(16,"triangular",8,230,1,"lower");
  // Compare entropy exponents without approximate logs:
  // c3 upper per column < triangular lower per column,
  // triangular upper per column < sqrt(2).
  const gapLeft=226n**17n,gapRight=230n**12n*5n**17n;
  check(gapLeft<gapRight,"entropy gap failed");
  check(3199n**2n<2n**10n*100n**2n,"triangular entropy upper failed");
  // Small exhaustive line test, illustrating the exact 001/100 argument.
  let lineControls=0;
  for(let L=2;L<=12;L++)for(let bits=0;bits<2**L;bits++){
    const s=bits.toString(2).padStart(L,"0"),ok=!s.includes("001")&&!s.includes("100");
    check(ok===(!s.includes("00")||!s.includes("1")),"line classification");lineControls++
  }
  // 10x10 safe-zero gadget: two ones with separation 3 in one row.
  // The special completion is C3-admissible, violates C4, and can be
  // inserted against any outside completion because its margin is >=3.
  const gadget=[[4,3],[4,6]],side=10;
  check(gadget.every(([r,c])=>r>=3&&c>=3&&r<side-3&&c<side-3),"gadget margin");
  check(gadget[0][0]===gadget[1][0]&&gadget[1][1]-gadget[0][1]===3,"gadget separation");
  // Source AST controls for all four square models involved in this tier.
  check(models.A202413.kind==="C"&&models.A202413.parameters.join()==="3,1","C3 source");
  check(models.A203040.kind==="C"&&models.A203040.parameters.join()==="4,1","C4 source");
  check(models.A202583.kind==="A"&&models.A202583.diagonal===1&&models.A202583.patterns.join()==="001,100","line source");
  check(models.A202484.kind==="reduced","parity source");
  const added=["A202413","A202484","A202583"],rows=[...basis.transferRows,...added.map(id=>({target:id,denominator:"1",terms:[{id,multiplier:"1"}]}))];
  check(basis.unresolved.length===4&&added.every(id=>basis.unresolved.includes(id))&&new Set(rows.map(r=>r.target)).size===rows.length,"basis inventory");
  const rank=basis.report.rank+added.length,unresolved=basis.unresolved.filter(id=>!added.includes(id));
  return {schemaVersion:1,author:"Komorebi P.",scope:"Exact constant rational linear span of 536 retained formal generating functions. Square-array independence is certified by strict strip entropy bounds, safe-zero local relaxations, and a uniform exceptional-line bound for A202583. The last boundary-factorized square model A202427 remains unresolved. The mathematical proof is supplied separately; integer row comparisons are its computational certificates.",report:{previousModels:basis.report.totalModels,previousRank:basis.report.rank,addedModels:added.length,totalModels:rows.length,rank,dependenceDimension:rows.length-rank,fullAtlasRankLowerBound:rank,fullAtlasRankUpperBound:rank+unresolved.length,unresolved:unresolved.length,exactRowInequalities:c3.states+triUpper.states+triLower.states,lineControls},basis:[...basis.basis,...added],transferRows:rows,addedBasis:added,unresolved,stripCertificates:[c3,triUpper,triLower],entropyComparison:{left:gapLeft.toString(),right:gapRight.toString(),strict:true},safeZeroGadget:{side,ones:gadget}}
}
module.exports={certifySquareSeparation};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8'),json=f=>JSON.parse(read(f));const out=certifySquareSeparation(read('OEIS_168_Array_Formulas.md'),require('../website/assets/graph-array-evaluator.js'),json('ANTIDIAGONAL_COMPLETE_TRANSFER_BASIS.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
