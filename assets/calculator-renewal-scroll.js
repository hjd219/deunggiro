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
   const pageTop=page.offsetTop,pageH=page.offsetHeight;
   const isMobile=matchMedia('(max-width:800px)').matches;
   const gap=isMobile?20:Math.max(16,Math.min(64,wh-pageH-16));
   finalY=wh-gap-(pageTop+pageH);
   stopAt=Math.max(0,wh-finalY);
   releaseAt=stopAt+Math.max(isMobile?120:260,vh*(isMobile?.12:.35));
   stage.style.height=(releaseAt+vh)+'px';
   start=stage.offsetTop;
   update();
 }
 function update(){
   const y=scrollY||0,wh=win.clientHeight,p=Math.max(0,y-start);
   document.body.classList.remove('v55-services','v55-release');
   document.documentElement.style.setProperty('--v55-release-y','0px');
   if(p<stopAt){track.style.transform='translate3d(0,'+(wh-p)+'px,0)';return}
   track.style.transform='translate3d(0,'+finalY+'px,0)';
   document.body.classList.add('v55-services');
   if(p>releaseAt){
     const rise=Math.min(vh,p-releaseAt);
     document.body.classList.add('v55-release');
     document.documentElement.style.setProperty('--v55-release-y',(-rise)+'px');
   }
 }
 addEventListener('scroll',update,{passive:true});
 addEventListener('resize',()=>{if(Math.abs(innerWidth-lastWidth)>2){lastWidth=innerWidth;measure()}},{passive:true});
 addEventListener('orientationchange',()=>setTimeout(measure,150));
 requestAnimationFrame(()=>{measure();document.documentElement.classList.add('dg-home-ready')});
})();