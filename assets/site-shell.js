document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;

  const loadScript=(src)=>new Promise((resolve,reject)=>{
    if(document.querySelector(`script[src="${src}"]`)){
      resolve();
      return;
    }
    const script=document.createElement('script');
    script.src=src;
    script.async=false;
    script.onload=resolve;
    script.onerror=reject;
    document.head.appendChild(script);
  });

  const normalizePhoneCtas=()=>{
    document.querySelectorAll('a[href^="tel:0324251500"]').forEach(a=>{
      if(a.closest('footer,.footer,.dg-shell-footer')) return;
      const isCta=
        a.matches('.btn,.phone,.dg-shell-phone,.dg-shell-mobile-call,.mobile-only') ||
        a.closest('.buttons,.contact,.dg-shell-contact,.subhero,.hero,.header,.dg-shell-header');
      if(!isCta) return;
      a.classList.add('dg-phone-cta');
      a.textContent='032-425-1500 상담';
    });
  };

  const coreModules=[
    '/assets/site-header.js?v=20260911-1',
    '/assets/site-footer.js?v=20260911-1'
  ];

  Promise.all(coreModules.map(loadScript))
    .then(normalizePhoneCtas)
    .catch(()=>normalizePhoneCtas());

  if(current==='/corporate.html'){
    loadScript('/assets/corporate-extra.js?v=20260911-1').catch(()=>{});
  }
});
