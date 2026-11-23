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
