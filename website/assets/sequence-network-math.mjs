/** Strict display-only OEIS formula reader. Never evaluates mathematical text.
 * If tokenization or syntax is ambiguous, return null and preserve exact source.
 * Generated TeX contains only fixed control sequences and validated tokens.
 */
const ID = /^A\d{6}$/;
const IDENT = /^(?:[a-zA-Z]|phi|Phi|pi|Pi|Gamma|Theta|theta|omega|Omega)$/;
const FUNCTIONS = new Set(['binom','binomial','sqrt','exp','log','sin','cos','tan','sec','sinh','cosh','tanh','abs','floor','ceil','round']);
const SYMBOL = Object.freeze({phi:'\\phi',Phi:'\\Phi',pi:'\\pi',Pi:'\\pi',Gamma:'\\Gamma',Theta:'\\Theta',theta:'\\theta',omega:'\\omega',Omega:'\\Omega'});
const prec = Object.freeze({eq:0,add:1,mul:2,pow:3,atom:4});

function tokenize(text){
  if(typeof text!=='string'||text.length>420||/[\\<>\u0000-\u0008]/.test(text))return null;
  const result=[];let at=0;
  while(at<text.length){
    if(/\s/.test(text[at])){at++;continue;}
    const m=/^(?:A\d{6}|\d+(?:\.\d+)?|[A-Za-z]+|>=|<=|!=|[+\-*/^(),=!])/.exec(text.slice(at));
    if(!m || result.length>180)return null;
    result.push(m[0]);at+=m[0].length;
  }
  return result;
}

/** Parse a bounded, unambiguous arithmetic subset of OEIS formulas. */
export function exactFormulaLatex(source){
  if(typeof source!=='string')return null;
  let input=source.trim();if(input.endsWith('.'))input=input.slice(0,-1);
  let prefix='';
  if(/^G\.f\.:?\s*/i.test(input)){input=input.replace(/^G\.f\.:?\s*/i,'');prefix='\\text{OGF: }\\quad ';}
  else if(/^E\.g\.f\.:?\s*/i.test(input)){input=input.replace(/^E\.g\.f\.:?\s*/i,'');prefix='\\text{EGF: }\\quad ';}
  const tokens=tokenize(input);
  if(!tokens?.length)return null;
  try{
    let at=0, depth=0;
    const peek=()=>tokens[at], take=()=>tokens[at++];
    function group(){
      if(take()!=='('||++depth>24)throw Error('group');
      const values=[];
      if(peek()!==')')while(true){
        values.push(equality());
        if(peek()!==',')break;take();
      }
      if(take()!==')')throw Error('close');
      depth--;
      return values;
    }
    const render=(term,context=-1)=>term.p<context?'\\left('+term.s+'\\right)':term.s;
    function atom(){
      const t=take();
      if(t===undefined)throw Error('end');
      if(t==='('){at--;const args=group();if(args.length!==1)throw Error('tuple');return {s:'\\left('+args[0].s+'\\right)',p:prec.atom};}
      if(/^\d+(?:\.\d+)?$/.test(t))return {s:t,p:prec.atom};
      if(!ID.test(t)&&!IDENT.test(t)&&!FUNCTIONS.has(t))throw Error('identifier');
      let name=ID.test(t)?'\\mathrm{'+t+'}':SYMBOL[t]||t;
      if(peek()==='('){const args=group();
        if((t==='binomial'||t==='binom')&&args.length===2)return {s:'\\binom{'+args[0].s+'}{'+args[1].s+'}',p:prec.atom};
        if(t==='sqrt'&&args.length===1)return {s:'\\sqrt{'+args[0].s+'}',p:prec.atom};
        if(t==='abs'&&args.length===1)return {s:'\\left|'+args[0].s+'\\right|',p:prec.atom};
        if(t==='floor'&&args.length===1)return {s:'\\lfloor '+args[0].s+'\\rfloor',p:prec.atom};
        if(t==='ceil'&&args.length===1)return {s:'\\lceil '+args[0].s+'\\rceil',p:prec.atom};
        if(FUNCTIONS.has(t)&&!['binom','binomial','sqrt','abs','floor','ceil'].includes(t)){
          if(args.length!==1)throw Error('arity');name=t==='round'?'\\operatorname{round}':'\\'+t;
        }
        else if(args.length!==1)throw Error('arity');
        return {s:name+'\\!\\left('+args.map(x=>x.s).join(',\\;')+'\\right)',p:prec.atom};
      }
      if(FUNCTIONS.has(t))throw Error('bare function');
      return {s:name,p:prec.atom};
    }
    function power(){let lhs=atom();while(peek()==='!'){take();lhs={s:render(lhs,prec.atom)+'!',p:prec.atom};}
      if(peek()==='^'){take();const rhs=unary();lhs={s:render(lhs,prec.atom)+'^{'+rhs.s+'}',p:prec.pow};}return lhs;}
    function unary(){if(peek()==='-'||peek()==='+'){const op=take(),v=unary();return {s:op+render(v,prec.pow),p:prec.pow};}return power();}
    function multiply(){let lhs=unary();while(['*','/'].includes(peek())){
      const op=take(),rhs=unary();
      lhs={s:op==='/'?'\\frac{'+lhs.s+'}{'+rhs.s+'}':render(lhs,prec.mul)+'\\cdot '+render(rhs,prec.mul),p:prec.mul};
    }return lhs;}
    function addition(){let lhs=multiply();while(['+','-'].includes(peek())){
      const op=take(),rhs=multiply();lhs={s:render(lhs,prec.add)+' '+op+' '+render(rhs,prec.add+(op==='-'?1:0)),p:prec.add};
    }return lhs;}
    function equality(){let lhs=addition();while(['=','>=','<=','!='].includes(peek())){
      const op=take(),rhs=addition(),operation={'=':'=', '>=':'\\ge', '<=':'\\le', '!=':'\\ne'}[op];
      lhs={s:lhs.s+' '+operation+' '+rhs.s,p:prec.eq};
    }return lhs;}
    const parsed=equality();if(at!==tokens.length)return null;
    return prefix+parsed.s;
  }catch{return null;}
}

/** Produce mathematical notation only from strictly verified template syntax. */
export function transferFormulaLatex(edge){
  if(!edge || typeof edge.expression!=='string'||!ID.test(edge.target)||!Array.isArray(edge.inputs)||edge.inputs.some(id=>!ID.test(id)))return null;
  if(edge.kind==='hyperedge'){
    const rhs=exactFormulaLatex(edge.expression);
    return rhs?'\\mathrm{'+edge.target+'}\\!\\left(n\\right) = '+rhs:null;
  }
  if(edge.kind==='quadratic')return exactFormulaLatex(edge.expression);
  if(edge.kind==='gauge'){
    const m=/^b\(t\)\/a\(t\) = K\*c\^\(t-t0\)\*L\(t\)\/L\(t0\); K=(-?\d+), c=(-?\d+), t0=(\d+), L\(t\)=/.exec(edge.expression);
    if(!m)return null;
    return `\\frac{b(t)}{a(t)} = ${m[1]}\\cdot ${m[2]}^{t-${m[3]}}\\cdot\\frac{L(t)}{L(${m[3]})}`;
  }
  if(edge.kind==='riordan'){
    const m=/^R\[c=(-?\d+),s=(-?\d+),r=(-?\d+),t=(-?\d+)\] OGF transform$/.exec(edge.expression);
    if(!m)return null;
    return `\\mathrm{OGF}\\!\\left(\\mathrm{${edge.inputs[0]}}\\right)\\;\\xrightarrow{\\mathcal{R}_{${m[1]},${m[2]},${m[3]},${m[4]}}}\\;\\mathrm{OGF}\\!\\left(\\mathrm{${edge.target}}\\right)`;
  }
  return null;
}

/** Conservative extraction of source-field mathematical fragments. */
export function sourceFormulaLatex(text){
  if(typeof text!=='string'||text.length>420||/https?:|\b(?:where|if and only if|conjectur|corrected|by _|see |asymptotic)\b/i.test(text))return null;
  return exactFormulaLatex(text);
}
