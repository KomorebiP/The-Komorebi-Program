/**
 * Safe, read-only display adapters for the pinned OEIS transfer index.
 * No expression is evaluated. An unsupported grammar has a plain-source fallback.
 * Author: Komorebi P.
 */
const TOKEN = /A\d{6}|n|u|\d+|\*\*|[()+*/^=-]/y;
const GAUGE = /^b\(t\)\/a\(t\) = K\*c\^\(t-t0\)\*L\(t\)\/L\(t0\); K=([^,]+), c=([^,]+), t0=(\d+), L\(t\)=(.*); offsets a=([-+]?\d+), b=([-+]?\d+)$/;
const RIORDAN = /^R\[c=(-?\d+),s=(-?\d+),r=(-?\d+),t=(-?\d+)\] OGF transform$/;

export function algebraLatex(source) {
  if (typeof source!=='string' || !source.length || source.length>1000) return null;
  const text=source.replace(/\s+/g,'');
  const tokens=[];
  for(let i=0;i<text.length;){
    TOKEN.lastIndex=i;
    const match=TOKEN.exec(text);
    if(!match || match.index!==i || tokens.length>300)return null;
    tokens.push(match[0]);i=TOKEN.lastIndex;
  }
  let cursor=0,depth=0;
  const peek=()=>tokens[cursor],take=()=>tokens[cursor++];
  const requireToken=token=>{if(take()!==token)throw Error('Unexpected token');};
  function primary(){
    if(++depth>48)throw Error('Too much nesting');
    try{
      const t=take();
      if(t==='('){const value=add();requireToken(')');return {type:'group',value};}
      if(/^\d+$/.test(t||''))return {type:'literal',value:t};
      if(t==='n'||t==='u')return {type:'literal',value:t};
      if(/^A\d{6}$/.test(t||'')){requireToken('(');const index=add();requireToken(')');return {type:'sequence',name:t,index};}
      throw Error('Unsupported arithmetic token');
    }finally{depth--;}
  }
  function power(){
    let left=primary();
    if(peek()==='**'||peek()==='^'){take();left={type:'power',left,right:unary()};}
    return left;
  }
  function unary(){
    if(peek()==='+'){take();return unary();}
    if(peek()==='-'){take();return {type:'negative',value:unary()};}
    return power();
  }
  function product(){
    let left=unary();
    while(peek()==='*'||peek()==='/'){
      const op=take();left={type:op==='*'?'multiply':'divide',left,right:unary()};
    }
    return left;
  }
  function add(){
    let left=product();
    while(peek()==='+'||peek()==='-'){
      const op=take();left={type:op==='+'?'add':'subtract',left,right:product()};
    }
    return left;
  }
  function relation(){
    let value=add();
    if(peek()==='='){take();value={type:'equal',left:value,right:add()};}
    if(cursor!==tokens.length)throw Error('Trailing tokens');
    return value;
  }
  function render(tree){
    switch(tree.type){
      case 'literal':return tree.value;
      case 'sequence':return '\\mathrm{'+tree.name+'}\\!\\left('+render(tree.index)+'\\right)';
      case 'group':return '\\left('+render(tree.value)+'\\right)';
      case 'negative':return '-'+render(tree.value);
      case 'power':return '{'+render(tree.left)+'}^{'+render(tree.right)+'}';
      case 'multiply':return render(tree.left)+'\\cdot '+render(tree.right);
      case 'divide':return '\\frac{'+render(tree.left)+'}{'+render(tree.right)+'}';
      case 'add':return render(tree.left)+'+'+render(tree.right);
      case 'subtract':return render(tree.left)+'-'+render(tree.right);
      case 'equal':return render(tree.left)+'='+render(tree.right);
      default:throw Error('Unknown syntax tree');
    }
  }
  try{return render(relation());}catch{return null;}
}

function friendly(source){
  return source.replace(/\*\*/g,'^').replace(/\*/g,' × ').replace(/ - /g,' − ').replace(/\s+/g,' ').trim();
}
function rationalLatex(value){
  const m=/^(-?\d+)(?:\/(\d+))?$/.exec(value);
  if(!m)return null;
  return m[2]?'\\frac{'+m[1]+'}{'+m[2]+'}':m[1];
}

function gaugeGcd(a,b){
  a=a<0n?-a:a;b=b<0n?-b:b;
  while(b!==0n){const r=a%b;a=b;b=r;}return a;
}

function gaugeFraction(n,d){
  if(d===0n)throw Error('Zero gauge denominator');
  if(d<0n){n=-n;d=-d;}
  const g=gaugeGcd(n,d);return [n/g,d/g];
}

function gaugeRational(text){
  if(!/^-?\d{1,18}(?:\/\d{1,18})?$/.test(text))throw Error('Unsupported gauge rational');
  const [n,d='1']=text.split('/');return gaugeFraction(BigInt(n),BigInt(d));
}

function gaugeLinear(a,b){
  const t=a===0n?'':a===1n?'t':a===-1n?'-t':String(a)+'t';
  return t?(t+(b===0n?'':b>0n?'+'+b:String(b))):String(b);
}

function gaugeIndex(offset){
  return 't'+(offset===0n?'':offset>0n?'+'+offset:String(offset));
}

function specializedGauge(edge,match=GAUGE.exec(String(edge?.expression||''))){
  try{
    if(!match || !/^A\d{6}$/.test(edge.target)||edge.inputs?.length!==1||
       !/^A\d{6}$/.test(edge.inputs[0]))return null;
    const maps=edge.index_maps?.[edge.inputs[0]];
    if(JSON.stringify(maps)!=='[[1,0]]')return null;
    const [,k,c,start,product,sourceOffset,targetOffset]=match;
    if(!/^\d{1,5}$/.test(start)||!/^[-+]?\d{1,12}$/.test(sourceOffset)||
       !/^[-+]?\d{1,12}$/.test(targetOffset)||Number(start)!==edge.valid_from)return null;
    const t0=BigInt(start),oa=BigInt(sourceOffset),ob=BigInt(targetOffset);
    let [num,den]=gaugeRational(k);
    const [baseN,baseD]=gaugeRational(c);
    if(num===0n||baseN===0n)return null;
    const factors=[];
    if(product!=='1'){
      const pieces=product.split(/(?<=\^\-?\d+)\*(?=\()/);
      if(pieces.length>8)return null;
      for(const piece of pieces){
        const f=/^\((-?\d{1,18})\*n([+-]\d{1,18})\)\^(-?\d{1,2})$/.exec(piece);
        if(!f)return null;
        const a=BigInt(f[1]),b=BigInt(f[2]),power=Number(f[3]);
        if(a===0n||power===0||Math.abs(power)>12)return null;
        const value=a*t0+b;
        if(value===0n)return null;
        const v=value**BigInt(Math.abs(power));
        [num,den]=power>0?gaugeFraction(num,den*v):gaugeFraction(num*v,den);
        factors.push({a:String(a),b:String(b),power});
      }
    }
    const top=[],bottom=[],plainTop=[],plainBottom=[];
    const sign=num<0n?'-':'';
    const absNum=num<0n?-num:num;
    if(absNum!==1n){top.push(String(absNum));plainTop.push(String(absNum));}
    if(den!==1n){bottom.push(String(den));plainBottom.push(String(den));}
    if(baseN!==baseD){
      const base=baseD===1n?String(baseN):'\\frac{'+baseN+'}{'+baseD+'}';
      const wrapped=baseN<0n||baseD!==1n?'\\left('+base+'\\right)':base;
      const exp=t0===0n?'t':'t-'+t0;
      top.push(wrapped+'^{'+exp+'}');
      const pbase=baseD===1n&&baseN>0n?String(baseN):'('+baseN+(baseD!==1n?'/'+baseD:'')+')';
      plainTop.push(pbase+'^('+exp+')');
    }
    for(const f of factors){
      const linear=gaugeLinear(BigInt(f.a),BigInt(f.b));
      const power=Math.abs(f.power);
      const grouped=linear==='t'?'t':'\\left('+linear+'\\right)';
      const plainGrouped=linear==='t'?'t':'('+linear+')';
      (f.power>0?top:bottom).push(grouped+(power===1?'':'^{'+power+'}'));
      (f.power>0?plainTop:plainBottom).push(plainGrouped+(power===1?'':'^'+power));
    }
    const topTex=top.join('\\,')||'1',bottomTex=bottom.join('\\,');
    const rhs=sign+(bottomTex?'\\frac{'+topTex+'}{'+bottomTex+'}':topTex);
    const pTop=plainTop.join(' × ')||'1',pBottom=plainBottom.join(' × ');
    const pRhs=sign+(pBottom?'('+pTop+')/('+pBottom+')':pTop);
    const lhs='\\frac{\\mathrm{'+edge.target+'}('+gaugeIndex(ob)+')}{\\mathrm{'+edge.inputs[0]+'}('+gaugeIndex(oa)+')}';
    const pLhs=edge.target+'('+gaugeIndex(ob)+') / '+edge.inputs[0]+'('+gaugeIndex(oa)+')';
    return {tex:lhs+'='+rhs,plain:pLhs+' = '+pRhs,
      scale:[String(num),String(den)],base:[String(baseN),String(baseD)],
      start:String(t0),sourceOffset:String(oa),targetOffset:String(ob),factors};
  }catch{return null;}
}

/**
 * The archived gauge field literally uses L(t) on its left and n inside
 * the defining product. Here the dummy variable is consistently renamed u.
 * Raw source is preserved separately, unchanged.
 */
export function formatNetworkMath(edge) {
  const raw=String(edge?.expression||'');
  if(edge?.kind==='gauge'){
    const m=GAUGE.exec(raw);
    if(!m)return {plain:raw,tex:null,definition:null,parameters:[],help:'Archived gauge specification.'};
    const factor=m[4].replace(/\bn\b/g,'u');
    const definitionTex=algebraLatex(factor);
    const K=rationalLatex(m[1]),c=rationalLatex(m[2]);
    return {
      plain:'b(t)/a(t) = K × c^(t−t₀) × L(t)/L(t₀)',
      tex:'\\frac{b(t)}{a(t)}=K\\,c^{t-t_0}\\,\\frac{L(t)}{L(t_0)}',
      specialized:specializedGauge(edge,m),
      definition:{plain:'L(u) = '+friendly(factor),tex:definitionTex?'L(u)='+definitionTex:null},
      parameters:[['K (scale)',m[1]],['c (base)',m[2]],['t₀ (starting index)',m[3]],['a offset',m[5]],['b offset',m[6]]],
      help:'The expression uses the archived ratio notation b(t)/a(t). In the displayed definition of L, u is the same dummy variable called n in the original record. Index offsets are retained below.',
      valid:m[3]===String(edge.valid_from),fullTex:K&&c?
        '\\frac{b(t)}{a(t)}='+K+'\\cdot '+c+'^{t-'+m[3]+'}\\cdot \\frac{L(t)}{L('+m[3]+')}':null
    };
  }
  if(edge?.kind==='hyperedge'){
    const tex=algebraLatex(raw);
    return {plain:edge.target+'(n) = '+friendly(raw),
      tex:tex?'\\mathrm{'+edge.target+'}(n)='+tex:null,
      parameters:[],help:'Target expression in terms of the source sequences at the recorded indices.'};
  }
  if(edge?.kind==='quadratic'){
    return {plain:friendly(raw),tex:algebraLatex(raw),parameters:[],
      help:'Two directed views of one quadratic-channel identity; the archived index maps remain available below.'};
  }
  if(edge?.kind==='riordan'){
    const m=RIORDAN.exec(raw);
    return {plain:'Riordan transform of the source ordinary generating function',
      tex:null,parameters:m?[['c',m[1]],['s',m[2]],['r',m[3]],['t',m[4]]]:[],
      help:'The archive records Riordan parameters and a conditional generating-function transfer. It does not provide a display-ready full OGF equation here.'};
  }
  return {plain:raw,tex:null,parameters:[],help:'Archived expression.'};
}
