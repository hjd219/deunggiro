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

/* Mobile fixed action bar - phone + calculator */
(() => {
  const install = () => {
    if (document.querySelector('.dg-mobile-actionbar')) return;

    const style = document.createElement('style');
    style.textContent = `
      .dg-mobile-actionbar{display:none}
      @media (max-width:900px){
        body{padding-bottom:calc(78px + env(safe-area-inset-bottom))!important}
        .dg-mobile-actionbar{
          position:fixed;
          left:0;
          right:0;
          bottom:0;
          z-index:2147483000;
          display:grid;
          grid-template-columns:1fr 1fr;
          height:calc(72px + env(safe-area-inset-bottom));
          padding:0 0 env(safe-area-inset-bottom);
          box-sizing:border-box;
          overflow:hidden;
          background:#fff;
          border-top:1px solid rgba(37,142,208,.24);
          box-shadow:0 -5px 18px rgba(23,40,64,.13);
        }
        .dg-mobile-actionbar a{
          min-width:0;
          display:flex;
          align-items:center;
          justify-content:center;
          gap:12px;
          color:#fff;
          text-decoration:none;
          -webkit-tap-highlight-color:transparent;
        }
        .dg-mobile-actionbar .dg-phone{background:linear-gradient(135deg,#0b3974,#0758a7)}
        .dg-mobile-actionbar .dg-calc{background:linear-gradient(135deg,#159ee8,#27b8ef)}
        .dg-mobile-actionbar .dg-copy{display:flex;flex-direction:column;gap:5px;min-width:0}
        .dg-mobile-actionbar .dg-title{font-size:16px;line-height:1;font-weight:850;letter-spacing:-.45px;white-space:nowrap}
        .dg-mobile-actionbar .dg-sub{font-size:11.5px;line-height:1;color:rgba(255,255,255,.90);font-weight:600;white-space:nowrap}
        .dg-mobile-actionbar svg{
          width:29px;
          height:29px;
          flex:0 0 29px;
          fill:none;
          stroke:#fff;
          stroke-width:2;
          stroke-linecap:round;
          stroke-linejoin:round;
        }
        .dg-mobile-actionbar .dg-arrow{width:17px;height:17px;flex-basis:17px;margin-left:1px}
        .dg-mobile-actionbar a:active{filter:brightness(.94)}
      }
      @media (max-width:380px){
        .dg-mobile-actionbar a{gap:8px}
        .dg-mobile-actionbar svg{width:25px;height:25px;flex-basis:25px}
        .dg-mobile-actionbar .dg-title{font-size:15px}
        .dg-mobile-actionbar .dg-sub{font-size:10.5px}
      }
    `;
    document.head.appendChild(style);

    const bar = document.createElement('nav');
    bar.className = 'dg-mobile-actionbar';
    bar.setAttribute('aria-label', '빠른 상담 메뉴');
    bar.innerHTML = `
      <a class="dg-phone" href="tel:0324251500" aria-label="전화상담 032-425-1500">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.2 3.8 4.9 5.1c-.7.4-1 1.2-.7 2 2.2 6.1 6.6 10.5 12.7 12.7.8.3 1.6 0 2-.7l1.3-2.3c.3-.6.2-1.3-.3-1.7l-3-2.2c-.5-.4-1.2-.3-1.7.1l-1.6 1.6a14.2 14.2 0 0 1-4.2-4.2L11 8.8c.4-.5.5-1.2.1-1.7l-2.2-3c-.4-.5-1.1-.6-1.7-.3Z"/></svg>
        <span class="dg-copy"><span class="dg-title">전화상담</span><span class="dg-sub">032-425-1500</span></span>
      </a>
      <a class="dg-calc" href="/#calculator" aria-label="등기비용 계산기">
        <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="2.8" width="14" height="18.4" rx="2"/><path d="M8 6h8v3H8zM8 13h1m3 0h1m3 0h0M8 17h1m3 0h1m3 0h0"/></svg>
        <span class="dg-copy"><span class="dg-title">비용계산</span><span class="dg-sub">간편하게 확인하세요</span></span>
        <svg class="dg-arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>
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
