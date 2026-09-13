/* Google Analytics 4 - site-wide loader */
(() => {
  const measurementId = 'G-E7367RF0XY';
  if (window.__deunggiroGa4Loaded) return;
  window.__deunggiroGa4Loaded = true;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId);

  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
  document.head.appendChild(script);

  /* 계산기 페이지도 메인과 동일한 공통 헤더·모바일 메뉴 사용 */
  if (location.pathname === '/acquisition-calculator.html' || location.pathname === '/corporate-calculator.html') {
    const shell = document.createElement('script');
    shell.src = '/assets/site-shell.js?v=20260912-calculator-header';
    shell.defer = true;
    document.head.appendChild(shell);

    /* 계산기 카운터는 firestore-counter-public.js 한 파일에서만 처리 */
    if (!document.querySelector('script[data-dg-counter]')) {
      const counter = document.createElement('script');
      counter.src = '/assets/firestore-counter-public.js?v=20260914-single';
      counter.defer = true;
      counter.dataset.dgCounter = '1';
      document.head.appendChild(counter);
    }
  }
})();
