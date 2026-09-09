(()=>{
const paths=['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html'];
if(!paths.includes(location.pathname))return;

const init=()=>{
  const sidebar=document.querySelector('.layout>.sidebar');
  const card=sidebar?.querySelector('.side-card');
  const layout=document.querySelector('.layout');
  if(!sidebar||!card||!layout)return;

  let startY=0,left=0,width=0,layoutBottom=0;
  const imp=(el,p,v)=>el.style.setProperty(p,v,'important');
  const del=(el,p)=>el.style.removeProperty(p);

  const mobile=()=>innerWidth<=900;

  const clearCard=()=>{
    ['position','top','left','right','bottom','width','margin','transform'].forEach(p=>del(card,p));
  };

  const measure=()=>{
    if(mobile()){
      clearCard();
      return;
    }
    imp(sidebar,'display','block');
    imp(sidebar,'position','relative');
    imp(sidebar,'top','auto');
    imp(sidebar,'align-self','stretch');
    imp(sidebar,'height','auto');
    imp(sidebar,'overflow','visible');
    clearCard();
    imp(card,'position','relative');
    imp(card,'top','0');
    imp(card,'left','0');
    imp(card,'width','100%');
    const sr=sidebar.getBoundingClientRect();
    const lr=layout.getBoundingClientRect();
    startY=scrollY+sr.top;
    left=sr.left;
    width=sr.width;
    layoutBottom=scrollY+lr.bottom;
  };

  const follow=()=>{
    if(mobile()){
      clearCard();
      return;
    }
    const top=92;
    const y=scrollY;
    const cardH=card.offsetHeight;
    const maxTop=Math.max(startY,layoutBottom-cardH-12);

    if(y+top<=startY){
      imp(card,'position','relative');
      imp(card,'top','0');
      imp(card,'left','0');
      imp(card,'width','100%');
    }else if(y+top>=maxTop){
      imp(card,'position','absolute');
      imp(card,'top',Math.max(0,maxTop-startY)+'px');
      imp(card,'left','0');
      imp(card,'width','100%');
    }else{
      imp(card,'position','fixed');
      imp(card,'top',top+'px');
      imp(card,'left',left+'px');
      imp(card,'width',width+'px');
    }
  };

  const refresh=()=>{measure();follow();};
  addEventListener('scroll',follow,{passive:true});
  addEventListener('resize',refresh);
  if(document.fonts?.ready)document.fonts.ready.then(refresh);
  setTimeout(refresh,100);
  setTimeout(refresh,700);
  refresh();
};

if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
else init();
})();