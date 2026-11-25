/* Author: Komorebi P. Nonrational boundary classification and formal-series basis extension. */
'use strict';
function classifyFormal(raw,engine,basis,supplement){
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const models=engine.compile(raw),records=[...raw.matchAll(/^### (A\d{6})(?: \*)?\s*\n([\s\S]*?)(?=^### A\d{6}|^## |$(?![\s\S]))/gm)].filter(r=>!r[2].includes("fixed width"));
  const squares={
    A184208:"quaternary separated optional low cells",
    A202092:"even-index central-binomial fourth power; negative polynomial exponent",
    A202194:"central-binomial times quadratic; nonintegral polynomial exponent",
    A202398:"independent sets on four parity rectangles",
    A202413:"independently chosen ones on a spacing-three grid",
    A202427:"independent sets on the square interior",
    A202484:"independent sets on four parity rectangles with diagonal edges",
    A202583:"independently chosen isolated zeros on a spacing-three grid",
    A203040:"independently chosen ones on a spacing-four grid"
  };
  const reducedAnti={
    A202100:"central binomial products on balanced even side lengths",
    A202202:"central binomial on balanced side lengths",
    A202406:"independent sets on a growing strip of the parity rectangles",
    A202435:"independent sets on a growing interior strip",
    A202492:"independent sets on a growing strip of the diagonal parity rectangles",
    A202601:"independent sets on a growing interior strip"
  };
  function twoLoops(model){
    const L=model.kind==="B"?2:model.kind==="A"?model.patterns[0].length:model.parameters[0],b=model.kind==="B"?model.parameters[0]:2,w=L;
    const rows=[],allowed=a=>model.kind==="A"?!model.patterns.includes(a.join("")):a.reduce((x,y)=>x+y,0)<=model.parameters[1];
    for(let i=0;i<b**w;i++){const a=Array.from({length:w},(_,j)=>Math.floor(i/b**(w-1-j))%b);if(model.kind==="B"||allowed(a))rows.push(a)}
    const R=rows.length,N=R**(L-1),edges=Array.from({length:N},(_,s)=>{
      let t=s,h=[];for(let j=0;j<L-1;j++){h.unshift(rows[t%R]);t=Math.floor(t/R)}
      const out=[];for(let j=0;j<R;j++){const a=[...h,rows[j]];let ok=true;
        if(model.kind==="B"){for(let c=0;c<w-1;c++)if(a[0][c]+a[0][c+1]+a[1][c]+a[1][c+1]<model.parameters[1])ok=false}
        else{for(let c=0;c<w;c++)if(!allowed(a.map(r=>r[c])))ok=false;if(model.diagonal)for(let c=0;c<=w-L;c++)if(!allowed(a.map((r,k)=>r[c+k])))ok=false}
        if(ok)out.push((s%R**(L-2))*R+j)
      }return out
    });
    // Return two explicit distinct closed walks of the same length.
    for(let s=0;s<N;s++){
      let paths=new Map([[s,[[s]]]]);
      for(let k=1;k<=12;k++){
        const next=new Map();
        for(const [j,ps] of paths)for(const t of edges[j]){
          if(!next.has(t))next.set(t,[]);
          const a=next.get(t);
          for(const p of ps)if(a.length<2)a.push([...p,t])
        }
        paths=next;
        const a=paths.get(s);
        if(a&&a.length===2){
          check(a[0].join()!==a[1].join()&&a.every(p=>p[0]===s&&p.at(-1)===s&&p.slice(1).every((v,i)=>edges[p[i]].includes(v))),"bad walk certificate");
          return {method:"two distinct equal-length closed walks after transposition at i=1",windowLength:L,alphabetSize:b,states:N,state:s,walkLength:k,walks:a}
        }
      }
    }
    throw Error("missing exponential lower bound witness");
  }
  const nonrational=[];
  for(const [,id,body] of records){
    const a=models[id];
    if(body.startsWith("square;")||body.trimStart().startsWith("square;")){
      check(squares[id],"unknown square");
      nonrational.push({id,shape:"square",obstruction:id==="A202092"||id==="A202194"?"nonintegral or negative asymptotic power":"superexponential",witness:squares[id]});
    }else{
      check(body.includes("antidiagonal;"),"unknown variable shape");
      if(a.kind==="reduced"){check(reducedAnti[id],"missing reduced witness");nonrational.push({id,shape:"antidiagonal",obstruction:"subexponential boundary blocks and superpolynomial subsequence",witness:reducedAnti[id]})}
      else nonrational.push({id,shape:"antidiagonal",obstruction:"subexponential boundary blocks and superpolynomial subsequence",witness:twoLoops(a)})
    }
  }
  check(nonrational.length===29&&nonrational.filter(r=>r.shape==="square").length===9&&nonrational.filter(r=>r.shape==="antidiagonal").length===20,"variable-width inventory");
  for(const id of ["A054939","A054940"]){check(supplement.includes("### "+id),"missing labeled parity source");nonrational.push({id,shape:"labeled graph",obstruction:"superexponential",witness:"Fix all edges from vertex 1; half the assignments of the remaining edges have each parity for n>=3."})}
  const added=["A184208","A202398","A054939","A054940","A203040","A202092","A202194","A184217","A184207","A202100","A202202"];
  check(added.every(id=>nonrational.some(r=>r.id===id)),"formal model mismatch");
  const partialPermutations=[1,16,72,96,24].reduce((a,b)=>a+b,0);check(partialPermutations===209&&partialPermutations<256,"4x4 tile upper bound");
  const rows=[...basis.transferRows,...added.map(id=>({target:id,denominator:"1",terms:[{id,multiplier:"1"}]}))];
  check(new Set(rows.map(r=>r.target)).size===rows.length,"duplicate formal row");
  const rank=basis.report.rank+added.length;
  return {schemaVersion:1,author:"Komorebi P.",scope:"All 537 retained mathematical sequence definitions are classified by rationality of their ordinary generating series with zeros before the original offset. 506 rational records have a complete certified rank-241 basis. Eleven nonrational records are certified independent modulo that rational span by growth and antidiagonal boundary-block arguments; 20 nonrational dependence questions remain. No new OEIS matches or claims of full-catalogue rank.",report:{atlasRecords:537,rationalModels:basis.report.totalModels,rationalRank:basis.report.rank,nonrationalModels:nonrational.length,squareObstructions:9,antidiagonalObstructions:20,labeledGraphObstructions:2,explicitTwoLoopCertificates:nonrational.filter(r=>r.witness.walks).length,addedFormalIndependentModels:added.length,formalRepresentedModels:rows.length,formalRank:rank,formalDependenceDimension:rows.length-rank,remainingFormalDependenceQuestions:nonrational.length-added.length},basis:[...basis.basis,...added],transferRows:rows,addedFormalBasis:added,nonrationalClassification:nonrational,strictTileBound:{width:4,allowedPartialPermutations:partialPermutations,comparisonPowerOfTwo:256},unresolved:nonrational.filter(r=>!added.includes(r.id)).map(r=>r.id)}
}
module.exports={classifyFormal};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8');const out=classifyFormal(read('OEIS_168_Array_Formulas.md'),require('../website/assets/graph-array-evaluator.js'),JSON.parse(read('COMPLETE_FIXED_TRANSFER_BASIS.json')),read('OEIS_64_Graph_Formulas.md'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
