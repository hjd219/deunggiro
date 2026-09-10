(()=>{const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');const fixedByCategory={
'상속포기·한정승인':[
 {title:'상속포기·한정승인 절차',href:'#ren-process',type:'페이지'},
 {title:'상속포기·한정승인 필요서류',href:'#ren-documents',type:'페이지'},
 {title:'상속포기·한정승인 자주 묻는 질문',href:'#ren-faq',type:'페이지'}
],
'법인등기':[
 {title:'법인등기 필요서류',href:'#documents',type:'페이지'},
 {title:'법인등기 비용계산',href:'/corporate-calculator.html',type:'계산기'},
 {title:'법인등기 자주 묻는 질문',href:'#corp-faq',type:'페이지'}
],
'부동산등기':[
 {title:'부동산등기 업무별 필요서류',href:'#realestate-guide',type:'페이지'},
 {title:'부동산등기 비용계산',href:'/acquisition-calculator.html',type:'계산기'},
 {title:'근저당 설정·말소 필요서류',href:'#mortgageSetDocs',type:'페이지'}
],
'가사':[
 {title:'가사 주요 업무',href:'#family-services',type:'페이지'},
 {title:'가사 필요서류',href:'#documents',type:'페이지'},
 {title:'가사 자주 묻는 질문',href:'#family-faq',type:'페이지'}
]
};document.querySelectorAll('.dg-section-finder').forEach(root=>{const input=root.querySelector('.dg-section-query'),toggle=root.querySelector('.dg-section-toggle'),list=root.querySelector('.dg-section-results'),search=root.querySelector('.dg-section-search-button'),status=root.querySelector('.dg-section-search-status'),category=root.dataset.category||'';if(!input||!toggle||!list||!search)return;let posts=[];const fixed=fixedByCategory[category]||[];const categories=category==='상속등기'?['상속등기','상속재산분할']:[category];const open=()=>{list.classList.add('is-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};const close=()=>{list.classList.remove('is-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};function render(query=''){const key=clean(query);const postItems=posts.map(x=>({title:x.title||'',summary:x.summary||'',keywords:x.keywords||'',href:'/posts/'+encodeURIComponent(String(x.slug).replace(/\.html$/,''))+'.html',type:'관련 글'}));const items=[...fixed,...postItems].filter(x=>!key||clean((x.title||'')+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).slice(0,18);list.innerHTML='';if(status){status.textContent=key?'검색 결과 '+items.length+'개':category+' 관련 항목 '+items.length+'개';status.classList.add('is-active')}if(!items.length){const li=document.createElement('li');li.className='dg-section-empty';li.textContent='관련 검색 결과가 없습니다.';list.appendChild(li);open();return}items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='dg-section-result-type';tag.textContent=x.type||'관련 글';a.appendChild(tag);a.appendChild(document.createTextNode(x.title||''));li.appendChild(a);list.appendChild(li)});open()}fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&categories.includes(p.category));if(document.activeElement===input||input.value)render(input.value)}).catch(()=>{});toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});input.addEventListener('focus',()=>render(input.value));input.addEventListener('click',()=>render(input.value));input.addEventListener('input',()=>render(input.value));input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});search.addEventListener('click',()=>render(input.value));document.addEventListener('click',e=>{if(!root.contains(e.target))close()})})})();

(()=>{
  if(location.pathname!='/renunciation.html'&&location.pathname!='/renunciation') return;
  const process=document.getElementById('ren-process');
  if(!process||document.getElementById('ren-aftercare')) return;

  const style=document.createElement('style');
  style.textContent=`
    #ren-aftercare{background:var(--detail-sky,#eef8fd);padding:0 0 44px}
    #ren-aftercare .ren-aftercare-card{background:#fff;border:1px solid #a9ddf4;border-radius:22px;padding:24px;box-shadow:0 6px 18px rgba(31,41,55,.035)}
    #ren-aftercare .ren-aftercare-title{font-size:18px;font-weight:900;letter-spacing:-.6px;margin:0 0 14px;color:#132f4c}
    #ren-aftercare .ren-aftercare-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
    #ren-aftercare .ren-aftercare-box{border:1px solid #d3e8f3;border-radius:15px;background:#fbfdff;padding:18px}
    #ren-aftercare .ren-aftercare-box h3{display:inline-flex;align-items:center;min-height:34px;margin:0 0 12px;padding:0 12px;border:1px solid #a9ddf4;border-radius:8px;background:#eefaff;color:#168dca;font-size:14px;font-weight:900;letter-spacing:-.4px}
    #ren-aftercare .ren-aftercare-box p{margin:0;color:#324b61;font-size:14px;line-height:1.75}
    #ren-aftercare .ren-aftercare-key{margin-top:11px;padding:10px 12px;border-radius:10px;background:#eef7fc;color:#2b455b;font-size:13px;line-height:1.6}
    #ren-aftercare .ren-aftercare-key strong{color:#168dca}
    @media(max-width:800px){
      #ren-aftercare{padding-bottom:30px}
      #ren-aftercare .ren-aftercare-card{padding:18px;border-radius:18px}
      #ren-aftercare .ren-aftercare-grid{grid-template-columns:1fr}
      #ren-aftercare .ren-aftercare-title{font-size:17px}
      #ren-aftercare .ren-aftercare-box{padding:16px}
    }
  `;
  document.head.appendChild(style);

  const section=document.createElement('section');
  section.id='ren-aftercare';
  section.innerHTML=`<div class="container"><div class="ren-aftercare-card"><div class="ren-aftercare-title">심판 후에는 상속포기와 한정승인의 후속절차가 다릅니다.</div><div class="ren-aftercare-grid"><div class="ren-aftercare-box"><h3>상속포기 후속절차</h3><p>후순위 상속인에게 상속포기 사실을 알리고, 필요한 경우 상속포기 심판문을 제공합니다. 상속채권자는 상속포기 사실을 모른 상태에서 소송을 제기할 수 있으므로, 소장을 받은 경우 답변서 제출이 필요합니다.</p><div class="ren-aftercare-key"><strong>핵심</strong> 후순위 상속인 통지 · 심판문 제공 · 소송 제기 시 답변서 제출</div></div><div class="ren-aftercare-box"><h3>한정승인 후속절차</h3><p>장례비·화장비용 등 상속비용이 적극재산을 초과하는 경우에는 별도 청산절차가 필요하지 않을 수 있으나, 채권자에게 내용증명 등으로 한정승인 사실을 통지합니다. 반대로 적극재산이 상속비용보다 많다면 별도 청산절차를 진행합니다.</p><div class="ren-aftercare-key"><strong>청산방법</strong> 적극재산이 현금성 재산만 있는 경우 임의청산을 검토하고, 부동산 등 환가가 어려운 재산이 있는 경우에는 법원에서 진행하는 상속재산파산을 검토합니다.</div></div></div></div></div>`;
  process.insertAdjacentElement('afterend',section);
})();

(()=>{
  if(location.pathname!='/renunciation.html'&&location.pathname!='/renunciation') return;
  const apply=()=>{
    const buttons=[...document.querySelectorAll('.subhero .buttons a')];
    const target=buttons.find(a=>a.textContent.replace(/\s+/g,'').includes('상속포기·한정승인세부안내')) || buttons.find(a=>a.textContent.replace(/\s+/g,'')==='관련법률정보');
    if(!target) return false;
    target.href='/posts.html';
    target.textContent='관련 법률정보';
    target.className='btn btn-border';
    target.removeAttribute('id');
    target.removeAttribute('aria-haspopup');
    target.removeAttribute('aria-expanded');
    return true;
  };
  apply();
  window.addEventListener('load',apply,{once:true});
  setTimeout(apply,700);
})();

(()=>{
  if(location.pathname!='/renunciation.html'&&location.pathname!='/renunciation') return;
  const style=document.createElement('style');
  style.textContent=`
    .ren-lower-section .ren-docs,.ren-lower-section .ren-faq-wrap{background:#fff;border:1px solid #a9ddf4;border-radius:22px;padding:24px;box-shadow:0 6px 18px rgba(31,41,55,.035)}
    .ren-lower-section .ren-docs>.title,.ren-lower-section .ren-faq-wrap>.title{margin:0 0 18px;padding-bottom:14px;border-bottom:1px solid #dcebf3;font-size:28px;line-height:1.3;letter-spacing:-1.3px}
    @media(max-width:800px){
      .ren-lower-section .ren-docs,.ren-lower-section .ren-faq-wrap{padding:18px;border-radius:18px}
      .ren-lower-section .ren-docs>.title,.ren-lower-section .ren-faq-wrap>.title{font-size:24px;margin-bottom:15px;padding-bottom:12px}
    }
  `;
  document.head.appendChild(style);
})();