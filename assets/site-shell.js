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
  const removeDetailLegalInfo=()=>{
    if(!detailPaths.has(current))return;
    document.querySelectorAll('.subhero-copy .buttons a,.subhero-copy .buttons button,.hero .buttons a,.hero .buttons button').forEach(el=>{
      if((el.textContent||'').includes('법률정보'))el.remove();
    });
    const header=document.querySelector('header.dg-shell-header');
    if(header)header.querySelectorAll('nav a[href="/posts.html"]').forEach(a=>a.remove());
  };

  const coreModules=['/assets/site-header.js?v=20260917-clean','/assets/site-footer.js?v=20260917-compact'];
  Promise.all(coreModules.map(loadScript)).then(()=>{normalizePhoneCtas();removeDetailLegalInfo();}).catch(()=>{normalizePhoneCtas();removeDetailLegalInfo();});

  /* AI 등기로 플로팅 아이콘/패널은 전 페이지에서 설치하지 않음 */
  document.querySelectorAll('.dg-ai-float,.dg-ai-panel,#dg-ai-open,#dg-ai-panel,script[data-dg-ai-widget]').forEach(el=>el.remove());

  const inheritanceDetailPaths=new Set(['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html']);
  if(inheritanceDetailPaths.has(current))loadScript('/assets/analytics.js').catch(()=>{});
  if(current==='/corporate.html')loadScript('/assets/corporate-extra.js?v=20260911-1').catch(()=>{});
});
