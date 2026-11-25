// Author: Komorebi P.
// Exact standard-library JavaScript reproduction. Node.js 18+.
// Source reference data: OEIS Foundation Inc., CC BY-SA 4.0; see the research note.

function check(ok,msg){if(!ok)throw Error(msg)}

function mod(a,p){return (a%p+p)%p}

function powmod(a,n,p){let z=1n;for(a=mod(a,p);n;n>>=1n,a=a*a%p)if(n&1n)z=z*a%p;return z}

function stripValues(w,H){
  const rows=Array.from({length:2**w},(_,a)=>a).filter(a=>!(a&(a<<1)));
  let v=rows.map(a=>a===0?1n:0n), out=[1n];
  const edges=rows.map(a=>rows.map((b,j)=>((a&b)||((a<<1)&b))?-1:j).filter(j=>j>=0));
  for(let h=1;h<=H;h++){let z=rows.map(()=>0n);for(let i=0;i<v.length;i++)for(const j of edges[i])z[j]+=v[i];v=z;out.push(v.reduce((a,b)=>a+b,0n))}
  return out
}

function rect(H,W){const h=H>>1,k=H-h,w=W>>1,l=W-w;const A=stripValues(w,k),B=stripValues(l,k);return A[h]*A[k]*B[h]*B[k]}

function sequence(W,N){const H=Math.ceil((N+2)/2),w=W>>1;const A=stripValues(w,H),B=stripValues(W-w,H);return Array.from({length:N},(_,i)=>{const h=(i+3)>>1,k=i+3-h;return A[h]*A[k]*B[h]*B[k]})}

function brute(H,W){let count=0n;let triples=[];for(let i=0;i<H;i++)for(let j=0;j<W;j++)for(const [di,dj] of [[0,1],[1,0],[1,1]])if(i+2*di<H&&j+2*dj<W)triples.push([i*W+j,(i+di)*W+j+dj,(i+2*di)*W+j+2*dj]);for(let a=0;a<2**(H*W);a++){let ok=true;for(const [i,j,k] of triples){let p=4*((a>>i)&1)+2*((a>>j)&1)+((a>>k)&1);if(p===0||p===2){ok=false;break}}if(ok)count++}return count}

function gfCoeffs(P,Q,H){let a=[];for(let m=0;m<=H;m++){let v=BigInt(P[m]??0);for(let i=1;i<Q.length&&i<=m;i++)v-=BigInt(Q[i])*a[m-i];a.push(v)}return a}

function packed(P,Q,m,B){const D=Q.length-1;const evalAt=A=>A.reduce((v,c,i)=>v+BigInt(c)*B**BigInt(D-i),0n);return (B**BigInt(m)*evalAt(P)/evalAt(Q))%B}

function bm(s,p){let C=[1n],B=[1n],L=0,m=1,b=1n;for(let n=0;n<s.length;n++){let d=mod(s[n],p);for(let i=1;i<=L;i++)d=mod(d+(C[i]??0n)*s[n-i],p);if(!d){m++;continue}const T=C.slice(),f=d*powmod(b,p-2n,p)%p;while(C.length<B.length+m)C.push(0n);for(let j=0;j<B.length;j++)C[j+m]=mod(C[j+m]-f*B[j],p);if(2*L<=n){L=n+1-L;B=T;b=d;m=1}else m++}while(C.length<L+1)C.push(0n);return C.slice(0,L+1)}

function recurrenceCertificate(W,degree,D){
  const seq=sequence(W,2*D+2),primes=[2147483647n,1000000007n,1000000009n];let Q=[],M=1n;
  for(const p of primes){const C=bm(seq.map(x=>mod(x,p)),p);check(C.length===degree+1,"modular degree "+W);if(M===1n){Q=C;M=p;continue}const inv=powmod(M,p-2n,p);Q=Q.map((v,j)=>v+M*mod((C[j]-v)*inv,p));M*=p}
  Q=Q.map(v=>v>M/2n?v-M:v);check(Q[0]===1n,"monic");
  // The parity-lift state dimension is D. D consecutive zero residuals prove all subsequent residuals zero.
  for(let t=degree;t<degree+D;t++){let z=0n;for(let j=0;j<=degree;j++)z+=Q[j]*seq[t-j];check(z===0n,"exact recurrence residual "+W+" "+t)}
  const P=Array.from({length:degree},(_,t)=>Q.slice(0,t+1).reduce((z,q,j)=>z+q*seq[t-j],0n));
  const trace2=Q[1]**2n-2n*Q[2];check(trace2<0n,"negative trace");
  // v29 single-mark weighted lift. Coordinate 0 is the reference; p is reversed Q.
  const p=Q.slice().reverse(),r=degree,w=p.slice(0,r).map(v=>1n+(v>0n?v:0n));
  const g=w.map((_,j)=>(j?w[j-1]:0n)-w[r-1]*p[j]);
  const beta=1n+g.reduce((best,x,j)=>{let c=x>0n?(x+w[j]-1n)/w[j]:0n;return c>best?c:best},0n);
  const K=w[r-1]+beta, top=w.map((v,j)=>v*beta-g[j]),bottom=w.map((v,j)=>v-p[j]);
  check(top.every(v=>v>0n)&&bottom.every(v=>v>0n),"positive lift");
  // Check BJ=JM and (B-KI)e0=Je_r columnwise via sparse multiplication.
  function step(v){let z=Array(r+1).fill(0n);z[0]=beta*v[0]+top.reduce((s,x,j)=>s+x*v[j+1],0n);z[r]=v[0]+bottom.reduce((s,x,j)=>s+x*v[j+1],0n);for(let i=1;i<r;i++)z[i]=v[i+1];return z}
  let v=Array(r+1).fill(0n);v[0]=1n;const e=step(v);check(e[0]-K===-w[r-1]&&e[r]===1n&&e.slice(1,r).every(x=>!x),"impulse injection");
  for(let j=0;j<r;j++){let x=Array(r+1).fill(0n);x[0]=-w[j];x[j+1]=1n;let b=step(x);let y=Array(r).fill(0n);if(j)y[j-1]=1n;y[r-1]-=p[j];check(b[0]===-w.reduce((s,z,k)=>s+z*y[k],0n)&&y.every((z,k)=>z===b[k+1]),"intertwining")}
  const c=[];for(let i=0;i<r+16;i++){c.push(v[1]);v=step(v)}
  const N=P.slice().reverse();
  for(let n=0;n<15;n++)check(N.reduce((z,x,j)=>z+x*(c[n+j+1]-K*c[n+j]),0n)===seq[n],"graph target");
  return {width:W,degree,dimension_bound:D,modular_prime_checks:primes.length,exact_residuals:D,trace_square:trace2.toString(),minimum_weighted_vertices:r+1,K:K.toString(),lift_columns:r,graph_target_checks:15,recurrence_Q:Q.map(String),numerator_P:P.map(String)}
}

function runChecks(ref){
  let bruteChecks=0,sourceChecks=0,geometryChecks=0,gfChecks=0,packChecks=0;
  for(let h=0;h<=5;h++)for(let w=0;w<=5;w++)if(h*w<=16){check(rect(h,w)===brute(h,w),"direct array "+h+","+w);bruteChecks++}
  for(let h=1;h<=16;h++)for(let k=1;k<=4;k++){let a=rect(h,2*k+1);check(a*a===rect(h,2*k)*rect(h,2*k+2),"width parity law");check(rect(h,2*k)===rect(2*k,h),"transpose");geometryChecks+=2}
  for(const f of ref){const s=sequence(f.width,f.terms.length);check(s.every((v,i)=>v===BigInt(f.terms[i])),"OEIS reference "+f.id);sourceChecks+=s.length}
  const GF=[[[1,1],[1,-1,-1]],[[1,2,1],[1,-1,-2,-1]],[[1,4,3,0,-1],[1,-1,-5,-4,0,1]]];
  for(let w=1;w<=3;w++){const a=gfCoeffs(...GF[w-1],100),b=stripValues(w,100);check(a.every((v,i)=>v===b[i]),"generating function "+w);gfChecks+=a.length}
  const a=sequence(3,100),b=sequence(5,100);
  for(let n=1;n<=100;n++){const B=2n**BigInt(8*n+24),h=(n+2)>>1,k=n+2-h;const v=GF.map(([P,Q])=>packed(P,Q,h,B)*packed(P,Q,k,B));check(v[0]*v[1]===a[n-1]&&v[1]*v[2]===b[n-1],"integer floor formula "+n);packChecks+=2}
  const recurrences=[recurrenceCertificate(3,30,72),recurrenceCertificate(5,165,450)];
  return {direct_exhaustive_rectangles:bruteChecks,source_term_checks:sourceChecks,source_ids:ref.length,geometry_checks:geometryChecks,generating_function_checks:gfChecks,packed_formula_checks:packChecks,eighth_terms:[a[7].toString(),b[7].toString()],recurrences}
}

const reference = [
  {
    "id": "A202485",
    "width": 3,
    "offset": 1,
    "terms": [
      "108",
      "324",
      "1170",
      "4225",
      "14560",
      "50176",
      "174720",
      "608400",
      "2113020",
      "7338681",
      "25513362",
      "88698724",
      "308204050",
      "1070925625",
      "3722206950",
      "12937242564",
      "44959937760",
      "156246278400",
      "543023015040",
      "1887238517824",
      "6558819027904",
      "22794207851584"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202485.seq"
  },
  {
    "id": "A202486",
    "width": 4,
    "offset": 1,
    "terms": [
      "324",
      "1296",
      "6084",
      "28561",
      "132496",
      "614656",
      "2822400",
      "12960000",
      "59907600",
      "276922881",
      "1276847289",
      "5887339441",
      "27163984225",
      "125333700625",
      "578223368100",
      "2667616624656",
      "12306835772100",
      "56776601750625",
      "261938687630400"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202486.seq"
  },
  {
    "id": "A202487",
    "width": 5,
    "offset": 1,
    "terms": [
      "1170",
      "6084",
      "42588",
      "298116",
      "1926288",
      "12446784",
      "81920160",
      "539168400",
      "3534548400",
      "23170928400",
      "152046773640",
      "997725295044",
      "6544683664680",
      "42930538579600",
      "281655584169120",
      "1847865662028864",
      "12122369483494680",
      "79525175944347225"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202487.seq"
  },
  {
    "id": "A202488",
    "width": 6,
    "offset": 1,
    "terms": [
      "4225",
      "28561",
      "298116",
      "3111696",
      "28005264",
      "252047376",
      "2377732644",
      "22430753361",
      "208538355600",
      "1938777760000",
      "18105705806400",
      "169084146471696",
      "1576826282769984",
      "14704992620052736",
      "137195887385735424"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202488.seq"
  },
  {
    "id": "A202489",
    "width": 7,
    "offset": 1,
    "terms": [
      "14560",
      "132496",
      "1926288",
      "28005264",
      "349399008",
      "4359168576",
      "56953820952",
      "744118440129",
      "9593661694500",
      "123687762250000",
      "1600355267745000",
      "20706470360604900",
      "267678301470603000",
      "3460351852844410000"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202489.seq"
  },
  {
    "id": "A202490",
    "width": 8,
    "offset": 1,
    "terms": [
      "50176",
      "614656",
      "12446784",
      "252047376",
      "4359168576",
      "75391979776",
      "1364214656016",
      "24685405970481",
      "441349719305625",
      "7890879937890625",
      "141454688946390625",
      "2535766502901450625",
      "45440435551542015625",
      "814283641948594140625"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202490.seq"
  },
  {
    "id": "A202491",
    "width": 9,
    "offset": 1,
    "terms": [
      "174720",
      "2822400",
      "81920160",
      "2377732644",
      "56953820952",
      "1364214656016",
      "34683335205048",
      "881777464888644",
      "22015082631334650",
      "549644193193005625",
      "13795021325301502000",
      "346228734374528569600",
      "8677470058423398780000"
    ],
    "url": "https://raw.githubusercontent.com/oeis/oeisdata/c5bd71de9eee0894df1301baa4f43f6431d8a08d/seq/A202/A202491.seq"
  }
];
console.log(JSON.stringify(runChecks(reference),null,2));
