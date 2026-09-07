/* DG_FIRESTORE_COUNTER_V1 */
(()=>{
  const PROJECT_ID='project-b08e5f3c-fa49-4ae6-933';
  const DB='(default)';
  const DOC='counters/calculator';
  const BASE='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DB)+'/documents/';
  const docUrl=BASE+DOC;

  async function readCount(){
    const r=await fetch(docUrl,{cache:'no-store'});
    if(!r.ok) throw new Error('counter read '+r.status);
    const j=await r.json();
    const v=j&&j.fields&&j.fields.count;
    return Number((v&&(v.integerValue??v.doubleValue))||0);
  }

  async function increment(){
    const url='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DB)+'/documents:commit';
    const name='projects/'+PROJECT_ID+'/databases/'+DB+'/documents/'+DOC;
    const body={writes:[{transform:{document:name,fieldTransforms:[{fieldPath:'count',increment:{integerValue:'1'}}]}}]};
    const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok) throw new Error('counter write '+r.status);
    return true;
  }

  async function render(){
    const el=document.getElementById('dg-calculator-usage');
    if(!el) return;
    try{
      const n=await readCount();
      const num=el.querySelector('[data-count]');
      if(num) num.textContent=n.toLocaleString('ko-KR')+'회';
      el.hidden=false;
    }catch(e){ /* fail closed: hide public counter */ }
  }

  window.DGCounter={
    countOnce:async function(kind){
      const key='dg-counter-counted-'+String(kind||'calculator');
      try{
        if(sessionStorage.getItem(key)==='1') return;
        await increment();
        sessionStorage.setItem(key,'1');
      }catch(e){ /* calculator must still work even if counter is unavailable */ }
    },
    refresh:render
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render);
  else render();
})();