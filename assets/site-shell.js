document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;

  const loadScript=(src)=>new Promise((resolve,reject)=>{
    if(document.querySelector(`script[src="${src}"]`)){resolve();return;}
    const script=document.createElement('script');
    script.src=src;script.async=false;script.onload=resolve;script.onerror=reject;
    document.head.appendChild(script);
  });

  const normalizePhoneCtas=()=>{
    document.querySelectorAll('a[href^="tel:0324251500"]').forEach(a=>{
      if(a.closest('footer,.footer,.dg-shell-footer')) return;
      const isCta=a.matches('.btn,.phone,.dg-shell-phone,.dg-shell-mobile-call,.mobile-only')||a.closest('.buttons,.subhero,.hero,.header,.dg-shell-header');
      if(!isCta)return;
      a.classList.add('dg-phone-cta');a.textContent='032-425-1500 상담';
    });
  };

  const isIndividualPost=current.startsWith('/posts/');
  if(isIndividualPost){
    document.querySelectorAll('header.header,header.dg-shell-header').forEach(el=>el.remove());
  }
  const coreModules=isIndividualPost
    ? ['/assets/site-footer.js?v=20260917-horizontal3']
    : ['/assets/site-header.js?v=20260917-clean2','/assets/site-footer.js?v=20260917-horizontal3'];
  Promise.all(coreModules.map(loadScript)).then(normalizePhoneCtas).catch(normalizePhoneCtas);

  // Current article pages are the only callers of this shared shell that
  // need analytics and visit tracking. Service hubs use their own assets.
  if(isIndividualPost){
    loadScript('/assets/analytics.js?v=20261018-1').catch(()=>{});
    loadScript('/assets/blog-view-tracker.js?v=20261018-1').catch(()=>{});
    loadScript('/assets/feedback-v1.js?v=20261025-1').catch(error=>console.warn('[DGFeedback] script unavailable',error));
  }
});
