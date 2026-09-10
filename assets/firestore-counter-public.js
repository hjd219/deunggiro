/* DG_CALCULATOR_COUNTER_V4 */
(()=>{
  const PROJECT_ID='project-b08e5f3c-fa49-4ae6-933';
  const DATABASE_ID='default';
  const base='https://firestore.googleapis.com/v1/projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents/';
  const commitUrl='https://firestore.googleapis.com/v1/projects/'+PROJECT_ID+'/databases/'+DATABASE_ID+'/documents:commit';

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
    try{
      const n=await readCount('calculator');
      const num=el.querySelector('[data-count]');
      if(num) num.textContent=n.toLocaleString('ko-KR')+'회';
      el.hidden=false;
    }catch(e){}
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

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render);
  else render();
})();
