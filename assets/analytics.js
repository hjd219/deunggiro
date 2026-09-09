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

/* CALCULATOR_BANK_ACCOUNTS_V1 */
document.addEventListener('DOMContentLoaded', () => {
  const calculatorPaths = new Set(['/acquisition-calculator.html', '/corporate-calculator.html']);
  if (!calculatorPaths.has(location.pathname)) return;
  const result = document.querySelector('.result');
  if (!result || result.querySelector('.dg-bank-accounts')) return;

  const box = document.createElement('div');
  box.className = 'dg-bank-accounts';
  box.innerHTML = `
    <div class="dg-bank-title">입금계좌</div>
    <div class="dg-bank-row"><b>신한은행</b><span>110-482-692656</span><small>현재두법무사사무소</small></div>
    <div class="dg-bank-row"><b>카카오뱅크</b><span>3333-07-6560416</span><small>현재두법무사사무소</small></div>`;

  const consult = result.querySelector('.consult');
  const officeFooter = result.querySelector('.office-footer');
  if (consult) result.insertBefore(box, consult);
  else if (officeFooter) result.insertBefore(box, officeFooter);
  else result.appendChild(box);

  const style = document.createElement('style');
  style.textContent = `
    .dg-bank-accounts{margin-top:14px;padding:14px 15px;border:1px solid #b9ddec;border-radius:12px;background:#f4fbfe;color:#263e53}
    .dg-bank-title{margin-bottom:8px;color:#168dca;font-size:13px;font-weight:900}
    .dg-bank-row{display:grid;grid-template-columns:72px minmax(0,1fr);gap:2px 9px;align-items:center;padding:5px 0;font-size:12.5px;line-height:1.45}
    .dg-bank-row b{color:#172840;font-weight:900}.dg-bank-row span{color:#172840;font-weight:850;letter-spacing:.1px}.dg-bank-row small{grid-column:2;color:#647486;font-size:10.5px;font-weight:700}
    @media(max-width:480px){.dg-bank-accounts{padding:12px}.dg-bank-row{grid-template-columns:68px minmax(0,1fr);font-size:12px}.dg-bank-row small{font-size:10px}}
    @media print{.dg-bank-accounts{display:block!important;margin-top:9px!important;padding:9px 11px!important;border:1px solid #91adbf!important;background:#f2faff!important;break-inside:avoid!important}.dg-bank-title{font-size:11px!important;margin-bottom:4px!important}.dg-bank-row{grid-template-columns:62px 120px 1fr!important;gap:5px!important;padding:2px 0!important;font-size:9px!important}.dg-bank-row small{grid-column:auto!important;font-size:8.5px!important}}
  `;
  document.head.appendChild(style);
});
