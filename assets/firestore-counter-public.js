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

/* CALCULATOR_PAGE_ACCOUNT_SINGLE_V2
   계산기 화면: 고객 준비서류는 숨기고 입금계좌는 PDF 버튼 바로 위에 1개만 표시 */
(()=>{
  const paths=['/acquisition-calculator.html','/corporate-calculator.html'];
  if(!paths.includes(location.pathname)) return;

  const style=document.createElement('style');
  style.id='dg-calculator-account-single-v2';
  style.textContent=`
    @media screen{
      .result .documents{display:none!important}
      .result .dg-calc-account-single{display:block!important;margin-top:14px!important;padding:15px 16px!important;border:1px solid #91adbf!important;border-radius:12px!important;background:#f2faff!important}
      .result .dg-calc-account-head{display:flex!important;align-items:center!important;gap:8px!important;margin-bottom:10px!important}
      .result .dg-calc-account-head strong{padding:4px 9px!important;border:1px solid #b9e0f2!important;border-radius:8px!important;background:#eaf7fd!important;color:#168dca!important;font-size:12px!important;font-weight:900!important}
      .result .dg-calc-account-head span{color:#607286!important;font-size:11px!important;font-weight:750!important}
      .result .dg-calc-account-list{display:grid!important;grid-template-columns:1fr 1fr!important;gap:9px!important}
      .result .dg-calc-account-row{padding:10px 12px!important;border:1px solid #cfe4ef!important;border-radius:9px!important;background:#fff!important;min-width:0!important}
      .result .dg-calc-account-bank{display:block!important;margin-bottom:3px!important;color:#168dca!important;font-size:11px!important;font-weight:900!important}
      .result .dg-calc-account-number{display:block!important;color:#0b2137!important;font-size:14px!important;font-weight:900!important;white-space:nowrap!important}
      .result .dg-calc-account-holder{display:block!important;margin-top:2px!important;color:#607286!important;font-size:10.5px!important;font-weight:750!important}
      @media(max-width:520px){.result .dg-calc-account-list{grid-template-columns:1fr!important}}
    }
    @media print{.result .dg-calc-account-single{display:none!important}}
  `;
  document.head.appendChild(style);

  const nums=['110-482-692656','3333-07-6560416'];
  const html=`<div class="dg-calc-account-single"><div class="dg-calc-account-head"><strong>입금계좌</strong><span>현재두 법무사 사무소</span></div><div class="dg-calc-account-list"><div class="dg-calc-account-row"><span class="dg-calc-account-bank">신한은행</span><span class="dg-calc-account-number">110-482-692656</span><span class="dg-calc-account-holder">현재두법무사사무소</span></div><div class="dg-calc-account-row"><span class="dg-calc-account-bank">카카오뱅크</span><span class="dg-calc-account-number">3333-07-6560416</span><span class="dg-calc-account-holder">현재두법무사사무소</span></div></div></div>`;

  function clean(){
    const result=document.querySelector('.result');
    if(!result) return;
    const pdf=result.querySelector('.pdf-download');
    if(!pdf) return;

    result.querySelectorAll('.account-box,.bank-account,.account-info,.deposit-account,.dg-estimate-account').forEach(el=>el.remove());
    Array.from(result.children).forEach(el=>{
      if(el.classList?.contains('dg-calc-account-single')) return;
      if(el.classList?.contains('print-columns')||el.classList?.contains('documents')||el.classList?.contains('print-footer')||el.classList?.contains('pdf-download')||el.classList?.contains('consult')) return;
      const t=(el.textContent||'').replace(/\s/g,'');
      if(nums.every(n=>t.includes(n))) el.remove();
    });

    let single=result.querySelector('.dg-calc-account-single');
    if(!single){
      pdf.insertAdjacentHTML('beforebegin',html);
      single=result.querySelector('.dg-calc-account-single');
    }else if(single.nextElementSibling!==pdf){
      pdf.insertAdjacentElement('beforebegin',single);
    }
  }

  const run=()=>requestAnimationFrame(clean);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
  new MutationObserver(run).observe(document.documentElement,{subtree:true,childList:true});
})();