/* SITE_HEADER_V4 - 정적 공통 헤더 동작 전용 */
(function(){
  const current=location.pathname;
  const activePath=current.startsWith('/posts/')?'/posts.html':current;
  const header=document.querySelector('header.dg-shell-header');
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

  const btn=document.getElementById('dg-shell-menu-btn');
  const panel=document.getElementById('dg-shell-mobile-panel');
  const close=document.getElementById('dg-shell-menu-close');
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
