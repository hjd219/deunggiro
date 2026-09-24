/* DG_CALCULATOR_COUNTER_V14_LIVE_ONLY */
(()=>{
  const PROJECT_ID='project-b08e5f3c-fa49-4ae6-933';
  const DATABASE_ID='default';
  const API_KEY='AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do';
  const base='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DATABASE_ID)+'/documents/';
  const commitUrl='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DATABASE_ID)+'/documents:commit?key='+encodeURIComponent(API_KEY);
  const REFRESH_MS=15000;
  const DEBUG=new URLSearchParams(location.search).get('counterdebug')==='1';
  function report(msg){console.error('[DGCounter]',msg);if(!DEBUG)return;let el=document.getElementById('dg-counter-debug');if(!el){el=document.createElement('div');el.id='dg-counter-debug';el.style.cssText='position:fixed;left:10px;right:10px;bottom:10px;z-index:99999;padding:10px 12px;background:#111;color:#fff;border-radius:8px;font:12px/1.45 monospace;word-break:break-all';document.body.appendChild(el)}el.textContent='COUNTER: '+msg}
  let refreshTimer=null;

  function docPath(kind){return 'counters/'+(String(kind||'calculator')==='pdf'?'pdf':'calculator')}

  async function readCount(kind){
    const r=await fetch(base+docPath(kind)+'?key='+encodeURIComponent(API_KEY),{cache:'no-store'});
    if(!r.ok){const t=await r.text();throw new Error('READ '+r.status+' '+t.slice(0,240))}
    const j=await r.json();
    const v=j&&j.fields&&j.fields.count;
    return Number((v&&(v.integerValue??v.doubleValue))||0);
  }

  async function incrementCount(kind){
    const name='projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents/'+docPath(kind);
    const body={writes:[{transform:{document:name,fieldTransforms:[{fieldPath:'count',increment:{integerValue:'1'}}]}}]};
    const r=await fetch(commitUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok){const t=await r.text();throw new Error('WRITE '+r.status+' '+t.slice(0,240))}
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
      el.hidden=true;
    }
  }

  window.DGCounter={
    countOnce:async function(kind){
      try{
        await incrementCount(kind);
        await render();
      }catch(e){report(e.message||String(e))}
    },
    refresh:render
  };

  function init(){
    const el=document.getElementById('dg-calculator-usage');
    if(el) el.hidden=true;
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
