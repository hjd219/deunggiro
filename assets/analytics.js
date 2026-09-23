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
})();

/* AI 등기로 - site-wide loader */
(() => {
  if (window.__deunggiroAiLoaderInstalled) return;
  window.__deunggiroAiLoaderInstalled = true;

  const install = () => {
    if (document.getElementById('dg-ai-panel') || document.querySelector('script[data-dg-ai-widget]')) return;
    const script = document.createElement('script');
    script.src = '/assets/ai-deunggiro-widget.js?v=20260915-5';
    script.defer = true;
    script.dataset.dgAiWidget = '1';
    document.body.appendChild(script);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', install, { once:true });
  } else {
    install();
  }
})();
