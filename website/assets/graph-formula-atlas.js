/* Author: Komorebi P. Exact residue evaluation and local catalogue search. */
(function(){
  'use strict';
  const gcd=(a,b)=>{a=a<0n?-a:a;while(b){let t=a%b;a=b;b=t;}return a;};
  function choose(n,k){let v=1n;for(let j=1;j<=k;j++)v=v*BigInt(n-k+j)/BigInt(j);return v;}
  function value(model,n){
    if(!Number.isSafeInteger(n)||n<0||n>10000)throw Error('Enter an integer vertex count from 0 to 10000.');
    let num=BigInt(model.s[n]??'0'),den=1n;
    for(const {d,e,h,c} of model.lanes){
      const q=Math.floor(n/d),r=n%d;let sum=0n;
      for(let j=0;j<=Math.min(q,e-1);j++)sum+=BigInt(c[r+d*j]??'0')*choose(q-j+e-1,e-1);
      const scale=BigInt(h);num=num*scale+sum*den;den*=scale;const g=gcd(num,den);num/=g;den/=g;
    }
    if(den!==1n||num<0n)throw Error('The retained coefficient data did not give a nonnegative integer.');
    return num.toString();
  }
  if(typeof module!=='undefined'&&module.exports){module.exports={value};}
  if(typeof document==='undefined')return;
  const $=id=>document.getElementById(id);
  for(const form of document.querySelectorAll('.gfa-eval')){
    form.hidden=false;
    form.addEventListener('submit',event=>{
      event.preventDefault();const output=form.querySelector('output');const input=form.querySelector('input');
      try{
        if(!input.value.trim())throw Error('Enter an integer index.');
        const n=Number(input.value);
        let result;
        if(form.dataset.arrayModel){
          if(!window.graphArrayEngine)throw Error('The array evaluator is unavailable. Reload the page.');
          result=window.graphArrayEngine.value(JSON.parse(form.dataset.arrayModel),n);
        }else if(form.dataset.supplementId){
          if(!window.graphSupplementEngine)throw Error('The graph evaluator is unavailable. Reload the page.');
          result=window.graphSupplementEngine.value(form.dataset.supplementId,n);
        }else{result=value(JSON.parse(form.dataset.model),n)}
        output.textContent='a('+input.value+') = '+result;
      }
      catch(error){output.textContent=error.message;}
    });
  }
  const form=$('gfa-search');
  if(form){
    const records=[...document.querySelectorAll('[data-gfa-record]')],size=24;let page=0;
    const query=$('gfa-query'),family=$('gfa-family'),bound=$('gfa-bound'),status=$('gfa-status');
    const params=new URLSearchParams(location.search);query.value=params.get('q')||'';
    if([...family.options].some(o=>o.value===params.get('family')))family.value=params.get('family');
    if([...bound.options].some(o=>o.value===params.get('bound')))bound.value=params.get('bound');
    function update(){
      const words=query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      const match=records.filter(r=>(!family.value||family.value===r.dataset.family)&&(!bound.value||bound.value===r.dataset.oeis)&&words.every(w=>r.dataset.search.includes(w)));
      const pages=Math.max(1,Math.ceil(match.length/size));page=Math.min(page,pages-1);const shown=new Set(match.slice(page*size,(page+1)*size));records.forEach(r=>r.hidden=!shown.has(r));
      status.textContent=match.length?match.length+' matching records · '+(page*size+1)+'–'+Math.min((page+1)*size,match.length)+' shown':'No matches. Try an OEIS ID, another family, or a shorter query.';
      $('gfa-page').textContent='Page '+(page+1)+' of '+pages;$('gfa-prev').disabled=page===0;$('gfa-next').disabled=page+1===pages;$('gfa-pagination').hidden=pages===1;
    }
    form.hidden=false;form.addEventListener('submit',e=>{e.preventDefault();page=0;update();});form.addEventListener('input',()=>{page=0;update();});form.addEventListener('reset',()=>{setTimeout(()=>{page=0;update();},0);});
    $('gfa-prev').addEventListener('click',()=>{page--;update();status.scrollIntoView({block:'nearest'});});$('gfa-next').addEventListener('click',()=>{page++;update();status.scrollIntoView({block:'nearest'});});update();
  }
  function reveal(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const target=$(id);if(target?.matches('details.gfa-record')){target.open=true;target.scrollIntoView({block:'start'});}}
  window.addEventListener('hashchange',reveal);reveal();
})();
