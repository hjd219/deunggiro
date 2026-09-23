(function(){
 const stage=document.querySelector('.v53-stage'),win=document.querySelector('.v53-window'),track=document.querySelector('.v53-track'),end=track&&track.querySelector('[data-scroll-end]');
 if(!stage||!win||!track||!end){document.documentElement.classList.add('dg-home-ready');return}
 let start=0,stopAt=0,releaseAt=0,finalY=0,vh=0,lastWidth=innerWidth;
 function measure(){
  vh=Math.round(window.visualViewport?window.visualViewport.height:innerHeight);
  const wh=win.clientHeight,endTop=end.offsetTop,endH=end.offsetHeight,isMobile=matchMedia('(max-width:800px)').matches;
  if(isMobile){finalY=wh-20-(endTop+endH);stopAt=wh-finalY;releaseAt=stopAt+Math.max(120,vh*.12)}
  else{const desiredTop=Math.max(16,Math.min(64,wh-endH-16));finalY=desiredTop-endTop;stopAt=wh-finalY;releaseAt=stopAt+Math.max(260,vh*.35)}
  const finalContentBottom=endTop+endH+finalY;
  const mainFooterGap=isMobile?20:Math.max(16,Math.min(64,wh-endH-16));
  const actualFooterGap=Math.max(0,wh-finalContentBottom);
  stage.style.height=(releaseAt+vh-(actualFooterGap-mainFooterGap))+'px';
  start=stage.offsetTop;update();
 }
 function update(){
  const y=scrollY||0,wh=win.clientHeight,p=Math.max(0,y-start);
  document.body.classList.remove('v55-services','v55-release');document.documentElement.style.setProperty('--v55-release-y','0px');
  if(p<stopAt){track.style.transform='translate3d(0,'+(wh-p)+'px,0)';return}
  track.style.transform='translate3d(0,'+finalY+'px,0)';document.body.classList.add('v55-services');
  if(p>releaseAt){const rise=Math.min(vh,p-releaseAt);document.body.classList.add('v55-release');document.documentElement.style.setProperty('--v55-release-y',(-rise)+'px')}
 }
 addEventListener('scroll',update,{passive:true});
 addEventListener('resize',()=>{if(Math.abs(innerWidth-lastWidth)>2){lastWidth=innerWidth;measure()}},{passive:true});
 addEventListener('orientationchange',()=>setTimeout(measure,150));
 requestAnimationFrame(()=>{measure();document.documentElement.classList.add('dg-home-ready')});
})();