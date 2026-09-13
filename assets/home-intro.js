(()=>{
  const m=document.getElementById('dg-intro-backdrop');
  if(!m)return;
  const o=()=>{m.classList.add('is-open');m.setAttribute('aria-hidden','false')};
  const c=()=>{m.classList.remove('is-open');m.setAttribute('aria-hidden','true')};
  document.querySelectorAll('.dg-intro-open').forEach(b=>b.addEventListener('click',o));
  m.querySelector('.dg-intro-close')?.addEventListener('click',c);
  m.addEventListener('click',e=>{if(e.target===m)c()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')c()});
})();
