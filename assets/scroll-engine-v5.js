(()=>{'use strict';
const stage=document.querySelector('.v53-stage');
const mask=document.querySelector('.v53-window');
const track=document.querySelector('.v53-track');
if(!stage||!mask||!track)return;

stage.classList.add('dg-scroll-stage');
mask.classList.add('dg-scroll-mask');
track.classList.add('dg-scroll-track');

let start=0, maskH=0, trackH=0, travel=0, raf=0;

function viewportHeight(){
  return Math.round(document.documentElement.clientHeight);
}
function measure(){
  const vh=viewportHeight();
  document.documentElement.style.setProperty('--dg-vh',vh+'px');

  track.style.transform='translate3d(0,0,0)';
  maskH=mask.clientHeight;
  trackH=track.scrollHeight;

  // Track starts immediately below the mask and ends when its bottom reaches mask top.
  travel=maskH+trackH;

  // Footer is placed at viewport bottom exactly when track completes.
  // stage top is 0 on these service pages, so height = travel + viewport height.
  stage.style.height=(travel+vh)+'px';
  start=stage.offsetTop;
  render();
}
function render(){
  raf=0;
  const p=Math.max(0,(window.scrollY||0)-start);
  const moved=Math.min(p,travel);
  track.style.transform='translate3d(0,'+Math.round(maskH-moved)+'px,0)';
  document.body.classList.toggle('dg-scroll-done',p>=travel);
}
function requestRender(){
  if(!raf)raf=requestAnimationFrame(render);
}
addEventListener('scroll',requestRender,{passive:true});
addEventListener('resize',()=>requestAnimationFrame(measure),{passive:true});
addEventListener('orientationchange',()=>setTimeout(measure,180));
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);
else measure();
requestAnimationFrame(()=>requestAnimationFrame(measure));
})();