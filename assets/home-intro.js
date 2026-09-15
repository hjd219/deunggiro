(()=>{
  const m=document.getElementById('dg-intro-backdrop');
  if(m){
    const o=()=>{m.classList.add('is-open');m.setAttribute('aria-hidden','false')};
    const c=()=>{m.classList.remove('is-open');m.setAttribute('aria-hidden','true')};
    document.querySelectorAll('.dg-intro-open').forEach(b=>b.addEventListener('click',o));
    m.querySelector('.dg-intro-close')?.addEventListener('click',c);
    m.addEventListener('click',e=>{if(e.target===m)c()});
    document.addEventListener('keydown',e=>{if(e.key==='Escape')c()});
  }
  const ai=document.createElement('script');
  ai.src='/assets/ai-deunggiro-widget.js?v=20260915-2';
  ai.defer=true;
  document.body.appendChild(ai);
})();
