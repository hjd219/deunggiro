(()=>{'use strict';
const body=document.body,stage=document.querySelector('.dg-scroll-stage'),mask=document.querySelector('.dg-scroll-mask'),track=document.querySelector('.dg-scroll-track');
if(!body.hasAttribute('data-dg-scroll')||!stage||!mask||!track)return;
let start=0,maskH=0,trackH=0,travel=0,lead=0,raf=0,lastW=innerWidth;
const mobile=()=>matchMedia('(max-width:800px)').matches;
const viewport=()=>Math.round(document.documentElement.clientHeight);
function paint(){
 raf=0;
 const p=Math.max(0,(scrollY||0)-start);
 const moved=Math.min(p,travel+lead);
 track.style.transform='translate3d(0,'+Math.round(maskH-moved)+'px,0)';
}
function measure(){
 const vh=viewport();
 document.documentElement.style.setProperty('--dg-vh',vh+'px');
 maskH=mask.clientHeight;
 trackH=track.scrollHeight;
 travel=maskH+trackH;
 /* One transition rule only: footer enters near the end while the last content is still visible. */
 lead=mobile()?Math.round(Math.max(28,Math.min(52,maskH*.055))):Math.round(Math.max(36,Math.min(72,maskH*.06)));
 stage.style.height=(travel+vh-lead)+'px';
 start=stage.offsetTop;
 paint();
}
function queue(){if(!raf)raf=requestAnimationFrame(paint)}
addEventListener('scroll',queue,{passive:true});
addEventListener('resize',()=>{const w=innerWidth;if(Math.abs(w-lastW)>2){lastW=w;measure()}},{passive:true});
addEventListener('orientationchange',()=>setTimeout(measure,150));
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);
requestAnimationFrame(()=>requestAnimationFrame(measure));
})();