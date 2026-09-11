document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;
  const navItems=[['/','홈'],['/inheritance.html','상속등기'],['/renunciation.html','상속포기·한정승인'],['/corporate.html','법인등기'],['/realestate.html','부동산등기'],['/family.html','가사'],['/posts.html','법률정보']];
  const activePath=()=> current.startsWith('/posts/')?'/posts.html':current;
  const navHtml=navItems.map(([href,label])=>`<a href="${href}"${activePath()===href?' aria-current="page"':''}>${label}</a>`).join('');
  const header=`<header class="dg-shell-header"><div class="dg-shell-inner"><a class="dg-shell-logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="dg-shell-nav">${navHtml}</nav><button class="dg-shell-mobile-menu-btn" id="dg-shell-menu-btn" type="button" aria-expanded="false">☰ 메뉴</button></div></header><div class="dg-shell-mobile-panel" id="dg-shell-mobile-panel" aria-hidden="true"><div class="dg-shell-mobile-grid">${navHtml}</div><button class="dg-shell-mobile-close" id="dg-shell-menu-close" type="button">메뉴 닫기 ↑</button></div>`;
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

  /* SITE_FOOTER_LOADER_V1 - 상담영역/푸터는 별도 파일에서만 실행 */
  const footerScript=document.createElement('script');
  footerScript.src='/assets/site-footer.js?v=20260911-1';
  footerScript.defer=true;
  document.head.appendChild(footerScript);

  /* CORPORATE_EXTRA_LOADER_V1 - 법인 전용 코드는 별도 파일에서만 실행 */
  if(current==='/corporate.html'){
    const script=document.createElement('script');
    script.src='/assets/corporate-extra.js?v=20260911-1';
    script.defer=true;
    document.head.appendChild(script);
  }

  const btn=document.getElementById('dg-shell-menu-btn'),panel=document.getElementById('dg-shell-mobile-panel'),close=document.getElementById('dg-shell-menu-close');
  if(btn&&panel){
    const setOpen=o=>{panel.classList.toggle('open',o);panel.setAttribute('aria-hidden',o?'false':'true');btn.setAttribute('aria-expanded',o?'true':'false')};
    btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
    close?.addEventListener('click',()=>setOpen(false));
    panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)});
  }
});
