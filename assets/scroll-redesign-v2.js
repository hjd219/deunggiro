(()=>{const stage=document.querySelector('.v53-stage'),mask=document.querySelector('.v53-window'),track=document.querySelector('.v53-track');if(!stage||!mask||!track)return;
stage.classList.add('dg-r2-stage');mask.classList.add('dg-r2-mask');track.classList.add('dg-r2-track');
let start=0,travel=0,maskH=0,trackH=0,raf=0;
const render=()=>{raf=0;const p=Math.max(0,(window.scrollY||0)-start);const y=maskH-Math.min(p,travel);track.style.transform='translate3d(0,'+Math.round(y)+'px,0)';document.body.classList.toggle('dg-r2-finished',p>=travel);};
const measure=()=>{document.body.classList.remove('dg-r2-finished');track.style.transform='translate3d(0,0,0)';maskH=mask.clientHeight;trackH=track.scrollHeight;travel=maskH+trackH;stage.style.height=(travel+maskH)+'px';start=stage.offsetTop;render();};
const tick=()=>{if(!raf)raf=requestAnimationFrame(render)};
addEventListener('scroll',tick,{passive:true});addEventListener('resize',()=>requestAnimationFrame(measure),{passive:true});addEventListener('orientationchange',()=>setTimeout(measure,180));
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);else measure();requestAnimationFrame(()=>requestAnimationFrame(measure));
})();