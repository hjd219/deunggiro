(()=>{'use strict';
const root=document.body;
const stage=document.querySelector('.dg-scroll-stage');
const mask=document.querySelector('.dg-scroll-mask');
const track=document.querySelector('.dg-scroll-track');
const end=track&&track.querySelector('.story-cases,.dg-services');
if(!root.hasAttribute('data-dg-scroll')||!stage||!mask||!track||!end)return;

let start=0,maskH=0,finalY=0,stopAt=0,releaseAt=0,vh=0,raf=0,lastWidth=innerWidth;
const isMobile=()=>matchMedia('(max-width:800px)').matches;
const viewportHeight=()=>Math.round(window.visualViewport?window.visualViewport.height:window.innerHeight);

function render(){
 raf=0;
 const p=Math.max(0,(scrollY||0)-start);
 root.classList.remove('dg-scroll-release');
 document.documentElement.style.setProperty('--dg-release-y','0px');
 if(p<stopAt){
   track.style.transform='translate3d(0,'+Math.round(maskH-p)+'px,0)';
   return;
 }
 track.style.transform='translate3d(0,'+Math.round(finalY)+'px,0)';
 if(p>releaseAt){
   const rise=Math.min(vh,p-releaseAt);
   root.classList.add('dg-scroll-release');
   document.documentElement.style.setProperty('--dg-release-y',(-Math.round(rise))+'px');
 }
}
function measure(){
 vh=viewportHeight();
 document.documentElement.style.setProperty('--dg-vh',vh+'px');
 maskH=mask.clientHeight;
 const endTop=end.offsetTop,endH=end.offsetHeight;
 if(isMobile()){
   finalY=maskH-20-(endTop+endH);
   stopAt=maskH-finalY;
   releaseAt=stopAt+Math.max(120,vh*.12);
 }else{
   const desiredTop=Math.max(16,Math.min(64,maskH-endH-16));
   finalY=desiredTop-endTop;
   stopAt=maskH-finalY;
   releaseAt=stopAt+Math.max(260,vh*.35);
 }
 const contentBottom=endTop+endH+finalY;
 const wantedGap=isMobile()?20:Math.max(16,Math.min(64,maskH-endH-16));
 const actualGap=Math.max(0,maskH-contentBottom);
 stage.style.height=(releaseAt+vh-(actualGap-wantedGap))+'px';
 start=stage.offsetTop;
 render();
}
function queue(){if(!raf)raf=requestAnimationFrame(render)}
addEventListener('scroll',queue,{passive:true});
addEventListener('resize',()=>{const w=innerWidth;if(Math.abs(w-lastWidth)>2){lastWidth=w;measure()}},{passive:true});
addEventListener('orientationchange',()=>setTimeout(measure,150));
if(window.visualViewport)window.visualViewport.addEventListener('resize',()=>{clearTimeout(window.__dgV5Resize);window.__dgV5Resize=setTimeout(measure,80)},{passive:true});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);
requestAnimationFrame(()=>requestAnimationFrame(measure));
})();