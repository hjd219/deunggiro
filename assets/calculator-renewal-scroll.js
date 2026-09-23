(function(){
 const stage=document.querySelector('.v53-stage');
 const win=document.querySelector('.v53-window');
 const track=document.querySelector('.v53-track');
 const page=track&&track.querySelector('.calc-page-shell');
 if(!stage||!win||!track||!page){document.documentElement.classList.add('dg-home-ready');return}

 let start=0,stopAt=0,releaseAt=0,finalY=0,vh=0,lastWidth=innerWidth;

 function measure(){
  vh=Math.round(window.visualViewport?window.visualViewport.height:innerHeight);
  const wh=win.clientHeight;
  const pageBottom=page.offsetTop+page.offsetHeight;
  const mobile=matchMedia('(max-width:800px)').matches;
  const gap=mobile?20:64;

  /* One rule only: move until the real calculator bottom reaches the fixed gap. */
  finalY=wh-gap-pageBottom;
  stopAt=Math.max(0,wh-finalY);

  /* Keep the completed calculator still briefly, then release the whole fixed scene for footer. */
  const hold=mobile?Math.max(120,vh*.12):Math.max(260,vh*.35);
  releaseAt=stopAt+hold;
  stage.style.height=releaseAt+'px';
  start=stage.offsetTop;
  update();
 }

 function update(){
  const p=Math.max(0,(scrollY||0)-start);
  const wh=win.clientHeight;

  document.body.classList.remove('v55-services','v55-release');
  document.documentElement.style.setProperty('--v55-release-y','0px');

  if(p<stopAt){
   track.style.transform='translate3d(0,'+(wh-p)+'px,0)';
   return;
  }

  track.style.transform='translate3d(0,'+finalY+'px,0)';
  document.body.classList.add('v55-services');

  if(p>releaseAt){
   const rise=Math.min(vh,p-releaseAt);
   document.body.classList.add('v55-release');
   document.documentElement.style.setProperty('--v55-release-y',(-rise)+'px');
  }
 }

 addEventListener('scroll',update,{passive:true});
 addEventListener('resize',()=>{
  if(Math.abs(innerWidth-lastWidth)>2){lastWidth=innerWidth;measure()}
 },{passive:true});
 addEventListener('orientationchange',()=>setTimeout(measure,150));
 if(window.visualViewport){
  let t=0;
  window.visualViewport.addEventListener('resize',()=>{
   clearTimeout(t);t=setTimeout(measure,80);
  },{passive:true});
 }
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
  measure();
  document.documentElement.classList.add('dg-home-ready');
 }));
})();