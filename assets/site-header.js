/* SITE_HEADER_V7 - 공통 헤더 + 모바일 세로형 전체메뉴 + 계산기 헤더 통일 */
(function(){
  const current=location.pathname;
  const activePath=current.startsWith('/posts/')?'/posts.html':current;
  const isCalculator=current==='/acquisition-calculator.html'||current==='/corporate-calculator.html';

  if(isCalculator){
    const style=document.createElement('style');
    style.id='dg-calculator-type-text-v2';
    style.textContent='.opts .opt,.types .type,.type-tabs button,.calc-tabs button{font-size:16px!important;line-height:1.25!important;font-weight:850!important}@media(max-width:800px){.opts .opt,.types .type,.type-tabs button,.calc-tabs button{font-size:16px!important}}';
    document.head.appendChild(style);

    const oldHeader=document.querySelector('body>header.header');
    if(oldHeader && !document.querySelector('header.dg-shell-header')){
      const shell=document.createElement('header');
      shell.className='dg-shell-header';
      shell.innerHTML=`<div class="dg-shell-inner"><a class="dg-shell-logo" href="/">등기로<small>현재두 법무사 사무소</small></a><nav class="dg-shell-nav" aria-label="주요 메뉴"><a href="/">홈</a><a href="/inheritance.html">상속등기</a><a href="/renunciation.html">상속포기·한정승인</a><a href="/corporate.html">법인등기</a><a href="/realestate.html">부동산등기</a><a href="/family.html">가사</a><a href="/posts.html">법률정보</a></nav><button class="dg-shell-mobile-menu-btn" id="dg-shell-menu-btn" type="button" aria-expanded="false">☰ 메뉴</button></div><div class="dg-shell-mobile-panel" id="dg-shell-mobile-panel" aria-hidden="true"></div>`;
      oldHeader.replaceWith(shell);
    }
  }

  const header=document.querySelector('header.dg-shell-header');
  if(!header) return;

  if(!document.querySelector('link[data-dg-mobile-menu]')){
    const link=document.createElement('link');
    link.rel='stylesheet';
    link.href='/assets/mobile-menu.css?v=20260913-right70';
    link.dataset.dgMobileMenu='1';
    document.head.appendChild(link);
  }

  header.querySelectorAll('nav a').forEach(a=>{
    let path;
    try{path=new URL(a.href,location.origin).pathname}catch(_){return}
    if(path===activePath||(activePath==='/'&&(path==='/'||path==='/index.html')))a.setAttribute('aria-current','page');
    else a.removeAttribute('aria-current');
  });

  const btn=document.getElementById('dg-shell-menu-btn');
  const panel=document.getElementById('dg-shell-mobile-panel');
  if(!btn||!panel)return;

  const icons={
    home:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>',
    inherit:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l3 3v15H6z"/><path d="M15 3v4h4"/><path d="M9 11h6M9 15h4"/></svg>',
    renounce:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 5.5 5.5v5.8c0 4.1 2.7 7.5 6.5 9.7 3.8-2.2 6.5-5.6 6.5-9.7V5.5z"/><path d="m9 12 2 2 4-4"/></svg>',
    corp:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h16"/><path d="M6 20V5h12v15"/><path d="M9 8h2M13 8h2M9 12h2M13 12h2M9 16h2M13 16h2"/></svg>',
    real:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 20V7h6v13"/><path d="M11 20V4h8v16"/><path d="M7.5 10h1M7.5 13h1M7.5 16h1M14 7h2M14 10h2M14 13h2M14 16h2"/><path d="M3 20h18"/></svg>',
    family:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="9" r="3"/><circle cx="16.5" cy="10.5" r="2.5"/><path d="M3.5 20c.4-4 2.3-6 5.5-6s5.1 2 5.5 6"/><path d="M14 15.5c3.1-.6 5.4 1 6 4.5"/></svg>',
    info:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h11l2 2v14H6z"/><path d="M17 4v3h3"/><path d="M9 10h6M9 14h6M9 18h4"/></svg>'
  };
  const items=[
    {kind:'home',label:'홈',desc:'등기로 메인으로 이동',href:'/',active:activePath==='/'||activePath==='/index.html'},
    {kind:'inherit',label:'상속등기',desc:'단독상속 · 공동상속 · 유증',href:'/inheritance.html',active:activePath==='/inheritance.html'},
    {kind:'renounce',label:'상속포기·한정승인',desc:'기한 · 절차 · 필요서류 · 청산',href:'/renunciation.html',active:activePath==='/renunciation.html'},
    {kind:'corp',label:'법인등기',desc:'설립 · 변경 · 증자 · 회사계속',href:'/corporate.html',active:activePath==='/corporate.html'},
    {kind:'real',label:'부동산등기',desc:'매매 · 증여 · 재산분할 · 담보',href:'/realestate.html',active:activePath==='/realestate.html'},
    {kind:'family',label:'가사',desc:'이혼 · 후견 · 개명 · 친생자관계',href:'/family.html',active:activePath==='/family.html'},
    {kind:'info',label:'법률정보',desc:'최신정보 · 판례 · 실무가이드',href:'/posts.html',active:activePath==='/posts.html'}
  ];

  panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');panel.setAttribute('aria-label','메뉴');
  panel.innerHTML=`<div class="dg-mm-top"><span class="dg-mm-brand">메뉴</span><button class="dg-mm-close" id="dg-shell-menu-close" type="button" aria-label="메뉴 닫기">×</button></div><div class="dg-mm-body"><h2 class="dg-mm-title">전체 메뉴</h2><p class="dg-mm-sub">원하는 업무를 선택하세요.</p><nav class="dg-mm-grid" aria-label="모바일 메뉴">${items.map(item=>`<a class="dg-mm-item dg-mm-${item.kind}${item.active?' is-current':''}" href="${item.href}"${item.active?' aria-current="page"':''}><span class="dg-mm-icon">${icons[item.kind]}</span><span class="dg-mm-copy"><span class="dg-mm-label">${item.label}</span><span class="dg-mm-desc">${item.desc}</span></span><span class="dg-mm-arrow" aria-hidden="true">›</span></a>`).join('')}</nav><div class="dg-mm-divider"></div><div class="dg-mm-quick-title">빠른 이용</div><div class="dg-mm-quick"><a class="dg-mm-calc-btn" href="/acquisition-calculator.html">비용 계산</a><a class="dg-mm-call-btn" href="tel:0324251500">032-425-1500 상담</a></div><div class="dg-mm-footer"><span class="dg-mm-footer-brand">등기로</span><span class="dg-mm-footer-sep">|</span><span>현재두 법무사 사무소</span></div></div>`;

  const close=panel.querySelector('#dg-shell-menu-close');btn.setAttribute('aria-controls','dg-shell-mobile-panel');
  const setOpen=open=>{panel.classList.toggle('open',open);panel.setAttribute('aria-hidden',open?'false':'true');btn.setAttribute('aria-expanded',open?'true':'false');document.body.classList.toggle('mobile-menu-open',open);if(open)requestAnimationFrame(()=>close?.focus({preventScroll:true}));else if(document.activeElement===close)btn.focus({preventScroll:true})};
  btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));close?.addEventListener('click',()=>setOpen(false));panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&panel.classList.contains('open'))setOpen(false)});
})();
