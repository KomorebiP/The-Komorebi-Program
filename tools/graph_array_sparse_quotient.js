/* Author: Komorebi P. Exact mask-restricted sparse row-history transitions. */
'use strict';
function compressSparse(model,options={}){
  const check=(ok,msg)=>{if(!ok)throw Error(msg)};
  const w=Number(model.w[1]),b=model.kind==="B"?model.parameters[0]:2,L=model.kind==="B"?2:model.kind==="A"?model.patterns[0].length:model.parameters[0];
  const maxRows=options.maxRows??4096,maxStates=options.maxStates??50000,maxEdges=options.maxEdges??1500000;
  if(b**w>maxRows)return {status:"row budget",width:w};
  const maskAll=(1<<w)-1,allow=(bits)=>model.kind==="A"?!model.patterns.includes(bits.join("")):bits.reduce((a,b)=>a+b,0)<=model.parameters[1];
  const rows=[],rowCodes=[];
  for(let i=0;i<b**w;i++){
    const a=Array(w);let t=i;for(let j=w-1;j>=0;j--){a[j]=t%b;t=Math.floor(t/b)}
    if(model.kind==="B"||Array.from({length:Math.max(0,w-L+1)},(_,k)=>k).every(k=>allow(a.slice(k,k+L)))){rows.push(a);rowCodes.push(i)}
  }
  const R=rows.length,N=R**(L-1),period=R**(L-2);
  if(N>maxStates)return {raw:N,status:"state budget",width:w};
  const flags=model.kind==="B"?null:Array.from({length:2**(L-1)},(_,h)=>{
    const a=Array.from({length:L-1},(_,i)=>(h>>(L-2-i))&1);
    return (allow([...a,0])?1:0)|(allow([...a,1])?2:0)
  });
  const cached=new Map(),edges=Array(N);let total=0;
  for(let s=0;s<N;s++){
    const history=Array(L-1);let t=s;for(let k=L-2;k>=0;k--){history[k]=rows[t%R];t=Math.floor(t/R)}
    let candidates;
    if(model.kind==="B"){
      candidates=[];
      for(let j=0;j<R;j++){const a=history[0],v=rows[j];let ok=true;for(let c=0;c<w-1;c++)if(a[c]+a[c+1]+v[c]+v[c+1]<model.parameters[1]){ok=false;break}if(ok)candidates.push(j)}
    }else{
      let one=0,zero=0;
      for(let c=0;c<w;c++){
        let h=0;for(let k=0;k<L-1;k++)h=(h<<1)|history[k][c];
        const f=flags[h],bit=1<<(w-1-c);if(!(f&1))one|=bit;if(!(f&2))zero|=bit;
        if(model.diagonal===1&&c>=L-1){h=0;for(let k=0;k<L-1;k++)h=(h<<1)|history[k][c-(L-1)+k];const g=flags[h];if(!(g&1))one|=bit;if(!(g&2))zero|=bit}
      }
      if(one&zero)candidates=[];
      else{
        const key=(one<<w)|zero;
        if(cached.has(key))candidates=cached.get(key);
        else{candidates=[];for(let j=0;j<R;j++)if((rowCodes[j]&one)===one&&!(rowCodes[j]&zero))candidates.push(j);cached.set(key,candidates)}
      }
    }
    total+=candidates.length;if(total>maxEdges)return {raw:N,status:"edge budget",width:w,edgeLowerBound:total};
    edges[s]=Int32Array.from(candidates,j=>(s%period)*R+j)
  }
  let cls=new Int32Array(N),K=1,rounds=0;
  function count(s,labels){const a=new Map();for(const t of edges[s])a.set(labels[t],(a.get(labels[t])||0)+1);return [...a].sort((a,b)=>a[0]-b[0])}
  while(true){const sig=new Map(),next=new Int32Array(N);for(let s=0;s<N;s++){const key=cls[s]+"|"+count(s,cls).map(x=>x.join(":")).join(",");if(!sig.has(key))sig.set(key,sig.size);next[s]=sig.get(key)}cls=next;rounds++;if(sig.size===K)break;K=sig.size}
  const weights=Array(K).fill(0),quotient=Array(K);
  for(let s=0;s<N;s++){weights[cls[s]]++;const row=count(s,cls);if(!quotient[cls[s]])quotient[cls[s]]=row;else check(JSON.stringify(quotient[cls[s]])===JSON.stringify(row),"non-equitable partition")}
  return {raw:N,states:K,edges:quotient.reduce((a,b)=>a+b.length,0),rawEdges:total,rounds,weights,quotient,width:w}
}
module.exports={compressSparse};
