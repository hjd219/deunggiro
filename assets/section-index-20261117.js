(function pageSectionIndex(){
  'use strict';
  if(window.__dgSectionIndex) return;
  const path=location.pathname.toLowerCase();
  if(/\/(?:posts?|blog)(?:[\/.-]|$)/.test(path)||/(?:calculator|self-check|privacy|disclaimer|email-policy|preview)\.html$/.test(path)) return;
  if(document.documentElement.classList.contains('dg-calculator-page')) return;
  if(document.querySelector('.about-side-index')) return;
  const stage=document.querySelector('.v53-stage');
  const win=document.querySelector('.v53-window');
  const track=document.querySelector('.v53-track');
  const hero=document.querySelector('body > .hero, body > section.hero');
  if(!stage||!win||!track||!hero) return;
  window.__dgSectionIndex=true;
  const sections=[...track.querySelectorAll(':scope > section')].filter(s=>{
    if(s.getAttribute('aria-hidden')==='true') return false;
    if(s.hasAttribute('data-scroll-sentinel')) return false;
    if(s.classList.contains('dg-spacer')) return false;
    return !!(s.querySelector('h2,h3')||s.classList.contains('person')||s.classList.contains('dg-services')||s.classList.contains('intro'));
  });
  const label=s=>{
    if(s===hero)return '소개';
    const cl=s.classList;
    if(cl.contains('person'))return '법무사';
    if(cl.contains('intro'))return '등기로 소개';
    if(cl.contains('story-case-detail'))return '처리사례';
    if(cl.contains('story-cases'))return '관련 안내';
    if(cl.contains('dg-services')&&!s.querySelector('h2'))return '업무 안내';
    let h=s.querySelector('h2')||s.querySelector('h3');
    let str=(h?.textContent||'상세 안내').replace(/\s+/g,' ').trim().replace(/\s*→\s*/g,'');
    str=str.replace(/자주 묻는 질문$/,'FAQ').replace(/필요서류$/,'필요서류');
    return str.length>14 ? str.slice(0,13)+'…' : str;
  };
  const landmarks=[{el:hero,label:'소개'},...sections.map(s=>({el:s,label:label(s)}))];
  if(landmarks.length<3) return;
  const style=document.createElement('style');
  style.id='dg-section-index-styles';
  style.textContent=`
  .dg-page-index{position:fixed;z-index:205;right:clamp(11px,1.8vw,30px);top:50%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:stretch;max-height:min(77vh,690px);overflow-y:auto;overscroll-behavior:contain;scrollbar-width:none;gap:0;padding:2px 8px 2px 23px;transition:opacity .2s ease,visibility .2s ease}
  .dg-page-index::-webkit-scrollbar{display:none}
  .dg-page-index::before{content:"";position:absolute;left:9px;top:20px;bottom:20px;width:2px;background:rgba(255,255,255,.95);box-shadow:0 1px 3px #071b27,0 0 7px rgba(0,0,0,.82);pointer-events:none}
  .dg-page-index.is-past{opacity:0;visibility:hidden;pointer-events:none}
  .dg-page-index button{appearance:none;position:relative;display:flex;align-items:center;gap:7px;min-width:136px;min-height:40px;margin:0;padding:7px 0;border:0;background:transparent;color:#fff!important;text-shadow:-1px -1px 2px rgba(0,0,0,.95),1px 1px 2px rgba(0,0,0,.95),0 2px 7px rgba(0,0,0,.95);cursor:pointer;font:750 12px/1.4 system-ui,-apple-system,"Malgun Gothic",sans-serif;text-align:left;white-space:nowrap;transition:font-size .2s ease}
  .dg-page-index button::before{content:"";position:absolute;left:-13px;top:50%;transform:translate(-50%,-50%);width:10px;height:10px;box-sizing:border-box;border:2px solid #fff;border-radius:50%;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.6),0 1px 7px rgba(0,0,0,.85)}
  .dg-page-index button .n{min-width:22px;color:inherit;font-size:inherit;font-variant-numeric:tabular-nums;letter-spacing:.02em}
  .dg-page-index button[aria-current="step"]{font-size:15px;font-weight:900}
  .dg-page-index button[aria-current="step"]::before{width:13px;height:13px;background:#1589bb;border-color:#fff}
  .dg-page-index button:focus-visible{outline:2px solid #fff;outline-offset:3px}
  @media(max-width:900px){.dg-page-index{display:none!important}}
  @media(prefers-reduced-motion:reduce){.dg-page-index,.dg-page-index button{transition:none!important}}
  `;
  document.head.appendChild(style);
  const nav=document.createElement('nav');
  nav.className='dg-page-index';
  nav.setAttribute('aria-label','현재 페이지 구간 이동');
  const buttons=landmarks.map((item,i)=>{
    const b=document.createElement('button');b.type='button';
    b.setAttribute('aria-label',String(i+1)+' '+item.label+' 구간으로 이동');
    const n=document.createElement('span');n.className='n';n.textContent=String(i+1).padStart(2,'0');
    const name=document.createElement('span');name.textContent=item.label;
    b.append(n,name);nav.appendChild(b);return b;
  });
  document.body.appendChild(nav);
  const reduced=matchMedia('(prefers-reduced-motion:reduce)');
  function relTop(section){
    const t=track.getBoundingClientRect();
    const s=section.getBoundingClientRect();
    return s.top-t.top;
  }
  function stageStart(){return stage.getBoundingClientRect().top+window.scrollY}
  function goto(i){
    if(i===0){window.scrollTo({top:0,behavior:reduced.matches?'auto':'smooth'});return}
    const top=stageStart()+win.clientHeight+relTop(landmarks[i].el)-Math.max(20,win.clientHeight*.065);
    const max=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
    window.scrollTo({top:Math.max(0,Math.min(top,max)),behavior:reduced.matches?'auto':'smooth'});
  }
  buttons.forEach((b,i)=>b.addEventListener('click',()=>goto(i)));
  let active=-1,scheduled=false;
  function paint(){
    scheduled=false;
    const y=window.scrollY;
    const start=stageStart(),wh=win.clientHeight;
    let idx=0;
    if(y>=start+wh*.6){
      idx=1;
      for(let i=2;i<landmarks.length;i++){
        if(y >= start+wh+relTop(landmarks[i].el)-wh*.31) idx=i;
      }
    }
    const footer=document.querySelector('.dg-shell-footer');
    nav.classList.toggle('is-past',!!footer&&footer.getBoundingClientRect().top<window.innerHeight*.82);
    if(idx!==active){
      active=idx;
      buttons.forEach((b,j)=>{if(j===idx)b.setAttribute('aria-current','step');else b.removeAttribute('aria-current')});
      if(idx>=0 && idx<buttons.length && nav.scrollHeight>nav.clientHeight){
        const node=buttons[idx],middle=node.offsetTop+node.offsetHeight/2-nav.clientHeight/2;
        nav.scrollTop=Math.max(0,middle);
      }
    }
  }
  function schedule(){
    if(scheduled)return;
    scheduled=true;
    requestAnimationFrame(paint);
  }
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',schedule,{passive:true});
  if('ResizeObserver' in window){const ro=new ResizeObserver(schedule);ro.observe(track);ro.observe(stage)}
  schedule();
})();