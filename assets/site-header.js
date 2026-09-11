/* SITE_HEADER_V1 - 공통 헤더와 모바일 메뉴만 담당 */
(function(){
  const current=location.pathname;
  const navItems=[
    ['/','홈'],
    ['/inheritance.html','상속등기'],
    ['/renunciation.html','상속포기·한정승인'],
    ['/corporate.html','법인등기'],
    ['/realestate.html','부동산등기'],
    ['/family.html','가사'],
    ['/posts.html','법률정보']
  ];
  const activePath=current.startsWith('/posts/')?'/posts.html':current;
  const navHtml=navItems.map(([href,label])=>`<a href="${href}"${activePath===href?' aria-current="page"':''}>${label}</a>`).join('');
  const header=`<header class="dg-shell-header"><div class="dg-shell-inner"><a class="dg-shell-logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="dg-shell-nav">${navHtml}</nav><button class="dg-shell-mobile-menu-btn" id="dg-shell-menu-btn" type="button" aria-expanded="false">☰ 메뉴</button></div></header><div class="dg-shell-mobile-panel" id="dg-shell-mobile-panel" aria-hidden="true"><div class="dg-shell-mobile-grid">${navHtml}</div><button class="dg-shell-mobile-close" id="dg-shell-menu-close" type="button">메뉴 닫기 ↑</button></div>`;

  const replaceFirst=(selectors,html)=>{
    for(const selector of selectors){
      const el=document.querySelector(selector);
      if(el){
        el.outerHTML=html;
        return true;
      }
    }
    return false;
  };

  if(!replaceFirst(['header.header','header.dg-shell-header'],header)){
    document.body.insertAdjacentHTML('afterbegin',header);
  }

  const btn=document.getElementById('dg-shell-menu-btn');
  const panel=document.getElementById('dg-shell-mobile-panel');
  const close=document.getElementById('dg-shell-menu-close');
  if(!btn||!panel) return;

  const setOpen=open=>{
    panel.classList.toggle('open',open);
    panel.setAttribute('aria-hidden',open?'false':'true');
    btn.setAttribute('aria-expanded',open?'true':'false');
  };
  btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
  close?.addEventListener('click',()=>setOpen(false));
  panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape') setOpen(false)});
})();
