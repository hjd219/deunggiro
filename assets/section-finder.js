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
  const cleanText=el=>String(el?.textContent||'').replace(/\s+/g,'');
  const killPopover=()=>{
    document.querySelectorAll('[id*="popover"],[class*="popover"],[data-detail-popover]').forEach(el=>{
      if(!el.closest('.subhero .buttons')) el.remove();
    });
  };
  const apply=()=>{
    const controls=[...document.querySelectorAll('.subhero .buttons a,.subhero .buttons button')];
    const old=controls.find(el=>cleanText(el).includes('상속포기·한정승인세부안내')) || controls.find(el=>cleanText(el)==='관련법률정보');
    if(!old) return false;
    if(old.tagName==='A'&&old.dataset.legalInfoFixed==='1') { killPopover(); return true; }
    const fresh=document.createElement('a');
    fresh.href='/posts.html';
    fresh.className='btn btn-border';
    fresh.textContent='관련 법률정보';
    fresh.dataset.legalInfoFixed='1';
    old.replaceWith(fresh);
    killPopover();
    return true;
  };
  const style=document.createElement('style');
  style.textContent='body[data-ren-law-fixed="1"] [id*="popover"],body[data-ren-law-fixed="1"] [class*="popover"]{display:none!important;visibility:hidden!important;pointer-events:none!important}';
  document.head.appendChild(style);
  document.body.dataset.renLawFixed='1';
  apply();
  window.addEventListener('DOMContentLoaded',apply,{once:true});
  window.addEventListener('load',apply,{once:true});
  setTimeout(apply,100);
  setTimeout(apply,400);
  setTimeout(apply,1000);
  const observer=new MutationObserver(()=>{apply();killPopover();});
  observer.observe(document.documentElement,{childList:true,subtree:true});
  document.addEventListener('click',e=>{
    const el=e.target.closest('.subhero .buttons a,.subhero .buttons button');
    if(!el||cleanText(el)!=='관련법률정보') return;
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    killPopover();
    window.location.href='/posts.html';
  },true);
})();

(()=>{
  if(location.pathname!='/renunciation.html'&&location.pathname!='/renunciation') return;
  const style=document.createElement('style');
  style.textContent=`
    .ren-lower-section .ren-docs,.ren-lower-section .ren-faq-wrap{background:#fff!important;border:1px solid #a9ddf4!important;border-radius:22px!important;padding:24px!important;box-shadow:0 6px 18px rgba(31,41,55,.035)!important}
    .ren-lower-section .ren-docs>.title,.ren-lower-section .ren-faq-wrap>.title{margin:0 0 18px!important;padding:0 0 14px!important;border-bottom:1px solid #dcebf3!important;font-size:28px!important;line-height:1.3!important;letter-spacing:-1.3px!important}
    @media(max-width:800px){
      .ren-lower-section .ren-docs,.ren-lower-section .ren-faq-wrap{padding:18px!important;border-radius:18px!important}
      .ren-lower-section .ren-docs>.title,.ren-lower-section .ren-faq-wrap>.title{font-size:24px!important;margin-bottom:15px!important;padding-bottom:12px!important}
    }
  `;
  document.head.appendChild(style);
})();

(()=>{
  if(location.pathname!='/renunciation.html'&&location.pathname!='/renunciation') return;
  if(document.getElementById('ren-special-cases')) return;
  const lower=document.querySelector('.ren-lower-section');
  if(!lower) return;

  const style=document.createElement('style');
  style.id='ren-special-cases-style';
  style.textContent=`
    html body #ren-special-cases{background:#eef6fb!important;background-color:#eef6fb!important;background-image:none!important;border-top:0!important;border-bottom:0!important;box-shadow:none!important;padding:0 0 46px}
    #ren-special-cases .ren-special-title{margin:0 0 9px;font-size:30px;line-height:1.25;letter-spacing:-1px;font-weight:900;color:#14263f}
    #ren-special-cases .ren-special-desc{margin:0 0 18px;color:#52667a;font-size:14px;line-height:1.6;font-weight:700}
    #ren-special-cases .ren-special-grid{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:12px!important;align-items:stretch!important}
    #ren-special-cases .ren-special-card{box-sizing:border-box!important;width:100%!important;min-width:0!important;height:118px!important;min-height:118px!important;padding:18px 16px 16px!important;display:flex!important;flex-direction:column!important;justify-content:flex-start!important;background:#fff!important;border:1.5px solid #69b8ee!important;border-radius:14px!important;text-decoration:none!important;color:#24384f!important;transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease!important}
    #ren-special-cases .ren-special-card:hover{border-color:#36a9e1!important;transform:translateY(-2px)!important;box-shadow:0 8px 22px rgba(25,41,68,.08)!important}
    #ren-special-cases .ren-special-head{display:flex!important;align-items:center!important;gap:7px!important;min-width:0!important;white-space:nowrap!important;margin:0!important}
    #ren-special-cases .ren-special-badge{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;height:21px!important;padding:0 8px!important;border-radius:999px!important;background:#2fa6ef!important;color:#fff!important;font-size:11px!important;font-weight:800!important;line-height:21px!important;margin:0!important}
    #ren-special-cases .ren-special-name{display:block!important;margin:0!important;color:#24384f!important;font-size:15px!important;font-weight:800!important;line-height:1.35!important;letter-spacing:-.3px!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important}
    #ren-special-cases .ren-special-copy{display:block!important;margin:12px 0 0!important;color:#3f4f63!important;font-size:12px!important;font-weight:700!important;line-height:1.45!important}
    @media(max-width:1000px){#ren-special-cases .ren-special-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
    @media(max-width:700px){
      #ren-special-cases{padding-bottom:34px!important}
      #ren-special-cases .ren-special-title{font-size:24px!important;letter-spacing:-.8px!important}
      #ren-special-cases .ren-special-desc{font-size:13px!important;margin-bottom:16px!important}
      #ren-special-cases .ren-special-grid{grid-template-columns:1fr 1fr!important;gap:8px!important}
      #ren-special-cases .ren-special-card{height:108px!important;min-height:108px!important;padding:14px 12px!important;border-radius:14px!important}
      #ren-special-cases .ren-special-name{font-size:13px!important}
      #ren-special-cases .ren-special-badge{height:19px!important;padding:0 7px!important;font-size:10px!important;line-height:19px!important}
      #ren-special-cases .ren-special-copy{margin-top:9px!important;font-size:10.5px!important}
    }
  `;
  document.head.appendChild(style);

  const section=document.createElement('section');
  section.id='ren-special-cases';
  section.innerHTML=`<div class="container"><h2 class="ren-special-title">상속포기·한정승인 특수한 상황도 확인하세요</h2><p class="ren-special-desc">상속포기·한정승인 상황에 맞는 세부 안내를 바로 확인할 수 있습니다.</p><div class="ren-special-grid"><a class="ren-special-card" href="/posts/naver-224404912884.html"><div class="ren-special-head"><span class="ren-special-badge">사례</span><h3 class="ren-special-name">후순위 상속인</h3></div><p class="ren-special-copy">선순위 상속포기 후 소송으로 상속인 된 사실을 안 경우</p></a><a class="ren-special-card" href="/renunciation.html#ren-faq"><div class="ren-special-head"><span class="ren-special-badge">사례</span><h3 class="ren-special-name">특별한정승인</h3></div><p class="ren-special-copy">단순승인 후 뒤늦게 채무초과 사실을 안 경우 검토</p></a><a class="ren-special-card" href="/posts/naver-224404962663.html"><div class="ren-special-head"><span class="ren-special-badge">사례</span><h3 class="ren-special-name">해외거주 상속인</h3></div><p class="ren-special-copy">미국 등 해외 거주자가 3개월 경과 후 상속포기한 경우</p></a><a class="ren-special-card" href="/renunciation.html#ren-faq"><div class="ren-special-head"><span class="ren-special-badge">사례</span><h3 class="ren-special-name">미성년자 상속인</h3></div><p class="ren-special-copy">미성년자가 포함되어 특별대리인 선임이 필요했던 경우</p></a><a class="ren-special-card" href="/posts/naver-224405895781.html"><div class="ren-special-head"><span class="ren-special-badge">사례</span><h3 class="ren-special-name">상속재산파산</h3></div><p class="ren-special-copy">한정승인 후 부동산이 있어 상속재산파산까지 진행한 경우</p></a></div></div>`;
  lower.insertAdjacentElement('afterend',section);
})();