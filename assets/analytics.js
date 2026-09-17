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

/* Mobile fixed action bar - phone + calculator */
(() => {
  const install = () => {
    if (document.querySelector('.dg-mobile-actionbar')) return;

    const style = document.createElement('style');
    style.textContent = `
      .dg-mobile-actionbar{display:none}
      @media (max-width:900px){
        body{padding-bottom:calc(68px + env(safe-area-inset-bottom))!important}
        .dg-mobile-actionbar{
          position:fixed!important;
          left:0!important;
          right:0!important;
          bottom:0!important;
          z-index:2147483000;
          display:grid;
          grid-template-columns:1fr 1fr;
          gap:0;
          height:calc(64px + env(safe-area-inset-bottom));
          padding:0 12px env(safe-area-inset-bottom);
          box-sizing:border-box;
          background:rgba(255,255,255,.97);
          border-top:2px solid #36a9e1;
          box-shadow:0 -5px 18px rgba(23,40,64,.10);
          -webkit-backdrop-filter:blur(10px);
          backdrop-filter:blur(10px);
        }
        .dg-mobile-actionbar a{
          min-width:0;
          display:flex;
          align-items:center;
          justify-content:center;
          gap:9px;
          color:#172840;
          text-decoration:none;
          font-size:15px;
          line-height:1;
          font-weight:800;
          letter-spacing:-.4px;
          -webkit-tap-highlight-color:transparent;
        }
        .dg-mobile-actionbar a+a{border-left:1px solid #e4ebf0}
        .dg-mobile-actionbar svg{
          width:25px;
          height:25px;
          flex:0 0 25px;
          fill:none;
          stroke:#258ed0;
          stroke-width:2;
          stroke-linecap:round;
          stroke-linejoin:round;
        }
        .dg-mobile-actionbar a:active{background:#f3f8fb}
      }
    `;
    document.head.appendChild(style);

    const bar = document.createElement('nav');
    bar.className = 'dg-mobile-actionbar';
    bar.setAttribute('aria-label', '빠른 상담 메뉴');
    bar.innerHTML = `
      <a href="tel:0324251500" aria-label="전화상담 032-425-1500">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.2 3.8 4.9 5.1c-.7.4-1 1.2-.7 2 2.2 6.1 6.6 10.5 12.7 12.7.8.3 1.6 0 2-.7l1.3-2.3c.3-.6.2-1.3-.3-1.7l-3-2.2c-.5-.4-1.2-.3-1.7.1l-1.6 1.6a14.2 14.2 0 0 1-4.2-4.2L11 8.8c.4-.5.5-1.2.1-1.7l-2.2-3c-.4-.5-1.1-.6-1.7-.3Z"/></svg>
        <span>전화상담</span>
      </a>
      <a href="/acquisition-calculator.html" aria-label="부동산 등기비용 계산기">
        <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2.8" width="14" height="18.4" rx="2"/><path d="M8 6h8v3H8zM8 13h1m3 0h1m3 0h0M8 17h1m3 0h1m3 0h0"/></svg>
        <span>비용계산</span>
      </a>
    `;
    document.body.appendChild(bar);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', install, { once:true });
  } else {
    install();
  }
})();
