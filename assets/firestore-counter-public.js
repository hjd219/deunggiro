/* DG_CALCULATOR_COUNTER_V13_CLEAN */
(()=>{
  const PROJECT_ID='project-b08e5f3c-fa49-4ae6-933';
  const DATABASE_ID='default';
  const base='https://firestore.googleapis.com/v1/projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents/';
  const commitUrl='https://firestore.googleapis.com/v1/projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents:commit';
  const REFRESH_MS=15000;
  let refreshTimer=null;

  function docPath(kind){return 'counters/'+(String(kind||'calculator')==='pdf'?'pdf':'calculator')}

  async function readCount(kind){
    const r=await fetch(base+docPath(kind),{cache:'no-store'});
    if(!r.ok) throw new Error('counter read '+r.status);
    const j=await r.json();
    const v=j&&j.fields&&j.fields.count;
    return Number((v&&(v.integerValue??v.doubleValue))||0);
  }

  async function incrementCount(kind){
    const name='projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents/'+docPath(kind);
    const body={writes:[{transform:{document:name,fieldTransforms:[{fieldPath:'count',increment:{integerValue:'1'}}]}}]};
    const r=await fetch(commitUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok) throw new Error('counter write '+r.status);
  }

  async function render(){
    const el=document.getElementById('dg-calculator-usage');
    if(!el) return;
    const num=el.querySelector('[data-count]');
    try{
      const calculator=await readCount('calculator');
      let pdf=0;
      try{pdf=await readCount('pdf')}catch(e){}
      if(num) num.textContent=(calculator+pdf).toLocaleString('ko-KR')+'회';
      el.hidden=false;
    }catch(e){
      if(num&&num.textContent.trim()) el.hidden=false;
      else el.hidden=true;
    }
  }

  window.DGCounter={
    countOnce:async function(kind){
      try{
        await incrementCount(kind);
        await render();
      }catch(e){}
    },
    refresh:render
  };

  function init(){
    const el=document.getElementById('dg-calculator-usage');
    if(el) el.hidden=false;
    render();
    if(!refreshTimer&&el){
      refreshTimer=setInterval(()=>{
        if(document.visibilityState==='visible') render();
      },REFRESH_MS);
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();

  document.addEventListener('visibilitychange',()=>{
    if(document.visibilityState==='visible') render();
  });
})();
