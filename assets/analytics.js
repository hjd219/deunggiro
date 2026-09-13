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
  }
})();
