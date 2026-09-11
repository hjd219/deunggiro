document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;
  const detailTitles={
    '/inheritance.html':{title:'상속등기는',icon:'<svg viewBox="0 0 48 48"><path d="M12 7h18l7 7v27H12z" stroke="#258ed0" stroke-width="3" fill="none"/><path d="M30 7v8h7M18 25l4 4 9-10" stroke="#25a8df" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'},
    '/corporate.html':{title:'법인등기는',icon:'<svg viewBox="0 0 48 48"><path d="M9 41h30M13 41V20h22v21M18 20v-7h12v7" stroke="#7766d5" stroke-width="3" fill="none"/><path d="M19 27h3m5 0h3m-11 7h3m5 0h3" stroke="#9a7be0" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'},
    '/realestate.html':{title:'부동산등기는',icon:'<svg viewBox="0 0 48 48"><path d="M7 23 24 9l17 14v18H12V24" stroke="#20a38e" stroke-width="3" fill="none"/><path d="M19 41V29h10v12" stroke="#53bba9" stroke-width="3" fill="none"/></svg>'},
    '/renunciation.html':{title:'상속포기·한정승인은',icon:'<svg viewBox="0 0 48 48"><path d="M24 7 38 12v10c0 9-5.5 15.5-14 20-8.5-4.5-14-11-14-20V12z" stroke="#c89725" stroke-width="3" fill="none"/><path d="M16 22h16M24 16v12M18 22l-4 6h8zm12 0-4 6h8z" stroke="#c89725" stroke-width="2.5" fill="none"/></svg>'},
    '/family.html':{title:'가사는',icon:'<svg viewBox="0 0 48 48"><circle cx="18" cy="18" r="6" stroke="#cf679d" stroke-width="3" fill="none"/><circle cx="31" cy="19" r="5" stroke="#7b6bd0" stroke-width="3" fill="none"/><path d="M8 39c1-8 5-12 10-12s9 4 10 12M26 30c5-3 12 1 13 9" stroke="#cf679d" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'}
  };
  const detail=detailTitles[current];
  if(!detail) return;
  const h1=document.querySelector('.subhero-copy h1,.service-hero h1,.subhero h1,.hero h1');
  if(!h1||document.querySelector('.dg-detail-title-block')) return;
  const oldLabel=h1.previousElementSibling;
  if(oldLabel&&oldLabel.classList.contains('label')) oldLabel.remove();
  h1.innerHTML=`${detail.title} <span class="dg-detail-brand">등기로</span>`;
  const block=document.createElement('div');block.className='dg-detail-title-block';
  const row=document.createElement('div');row.className='dg-detail-title-row';
  const icon=document.createElement('span');icon.className='dg-detail-title-icon';icon.innerHTML=detail.icon;
  const line=document.createElement('div');line.className='dg-detail-title-line';
  h1.parentNode.insertBefore(block,h1);block.appendChild(row);row.appendChild(icon);row.appendChild(h1);block.appendChild(line);
  const style=document.createElement('style');style.id='dg-detail-title-v1';style.textContent=`
    .dg-detail-title-block{display:inline-block;max-width:100%;margin-top:4px}
    .dg-detail-title-row{display:flex;align-items:center;gap:11px;max-width:100%}
    .dg-detail-title-icon{width:46px;height:46px;flex:0 0 46px;border:1px solid #e0e6ec;border-radius:13px;background:#fff;box-shadow:0 4px 12px rgba(31,41,55,.04);padding:8px;display:grid;place-items:center}
    .dg-detail-title-icon svg{width:100%;height:100%;display:block}
    .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:clamp(34px,4.4vw,49px)!important;line-height:1.16!important;letter-spacing:-2.8px!important;margin:0!important;font-weight:900!important;white-space:nowrap!important}
    .dg-detail-brand{color:#36a9e1!important}
    .dg-detail-title-line{height:3px;width:100%;background:#82cef1;border-radius:2px;margin-top:14px}
    .dg-detail-title-block+p{margin-top:24px!important}
    @media(max-width:800px){
      .dg-detail-title-block{max-width:100%;margin-top:2px}
      .dg-detail-title-row{gap:8px}
      .dg-detail-title-icon{width:38px;height:38px;flex-basis:38px;border-radius:11px;padding:6px}
      .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:clamp(20px,6.2vw,27px)!important;letter-spacing:-1.65px!important;white-space:nowrap!important}
      .dg-detail-title-line{margin-top:11px}
      .dg-detail-title-block+p{margin-top:21px!important}
    }
    @media(max-width:360px){
      .dg-detail-title-row{gap:7px}
      .dg-detail-title-icon{width:34px;height:34px;flex-basis:34px;padding:5px}
      .subhero .dg-detail-title-row h1,.service-hero .dg-detail-title-row h1,.hero .dg-detail-title-row h1{font-size:19px!important;letter-spacing:-1.4px!important}
    }`;
  document.head.appendChild(style);
});
