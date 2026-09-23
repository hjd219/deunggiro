(function(){
 const stage=document.querySelector('.v53-stage');
 const win=document.querySelector('.v53-window');
 const track=document.querySelector('.v53-track');
 const page=track&&track.querySelector('.calc-page-shell');
 if(!stage||!win||!track||!page){document.documentElement.classList.add('dg-home-ready');return}
 let start=0,stopAt=0,finalY=0,lastWidth=innerWidth;
 function measure(){
   const wh=win.clientHeight;
   const pageTop=page.offsetTop;
   const pageH=page.offsetHeight;
   const gap=matchMedia('(max-width:800px)').matches?20:32;
   finalY=wh-gap-(pageTop+pageH);
   stopAt=Math.max(0,wh-finalY);
   start=stage.offsetTop;
   stage.style.height=(stopAt+wh)+'px';
   update();
 }
 function update(){
   const wh=win.clientHeight;
   const p=Math.max(0,(scrollY||0)-start);
   const y=p<stopAt?wh-p:finalY;
   track.style.transform='translate3d(0,'+y+'px,0)';
 }
 addEventListener('scroll',update,{passive:true});
 addEventListener('resize',()=>{if(Math.abs(innerWidth-lastWidth)>2){lastWidth=innerWidth;measure()}},{passive:true});
 addEventListener('orientationchange',()=>setTimeout(measure,150));
 requestAnimationFrame(()=>{measure();document.documentElement.classList.add('dg-home-ready')});
})();