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
      const isCta=a.matches('.btn,.phone,.dg-shell-phone,.dg-shell-mobile-call,.mobile-only')||a.closest('.buttons,.contact,.dg-shell-contact,.subhero,.hero,.header,.dg-shell-header');
      if(!isCta)return;
      a.classList.add('dg-phone-cta');a.textContent='032-425-1500 상담';
    });
  };

  const detailPaths=new Set([
    '/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html',
    '/renunciation-after.html','/limited-acceptance-liquidation.html'
  ]);

  const removeUnwanted=()=>{
    document.querySelectorAll('.related-posts-panel').forEach(el=>el.remove());
    document.querySelectorAll('section.contact,section.cta,section.dg-shell-contact,.dg-shell-contact').forEach(el=>el.remove());
    if(detailPaths.has(current)){
      document.querySelectorAll('.subhero-copy .buttons a,.subhero-copy .buttons button,.hero .buttons a,.hero .buttons button,.hero .actions a,.hero .actions button').forEach(el=>{if((el.textContent||'').includes('법률정보'))el.remove();});
      document.querySelectorAll('header.dg-shell-header nav a[href="/posts.html"],.dg-shell-mobile-panel a[href="/posts.html"]').forEach(a=>a.remove());
    }
    document.querySelectorAll('.dg-ai-float,.dg-ai-panel,#dg-ai-open,#dg-ai-panel,[class*="ai-deunggiro"],script[data-dg-ai-widget],script[src*="ai-deunggiro-widget"]').forEach(el=>el.remove());
  };

  const coreModules=['/assets/site-header.js?v=20260917-clean2','/assets/site-footer.js?v=20260917-horizontal3'];
  Promise.all(coreModules.map(loadScript)).then(()=>{normalizePhoneCtas();removeUnwanted();}).catch(()=>{normalizePhoneCtas();removeUnwanted();});
  removeUnwanted();

  const inheritanceDetailPaths=new Set(['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html']);
  if(inheritanceDetailPaths.has(current))loadScript('/assets/analytics.js').catch(()=>{});
  if(current==='/corporate.html')loadScript('/assets/corporate-extra.js?v=20260911-1').catch(()=>{});
  if(current==='/realestate.html')loadScript('/assets/realestate-case-cards.js?v=20260917-1').catch(()=>{});
  if(current==='/posts.html')loadScript('/assets/posts-case-tabs.js?v=20260917-1').catch(()=>{});
});
