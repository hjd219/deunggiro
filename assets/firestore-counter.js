/* DG_FIRESTORE_REST_COUNTER_V7 */
(()=>{
  const PROJECT_ID="project-b08e5f3c-fa49-4ae6-933";
  const DATABASE_ID='default';
  const API_KEY="AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do";
  const DOC_PATH='counters/calculator';
  const DEBUG=new URLSearchParams(location.search).get('counterdebug')==='1';
  function status(msg){
    if(!DEBUG) return;
    let el=document.getElementById('dg-counter-debug');
    if(!el){
      el=document.createElement('div');
      el.id='dg-counter-debug';
      el.style.cssText='position:fixed;left:10px;right:10px;bottom:10px;z-index:99999;padding:10px 12px;background:#111;color:#fff;border-radius:8px;font:12px/1.45 monospace;word-break:break-all';
      document.body.appendChild(el);
    }
    el.textContent='COUNTER: '+msg;
  }
  const base='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DATABASE_ID)+'/documents/';
  const docUrl=base+DOC_PATH+'?key='+encodeURIComponent(API_KEY);
  const commitUrl='https://firestore.googleapis.com/v1/projects/'+encodeURIComponent(PROJECT_ID)+'/databases/'+encodeURIComponent(DATABASE_ID)+'/documents:commit?key='+encodeURIComponent(API_KEY);
  async function readCount(){
    const r=await fetch(docUrl,{cache:'no-store'});
    if(!r.ok) throw new Error('READ '+r.status);
    const j=await r.json(),v=j&&j.fields&&j.fields.count;
    return Number((v&&(v.integerValue??v.doubleValue))||0);
  }
  async function incrementCount(){
    const name='projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents/'+DOC_PATH;
    const body={writes:[{transform:{document:name,fieldTransforms:[{fieldPath:'count',increment:{integerValue:'1'}}]}}]};
    const r=await fetch(commitUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!r.ok) throw new Error('WRITE '+r.status);
  }
  async function render(){
    const el=document.getElementById('dg-calculator-usage');
    try{
      const n=await readCount();
      status('READ OK '+n);
      if(el){
        const num=el.querySelector('[data-count]');
        if(num) num.textContent=n.toLocaleString('ko-KR')+'회';
        el.hidden=false;
      }
    }catch(e){status(e.message);}
  }
  window.DGCounter={
    countOnce:async function(kind){
      const key='dg-counter-counted-'+String(kind||'calculator');
      try{
        status('WRITE START');
        if(sessionStorage.getItem(key)==='1'){status('ALREADY COUNTED THIS SESSION');return;}
        await incrementCount();
        sessionStorage.setItem(key,'1');
        status('WRITE OK');
        await render();
      }catch(e){status(e.message);}
    },
    refresh:render
  };
  status('V7 LOADED');
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render); else render();
})();