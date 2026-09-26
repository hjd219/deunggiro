/* HOME_MOBILE_MENU_V1 - 기존 우측 70% 메뉴를 메인 헤더에 복원 */
(function(){
  const header=document.querySelector('body>header');
  if(!header)return;
  const nav=header.querySelector('.nav');
  if(!nav)return;
  if(document.getElementById('dg-shell-menu-btn'))return;

  const btn=document.createElement('button');
  btn.className='dg-shell-mobile-menu-btn';
  btn.id='dg-shell-menu-btn';
  btn.type='button';
  btn.setAttribute('aria-expanded','false');
  btn.setAttribute('aria-controls','dg-shell-mobile-panel');
  btn.innerHTML='<span aria-hidden="true">☰</span> 메뉴';
  nav.appendChild(btn);

  const panel=document.createElement('div');
  panel.className='dg-shell-mobile-panel';
  panel.id='dg-shell-mobile-panel';
  panel.setAttribute('aria-hidden','true');
  panel.setAttribute('role','dialog');
  panel.setAttribute('aria-modal','true');
  panel.setAttribute('aria-label','메뉴');
  document.body.appendChild(panel);

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
    ['home','홈','등기로 메인으로 이동','/'],
    ['inherit','상속등기','단독상속 · 공동상속 · 유증','/inheritance.html'],
    ['renounce','상속포기·한정승인','기한 · 절차 · 필요서류 · 청산','/renunciation.html'],
    ['corp','법인등기','설립 · 변경 · 증자 · 회사계속','/corporate.html'],
    ['real','부동산등기','매매 · 증여 · 재산분할 · 담보','/realestate.html'],
    ['family','가사','이혼 · 후견 · 개명 · 친생자관계','/family.html'],
    ['info','법률정보','최신정보 · 판례 · 실무가이드','/posts.html']
  ];
  panel.innerHTML='<div class="dg-mm-top"><span class="dg-mm-brand">메뉴</span><button class="dg-mm-close" id="dg-shell-menu-close" type="button" aria-label="메뉴 닫기">×</button></div><div class="dg-mm-body"><nav class="dg-mm-grid" aria-label="모바일 메뉴">'+items.map(item=>'<a class="dg-mm-item dg-mm-'+item[0]+(item[0]==='home'?' is-current':'')+'" href="'+item[3]+'"><span class="dg-mm-icon">'+icons[item[0]]+'</span><span class="dg-mm-copy"><span class="dg-mm-label">'+item[1]+'</span><span class="dg-mm-desc">'+item[2]+'</span></span><span class="dg-mm-arrow" aria-hidden="true">›</span></a>').join('')+'</nav><div class="dg-mm-divider"></div><div class="dg-mm-quick-title">빠른 이용</div><div class="dg-mm-quick"><div class="dg-mm-calc-split"><a class="dg-mm-calc-btn" href="/acquisition-calculator.html">부동산 비용계산</a><a class="dg-mm-calc-btn dg-mm-corp-calc-btn" href="/corporate-calculator.html">법인 비용계산</a></div><a class="dg-mm-call-btn" href="tel:0324251500">032-425-1500 상담</a></div><div class="dg-mm-footer"><span class="dg-mm-footer-brand">등기로</span><span class="dg-mm-footer-sep">|</span><span>현재두 법무사 사무소</span></div></div>';


  /* 빠른 이용 비용계산: 모바일 2분할 */
  const mmStyle=document.createElement('style');
  mmStyle.id='dg-mm-calc-split-style';
  mmStyle.textContent='.dg-mm-calc-split{display:grid;grid-template-columns:1fr 1fr;gap:0;min-width:0;border:1.5px solid #37aee4;border-radius:16px;overflow:hidden;background:#fff}.dg-mm-calc-split .dg-mm-calc-btn{display:flex;align-items:center;justify-content:center;min-width:0;height:58px;padding:0 8px!important;border:0!important;border-radius:0!important;background:#fff!important;box-shadow:none!important;white-space:nowrap;font-size:13px}.dg-mm-calc-split .dg-mm-calc-btn+.dg-mm-calc-btn{border-left:1px solid #d5eaf3!important}';
  document.head.appendChild(mmStyle);

  const close=panel.querySelector('#dg-shell-menu-close');
  const setOpen=open=>{
    panel.classList.toggle('open',open);
    panel.setAttribute('aria-hidden',open?'false':'true');
    btn.setAttribute('aria-expanded',open?'true':'false');
    document.body.classList.toggle('mobile-menu-open',open);
  };
  btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
  close.addEventListener('click',()=>setOpen(false));
  panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&panel.classList.contains('open'))setOpen(false)});

  /* Same-origin page warmup: fetch only when the user shows navigation intent. */
  const warmed=new Set();
  const warm=a=>{
    if(!a||!a.href||a.target==='_blank'||a.hasAttribute('download'))return;
    let u;try{u=new URL(a.href,location.href)}catch(_){return}
    if(u.origin!==location.origin||u.pathname===location.pathname||!u.pathname.endsWith('.html')&&u.pathname!=='/')return;
    const key=u.pathname+u.search;if(warmed.has(key))return;warmed.add(key);
    const l=document.createElement('link');l.rel='prefetch';l.as='document';l.href=key;document.head.appendChild(l);
  };
  /* Desktop only: mobile touch prefetch can compete with navigation/rendering on iOS. */
  const canHover=window.matchMedia&&window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  if(canHover){
    document.addEventListener('pointerover',e=>warm(e.target.closest&&e.target.closest('a[href]')),{passive:true});
  }

})();