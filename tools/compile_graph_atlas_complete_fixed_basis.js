/* Author: Komorebi P. Finish the fixed-width transfer basis by exact Perron separation. */
'use strict';
function completeFixedBasis(raw,engine,basis,compact){
  const check=(a,m)=>{if(!a)throw Error(m)};
  const models=engine.compile(raw),binaryBounds=[],quaternaryWidths=[];
  // Growth bounds are represented in doubled powers of 2 per index.
  // Affine arguments with h,k have slope 1/2. Fixed lower binomial
  // arguments give polynomial factors, which have nth-root limit 1.
  function affine(a){const [op,x,y]=a;if(op==="const")return {slope2:0,constant:Number(x)};if(op==="var"){check(["n","h","k"].includes(x),"unexpected fixed-width variable");return {slope2:x==="n"?2:1,constant:x==="n"?0:2}}if(op==="add"){const b=affine(x),c=affine(y);return {slope2:b.slope2+c.slope2,constant:b.constant+c.constant}}throw Error("nonaffine argument")}
  function constant(a){const x=affine(a);check(x.slope2===0,"nonconstant parameter");return x.constant}
  function growth(a){const [op,x,y,z]=a;
    if(op==="const"||op==="var")return 0;
    if(op==="add")return Math.max(growth(x),growth(y));
    if(op==="mul")return growth(x)+growth(y);
    if(op==="pow")return growth(x)*constant(y);
    if(op==="choose"){constant(y);affine(x);return 0}
    if(op==="fib")return affine(x).slope2;
    if(op==="ind"){constant(y);return constant(x)*affine(z).slope2}
    throw Error("unsupported reduced expression")
  }
  const fixedRecords=[...raw.matchAll(/^### (A\d{6})(?: \*)?\s*\n([\s\S]*?)(?=^### A\d{6}|^## |$(?![\s\S]))/gm)].filter(r=>r[2].includes("fixed width"));
  for(const [,id,body] of fixedRecords){
    const a=models[id],w=Number(body.match(/fixed width (\d+)/)[1]);
    if(a.kind==="reduced"){const g=growth(a.expr);check(g<=18,"binary reduced growth exceeds 512 "+id);binaryBounds.push({id,width:w,method:"AST polynomial/exponential bound",growthPowerOfTwoDoubled:g});continue}
    check(a.w[0]==="const"&&Number(a.w[1])===w&&a.exponent==="n","fixed-width model mismatch "+id);
    if(a.kind==="B"&&a.parameters[0]===4){check(a.parameters[1]===7,"unexpected quaternary threshold");quaternaryWidths.push({id,width:w});continue}
    const L=a.kind==="B"?2:a.kind==="A"?a.patterns[0].length:a.parameters[0],R=2**w;
    let horizontalRows=0;
    for(let j=0;j<R;j++){const s=j.toString(2).padStart(w,"0");let ok=true;
      if(a.kind!=="B")for(let k=0;k<=w-L;k++){const t=s.slice(k,k+L);if(a.kind==="A"?a.patterns.includes(t):t.split("1").length-1>a.parameters[1]){ok=false;break}}
      if(ok)horizontalRows++
    }
    check(horizontalRows<=512,"binary row growth exceeds 512 "+id);binaryBounds.push({id,width:w,method:"horizontal row count",horizontalRows})
  }
  check(fixedRecords.length===139&&quaternaryWidths.length===8&&binaryBounds.length===131,"fixed-width inventory");
  check(quaternaryWidths.map(r=>r.width).sort((a,b)=>a-b).join()==="2,3,4,5,6,7,8,9","quaternary width sequence");
  const proposed=compact.spectral;
  check(proposed.map(m=>m.width).sort((a,b)=>a-b).join()==="6,7,8,9","remaining quaternary widths");
  check(proposed.every(m=>quaternaryWidths.some(r=>r.id===m.id&&r.width===m.width)),"quaternary binding mismatch");
  check(quaternaryWidths.filter(r=>r.width<=5).every(r=>basis.transferRows.some(x=>x.target===r.id)),"missing lower widths");
  function count(w,H){
    const N=4**w,rows=Array.from({length:N},(_,i)=>Array.from({length:w},(_,j)=>(i>>(2*j))&3));
    const edges=rows.map(a=>rows.map((b,j)=>{for(let k=0;k<w-1;k++)if(a[k]+a[k+1]+b[k]+b[k+1]<7)return -1;return j}).filter(j=>j>=0));
    let v=Array(N).fill(1n);
    for(let i=1;i<H;i++)v=edges.map(r=>r.reduce((s,j)=>s+v[j],0n));
    return v.reduce((s,x)=>s+x,0n)
  }
  // By transposition, 3 x 6 and 5 x 6 counts can be computed at widths 3 and 5.
  const a2=count(3,6),a4=count(5,6),bound=512n;
  check(a4>bound*bound*a2,"strict Perron lower bound fails");
  check(a2===601469417n&&a4===208292231201647n,"retained exact count mismatch");
  // Independently check the active-row and embedding predicates exhaustively on small widths.
  let activeChecks=0,embeddingChecks=0;
  const compat=(a,b)=>a.slice(1).every((x,j)=>x+a[j]+b[j]+b[j+1]>=7);
  const row=(i,w)=>Array.from({length:w},(_,j)=>(i>>(2*j))&3);
  for(let w=2;w<=4;w++){
    const all3=Array(w).fill(3);
    for(let i=0;i<4**w;i++){const a=row(i,w),active=a.slice(1).every((x,j)=>x+a[j]>=1);check(compat(a,all3)===active,"active predicate");
      for(let j=0;j<4**w;j++){const b=row(j,w),e=compat(a,b);check(!e||active,"inactive row edge");check(e===compat([...a,3],[...b,3]),"embedding predicate");embeddingChecks++}
      activeChecks++
    }
  }
  const ids=proposed.map(r=>r.id),rows=[...basis.transferRows,...ids.map(id=>({target:id,denominator:"1",terms:[{id,multiplier:"1"}]}))];
  check(new Set(rows.map(r=>r.target)).size===rows.length,"duplicate transfer row");
  check(fixedRecords.every(r=>rows.some(m=>m.target===r[1])),"incomplete fixed-width coverage");
  const rank=basis.report.rank+ids.length;
  return {schemaVersion:1,author:"Komorebi P.",scope:"All 506 rational atlas records consisting of graph/tree core and complement models, fixed-width binary and quaternary arrays, and four walk models. Exact constant rational linear span. Compact finite-state realizations do not certify minimal scalar recurrence orders. Spectral independence uses a proved strictly increasing Perron root and exact count bounds, not numerical eigensolvers.",report:{previousModels:basis.report.totalModels,previousRank:basis.report.rank,addedSpectralModels:ids.length,totalModels:rows.length,rank,dependenceDimension:rows.length-rank,fixedWidthArrays:fixedRecords.length,remainingFixedWidthModels:0,binaryGrowthBounds:binaryBounds.length,activeRowControls:activeChecks,embeddingControls:embeddingChecks},basis:[...basis.basis,...ids],transferRows:rows,addedBasis:ids,spectralCertificate:{threshold:7,alphabetSize:4,binaryGrowthUpperBound:512,width:6,moment2:a2.toString(),moment4:a4.toString(),strictInequalityMargin:(a4-bound*bound*a2).toString(),quaternaryWidths},binaryBounds}
}
module.exports={completeFixedBasis};
if(require.main===module){const fs=require('node:fs'),path=require('node:path');const dir=path.join(__dirname,'..','research','graph-formula-atlas');const read=f=>fs.readFileSync(path.join(dir,f),'utf8'),json=f=>JSON.parse(read(f));const out=completeFixedBasis(read('OEIS_168_Array_Formulas.md'),require('../website/assets/graph-array-evaluator.js'),json('COMPACT_ENLARGED_TRANSFER_BASIS.json'),json('FIXED_STATE_ARRAY_COMPACT_DEFERRED.json'));if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out)+'\n');console.log(JSON.stringify(out.report,null,2));}
