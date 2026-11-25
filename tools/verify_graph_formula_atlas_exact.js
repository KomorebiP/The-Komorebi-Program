/* Author: Komorebi P.
 * Exact all-index audit of the archived graph atlas. No dependencies beyond Node.js.
 * Run: node tools/verify_graph_formula_atlas_exact.js
 * Each (1-x^d)^e lane is reduced by its extraneous cyclotomic factors.
 * Clearing the remaining denominators and integer scales gives a polynomial identity.
 * This checks representation equivalence, reduced denominator orders and periods,
 * not the combinatorial proofs or independent OEIS matches.
 */
'use strict';
function audit(g,l){
  const fail=m=>{throw Error(m)};
  function records(s){const a=[...s.matchAll(/^### ([A-Z]+\d+)[^\n]*\n([\s\S]*?)(?=^## |^### |$(?![\s\S]))/gm)];const r=new Map(a.map(m=>[m[1],m[2]]));if(a.length!==r.size)fail("Duplicate record");return r}
  const G=records(g),L=records(l);if(G.size!==288||L.size!==288||[...G.keys()].some(id=>!L.has(id)))fail("Core inventory mismatch");
  const trim=a=>{while(a.length>1&&a.at(-1)===0n)a.pop();return a.length?a:[0n]};
  const mul=(a,b)=>{const z=Array(a.length+b.length-1).fill(0n);a.forEach((x,i)=>{if(x)b.forEach((y,j)=>{if(y)z[i+j]+=x*y})});return trim(z)};
  const add=(a,b)=>trim(Array.from({length:Math.max(a.length,b.length)},(_,i)=>(a[i]??0n)+(b[i]??0n)));
  const scale=(a,h)=>trim(a.map(x=>x*h));
  const pow=(a,e)=>{let z=[1n];while(e--)z=mul(z,a);return z};
  function div(a,b){let r=trim([...a]),q=Array(Math.max(1,r.length-b.length+1)).fill(0n);while(r.length>=b.length&&r.some(x=>x)){let i=r.length-b.length;if(r.at(-1)%b.at(-1))fail("Noninteger quotient");let c=r.at(-1)/b.at(-1);q[i]=c;b.forEach((x,j)=>r[i+j]-=x*c);trim(r)}return [trim(q),r]}
  function exact(a,b){const [q,r]=div(a,b);if(r.some(x=>x))fail("Nonzero remainder");return q}
  const one=d=>[1n,...Array(d-1).fill(0n),-1n];
  const phis=new Map();
  function phi(d){if(!phis.has(d)){let a=one(d);for(let k=1;k<d;k++)if(d%k===0)a=exact(a,phi(k));phis.set(d,a)}return phis.get(d)}
  const gcd=(a,b)=>b===0n?a:gcd(b,a%b),lcm=(a,b)=>a/gcd(a,b)*b;
  function block(s){let z=[];for(const ln of s.trim().split("\n")){const m=ln.match(/^\s*(\d+)-(\d+)\s+(.+)$/);if(!m||Number(m[1])!==z.length)fail("Coefficient block start");z.push(...m[3].split(",").map(BigInt));if(z.length!==Number(m[2])+1)fail("Coefficient block end")}return z}
  const tidy=s=>s.replace(/\\(?:begin|end)\{aligned\}|\\\\|&|\\times|\s/g,"");
  function parseR(s,b){s=tidy(s).replace(/^R\(x\)=/,"");if(s.startsWith("\\sum")){const z=block(b.match(/```text\n([\s\S]*?)\n```/)[1]);if(z.length!==Number(s.match(/\^\{(\d+)\}/)[1])+1)fail("Numerator block degree");return trim(z)}let z=[0n];while(s.length){const m=s.match(/^([+-]?)(\d*)(x(?:\^\{(\d+)\})?)?/);if(!m[0]||!m[2]&&!m[3])fail("Numerator parse: "+s);const k=m[3]?Number(m[4]??1):0;while(z.length<=k)z.push(0n);z[k]+=BigInt(m[2]||"1")*(m[1]==="-"?-1n:1n);s=s.slice(m[0].length)}return trim(z)}
  let passed=0,lanes=0,orders=0,periods=0,maxOrder=0;
  const distinct=new Set();
  for(const [id,b] of G){try{
    const formulas=[...b.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(m=>m[1]);if(formulas.length!==4)fail("Formula count");
    const shift=Number(b.match(/n<(\d+)/)[1]),r=parseR(formulas[2],b),p=[...Array(shift).fill(0n),...r];if(!r[0])fail("Noncanonical numerator shift");
    let q=[1n],t=tidy(formulas[3]).replace(/^Q\(x\)=/,"");const factors=new Map();
    while(t){const m=t.match(/^\\Phi_\{(\d+)\}\(x\)(?:\^\{(\d+)\})?/);if(!m)fail("Denominator parse: "+t);const d=Number(m[1]),e=Number(m[2]??1);if(!d||!e||factors.has(d))fail("Invalid factor");factors.set(d,e);q=mul(q,pow(phi(d),e));if(!div(r,phi(d))[1].some(x=>x))fail("Unreduced denominator");t=t.slice(m[0].length)}
    const meta=b.match(/Order (\d+); period (\d+)/),period=[...factors.keys()].reduce((a,d)=>lcm(a,BigInt(d)),1n);
    if(q.length-1!==Number(meta[1]))fail("Order mismatch");orders++;
    if(period!==BigInt(meta[2]))fail("Period mismatch");periods++;maxOrder=Math.max(maxOrder,q.length-1);
    const lb=L.get(id),s=lb.match(/Finite polynomial part S \(ascending\): `([^`]+)`/)[1].split(",").map(BigInt);
    const rows=[...lb.matchAll(/\*\*d=(\d+), e=(\d+), h=(\d+)\*\*\s*```text\n([\s\S]*?)\n```/g)];
    if(rows.length!==factors.size||rows.length!==[...lb.matchAll(/\*\*d=/g)].length)fail("Lane count mismatch");
    const H=rows.reduce((a,m)=>lcm(a,BigInt(m[3])),1n);let total=scale(mul(q,s),H);const seen=new Set();
    for(const m of rows){const d=Number(m[1]),e=Number(m[2]),h=BigInt(m[3]),c=block(m[4]);if(e!==factors.get(d)||seen.has(d)||h<=0n||c.length>d*e)fail("Invalid lane");seen.add(d);const pd=pow(phi(d),e),extraneous=exact(pow(one(d),e),pd),u=exact(trim(c),extraneous);total=add(total,scale(mul(exact(q,pd),u),H/h));lanes++}
    const expected=scale(p,H);if(total.length!==expected.length||total.some((x,i)=>x!==expected[i]))fail("Rational identity mismatch");
    distinct.add(p.join(",")+"/"+q.join(","));passed++;
  }catch(e){fail(id+": "+e.message)}}
  if(distinct.size!==262)fail("Distinct model count mismatch");
  return {identities:passed,lanes,orders,periods,distinct:distinct.size,maxOrder}
}

module.exports = { audit };
if (require.main === module) {
  const fs = require('node:fs');
  const path = require('node:path');
  const dir = path.join(__dirname, '..', 'research', 'graph-formula-atlas');
  const g = fs.readFileSync(path.join(dir, 'Graph_288_Formulas.md'), 'utf8');
  const l = fs.readFileSync(path.join(dir, 'Graph_288_Binomial_Lanes.md'), 'utf8');
  const report = audit(g, l);
  const altered = l.replace('  0-0    1\n', '  0-0    2\n');
  if (altered === l) throw Error('Negative control not constructed');
  let rejected = false;
  try { audit(g, altered); } catch (e) {
    if (!e.message.includes('G01: Rational identity mismatch')) throw e;
    rejected = true;
  }
  if (!rejected) throw Error('Negative control accepted');
  console.log(JSON.stringify({ ...report, negativeControlRejected: rejected }, null, 2));
}
