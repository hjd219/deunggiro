(()=>{'use strict';
const root=document.body;
const stage=document.querySelector('.dg-scroll-stage');
const mask=document.querySelector('.dg-scroll-mask');
const track=document.querySelector('.dg-scroll-track');
if(!root.hasAttribute('data-dg-scroll')||!stage||!mask||!track)return;

let start=0,maskH=0,trackH=0,travel=0,footerOverlap=0,raf=0;
const viewportHeight=()=>Math.round(document.documentElement.clientHeight);

function render(){
  raf=0;
  const p=Math.max(0,(window.scrollY||0)-start);
  const moved=Math.min(p,travel);
  track.style.transform='translate3d(0,'+Math.round(maskH-moved)+'px,0)';
  root.classList.toggle('dg-scroll-done',p>=travel);
}
function measure(){
  const vh=viewportHeight();
  document.documentElement.style.setProperty('--dg-vh',vh+'px');
  track.style.transform='translate3d(0,0,0)';
  maskH=mask.clientHeight;
  trackH=track.scrollHeight;
  travel=maskH+trackH;
  // Footer begins entering before the last content has completely left the mask.
  // One variable owns this transition so it is easy to tune later.
  footerOverlap=Math.max(72,Math.min(150,Math.round(vh*.14)));
  stage.style.height=(travel+vh-footerOverlap)+'px';
  start=stage.offsetTop;
  render();
}
function queueRender(){if(!raf)raf=requestAnimationFrame(render)}
addEventListener('scroll',queueRender,{passive:true});
addEventListener('resize',()=>requestAnimationFrame(measure),{passive:true});
addEventListener('orientationchange',()=>setTimeout(measure,180));
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);else measure();
requestAnimationFrame(()=>requestAnimationFrame(measure));
})();