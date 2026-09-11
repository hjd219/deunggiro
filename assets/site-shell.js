document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;

  /* SITE_HEADER_LOADER_V1 - 공통 헤더/모바일 메뉴는 별도 파일에서만 실행 */
  const headerScript=document.createElement('script');
  headerScript.src='/assets/site-header.js?v=20260911-1';
  headerScript.defer=true;
  document.head.appendChild(headerScript);

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
});
