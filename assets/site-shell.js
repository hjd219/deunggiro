document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;
  const navItems=[['/','홈'],['/inheritance.html','상속등기'],['/renunciation.html','상속포기·한정승인'],['/corporate.html','법인등기'],['/realestate.html','부동산등기'],['/family.html','가사'],['/posts.html','법률정보']];
  const activePath=()=> current.startsWith('/posts/')?'/posts.html':current;
  const navHtml=navItems.map(([href,label])=>`<a href="${href}"${activePath()===href?' aria-current="page"':''}>${label}</a>`).join('');
  const header=`<header class="dg-shell-header"><div class="dg-shell-inner"><a class="dg-shell-logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="dg-shell-nav">${navHtml}</nav><button class="dg-shell-mobile-menu-btn" id="dg-shell-menu-btn" type="button" aria-expanded="false">☰ 메뉴</button></div></header><div class="dg-shell-mobile-panel" id="dg-shell-mobile-panel" aria-hidden="true"><div class="dg-shell-mobile-grid">${navHtml}</div><button class="dg-shell-mobile-close" id="dg-shell-menu-close" type="button">메뉴 닫기 ↑</button></div>`;
  const genericContact={title:'복잡한 등기절차, 등기로에서 확인하세요.',desc:'상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.'};
  const contactByPath={
    '/inheritance.html':{title:'일반적인 상속등기로 해결되지 않는 경우',desc:'상속인이 연락되지 않거나, 미성년자·해외 상속인이 포함된 경우처럼 일반적인 절차로 해결되지 않는 경우에는 가족관계와 현재 상황을 확인한 후 진행방법을 안내합니다.'},
    '/renunciation.html':{title:'상속채무가 복잡하거나 3개월이 지난 경우',desc:'채무 규모가 불분명하거나 후순위 상속인, 미성년자, 특별한정승인처럼 일반적인 상속포기·한정승인만으로 판단하기 어려운 경우에는 상속관계와 채무 상황을 확인한 후 진행방법을 안내합니다.'},
    '/corporate.html':{title:'법인등기 내용이 여러 가지 함께 변경되는 경우',desc:'임원변경과 본점이전, 상호·목적변경, 증자처럼 여러 등기사항이 함께 변경되거나 과밀지역 여부·주주구성에 따라 절차가 달라지는 경우에는 현재 법인상태를 확인한 후 진행방법을 안내합니다.'},
    '/realestate.html':{title:'일반적인 매매·증여등기와 다른 경우',desc:'외국인·재외국민이 포함되거나 신탁부동산, 재산분할, 근저당 설정·말소처럼 확인할 사항이 많은 경우에는 계약관계와 등기상태를 확인한 후 필요한 절차와 서류를 안내합니다.'},
    '/family.html':{title:'가족관계와 이해관계가 복잡한 경우',desc:'미성년자 친권·특별대리인, 성년후견·한정후견, 개명·가족관계등록 정정처럼 당사자 관계에 따라 절차가 달라지는 경우에는 현재 가족관계를 확인한 후 진행방법을 안내합니다.'}
  };
  const contactInfo=contactByPath[current]||genericContact;
  const contact=`<section class="dg-shell-contact" id="contact"><div class="dg-shell-contact-grid"><div class="dg-shell-contact-copy"><h2>${contactInfo.title}</h2><p>${contactInfo.desc}</p></div><a class="dg-shell-phone" href="tel:0324251500">032-425-1500 상담</a></div></section>`;
  const footer=`<footer class="dg-shell-footer"><div class="dg-shell-footer-grid"><div><div class="dg-shell-footer-brand">등기로</div><div class="dg-shell-footer-office">현재두 법무사 사무소</div><div class="dg-shell-footer-info"><div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong> <a href="tel:0324251500">032-425-1500</a></div><div><strong>이메일</strong> <a href="mailto:hjd21@naver.com">hjd21@naver.com</a></div></div><div class="dg-shell-channel-row"><a class="dg-shell-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon naver">N</span>네이버 블로그</a><span class="dg-shell-dot">·</span><a class="dg-shell-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon youtube">▶</span>유튜브</a></div></div><div class="dg-shell-route"><div class="dg-shell-route-title">찾아오시는 길</div><div class="dg-shell-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="dg-shell-route-list"><div class="dg-shell-route-item"><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="dg-shell-route-actions"><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a><a href="tel:0324251500">방문문의 032-425-1500</a></div></div></div><div class="dg-shell-legal"><span>Copyright © 2026 현재두 법무사 사무소</span><nav aria-label="법적 안내"><a href="/privacy.html">개인정보처리방침</a><span>·</span><a href="/disclaimer.html">면책고지</a></nav></div></footer>`;
  const replaceFirst=(selectors,html)=>{for(const s of selectors){const el=document.querySelector(s);if(el){el.outerHTML=html;return true}}return false};
  if(!replaceFirst(['header.header','header.dg-shell-header'],header)) document.body.insertAdjacentHTML('afterbegin',header);
  /* DG_PHONE_CTA_UNIFIED_V1 */
  document.querySelectorAll('a[href^="tel:0324251500"]').forEach(a=>{
    if(a.closest('footer,.footer,.dg-shell-footer')) return;
    const isCta=a.matches('.btn,.phone,.dg-shell-phone,.dg-shell-mobile-call,.mobile-only')||a.closest('.buttons,.contact,.dg-shell-contact,.subhero,.hero,.header,.dg-shell-header');
    if(!isCta) return;
    a.classList.add('dg-phone-cta');
    a.textContent='032-425-1500 상담';
  });

  const managedContactPaths=new Set(['/','/index.html','/posts.html','/inheritance.html','/renunciation.html','/corporate.html','/realestate.html','/family.html','/acquisition-calculator.html','/corporate-calculator.html']);
  const detailNoContactPaths=new Set(['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html']);
  if(managedContactPaths.has(current)){
    if(!replaceFirst(['section.contact','section.cta','section.dg-shell-contact'],contact)) document.body.insertAdjacentHTML('beforeend',contact);
  }else if(!detailNoContactPaths.has(current)&&!document.querySelector('section.contact,section.cta,section.dg-shell-contact')){
    document.body.insertAdjacentHTML('beforeend',contact);
  }
  if(!replaceFirst(['footer.footer','footer.dg-shell-footer'],footer)) document.body.insertAdjacentHTML('beforeend',footer);

  // 상담 설명문은 제목의 실제 표시 폭을 넘지 않도록 맞춘다.
  const syncContactCopyWidth=()=>{
    const copy=document.querySelector('.dg-shell-contact-copy');
    if(!copy) return;
    const heading=copy.querySelector('h2');
    const desc=copy.querySelector('p');
    if(!heading||!desc) return;
    desc.style.maxWidth='';
    requestAnimationFrame(()=>{
      const width=Math.ceil(heading.getBoundingClientRect().width);
      if(width>0) desc.style.maxWidth=width+'px';
    });
  };
  syncContactCopyWidth();
  let contactResizeTimer;
  window.addEventListener('resize',()=>{
    clearTimeout(contactResizeTimer);
    contactResizeTimer=setTimeout(syncContactCopyWidth,120);
  });

  /* DETAIL_TITLE_V1: 개별 상세페이지 본문 제목만 통일 */
  const detailTitles={
    '/inheritance.html':{title:'상속등기는',icon:'<svg viewBox="0 0 48 48"><path d="M12 7h18l7 7v27H12z" stroke="#258ed0" stroke-width="3" fill="none"/><path d="M30 7v8h7M18 25l4 4 9-10" stroke="#25a8df" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'},
    '/corporate.html':{title:'법인등기는',icon:'<svg viewBox="0 0 48 48"><path d="M9 41h30M13 41V20h22v21M18 20v-7h12v7" stroke="#7766d5" stroke-width="3" fill="none"/><path d="M19 27h3m5 0h3m-11 7h3m5 0h3" stroke="#9a7be0" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'},
    '/realestate.html':{title:'부동산등기는',icon:'<svg viewBox="0 0 48 48"><path d="M7 23 24 9l17 14v18H12V24" stroke="#20a38e" stroke-width="3" fill="none"/><path d="M19 41V29h10v12" stroke="#53bba9" stroke-width="3" fill="none"/></svg>'},
    '/renunciation.html':{title:'상속포기·한정승인은',icon:'<svg viewBox="0 0 48 48"><path d="M24 7 38 12v10c0 9-5.5 15.5-14 20-8.5-4.5-14-11-14-20V12z" stroke="#c89725" stroke-width="3" fill="none"/><path d="M16 22h16M24 16v12M18 22l-4 6h8zm12 0-4 6h8z" stroke="#c89725" stroke-width="2.5" fill="none"/></svg>'},
    '/family.html':{title:'가사는',icon:'<svg viewBox="0 0 48 48"><circle cx="18" cy="18" r="6" stroke="#cf679d" stroke-width="3" fill="none"/><circle cx="31" cy="19" r="5" stroke="#7b6bd0" stroke-width="3" fill="none"/><path d="M8 39c1-8 5-12 10-12s9 4 10 12M26 30c5-3 12 1 13 9" stroke="#cf679d" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'}
  };
  const detail=detailTitles[current];
  if(detail){
    const h1=document.querySelector('.subhero-copy h1,.service-hero h1,.subhero h1,.hero h1');
    if(h1&&!document.querySelector('.dg-detail-title-block')){
      const oldLabel=h1.previousElementSibling;
      if(oldLabel&&oldLabel.classList.contains('label')) oldLabel.remove();
      h1.innerHTML=`${detail.title} <span class="dg-detail-brand">등기로</span>`;
      const block=document.createElement('div');block.className='dg-detail-title-block';
      const row=document.createElement('div');row.className='dg-detail-title-row';
      const icon=document.createElement('span');icon.className='dg-detail-title-icon';icon.innerHTML=detail.icon;
      const line=document.createElement('div');line.className='dg-detail-title-line';
      h1.parentNode.insertBefore(block,h1);block.appendChild(row);row.appendChild(icon);row.appendChild(h1);block.appendChild(line);
      const style=document.createElement('style');style.id='dg-detail-title-v1';style.textContent=`
        .dg-detail-title-block{display:inline-block;max-width:100%;margin-top:4px}
        .dg-detail-title-row{display:flex;align-items:center;gap:11px;max-width:100%}
        .dg-detail-title-icon{width:46px;height:46px;flex:0 0 46px;border:1px solid #e0e6ec;border-radius:13px;background:#fff;box-shadow:0 4px 12px rgba(31,41,55,.04);padding:8px;display:grid;place-items:center}
        .dg-detail-title-icon svg{width:100%;height:100%;display:block}
        .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:clamp(34px,4.4vw,49px)!important;line-height:1.16!important;letter-spacing:-2.8px!important;margin:0!important;font-weight:900!important;white-space:nowrap!important}
        .dg-detail-brand{color:#36a9e1!important}
        .dg-detail-title-line{height:3px;width:100%;background:#82cef1;border-radius:2px;margin-top:14px}
        .dg-detail-title-block+p{margin-top:24px!important}
        @media(max-width:800px){
          .dg-detail-title-block{max-width:100%;margin-top:2px}
          .dg-detail-title-row{gap:8px}
          .dg-detail-title-icon{width:38px;height:38px;flex-basis:38px;border-radius:11px;padding:6px}
          .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:clamp(20px,6.2vw,27px)!important;letter-spacing:-1.65px!important;white-space:nowrap!important}
          .dg-detail-title-line{margin-top:11px}
          .dg-detail-title-block+p{margin-top:21px!important}
        }
        @media(max-width:360px){
          .dg-detail-title-row{gap:7px}
          .dg-detail-title-icon{width:34px;height:34px;flex-basis:34px;padding:5px}
          .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:19px!important;letter-spacing:-1.4px!important}
        }`;
      document.head.appendChild(style);
    }
  }

  /* CORPORATE_EXTRA_LOADER_V1 - 법인 전용 코드는 별도 파일에서만 실행 */
  if(current==='/corporate.html'){
    const script=document.createElement('script');
    script.src='/assets/corporate-extra.js?v=20260911-1';
    script.defer=true;
    document.head.appendChild(script);
  }

  const btn=document.getElementById('dg-shell-menu-btn'),panel=document.getElementById('dg-shell-mobile-panel'),close=document.getElementById('dg-shell-menu-close');if(btn&&panel){const setOpen=o=>{panel.classList.toggle('open',o);panel.setAttribute('aria-hidden',o?'false':'true');btn.setAttribute('aria-expanded',o?'true':'false')};btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));close?.addEventListener('click',()=>setOpen(false));panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)})}
});
