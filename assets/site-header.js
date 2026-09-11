/* SITE_HEADER_V2 - 정적 HTML 헤더를 유지하고 동작만 담당 */
(function(){
  const current=location.pathname;
  const activePath=current.startsWith('/posts/')?'/posts.html':current;

  /* 새로고침 시 기존 헤더를 다른 마크업으로 교체하지 않는다.
     각 페이지 HTML에 이미 들어있는 헤더를 그대로 사용해 메뉴 깜빡임을 방지한다. */
  const header=document.querySelector('header.header,header.dg-shell-header');
  if(!header) return;

  header.querySelectorAll('nav a').forEach(a=>{
    let path;
    try{ path=new URL(a.href,location.origin).pathname; }catch(_){ return; }
    if(path===activePath || (activePath==='/' && (path==='/'||path==='/index.html'))){
      a.setAttribute('aria-current','page');
    }else{
      a.removeAttribute('aria-current');
    }
  });

  const btn=document.getElementById('mobile-menu-btn') || document.getElementById('dg-shell-menu-btn');
  const panel=document.getElementById('mobile-menu-panel') || document.getElementById('dg-shell-mobile-panel');
  const close=document.getElementById('mobile-menu-close') || document.getElementById('dg-shell-menu-close');
  if(!btn||!panel) return;

  const setOpen=open=>{
    panel.classList.toggle('open',open);
    panel.setAttribute('aria-hidden',open?'false':'true');
    btn.setAttribute('aria-expanded',open?'true':'false');
    document.body.classList.toggle('mobile-menu-open',open);
  };

  btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
  close?.addEventListener('click',()=>setOpen(false));
  panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape') setOpen(false)});
})();
