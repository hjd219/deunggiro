(()=>{
  const PATH=location.pathname;
  const inheritanceItems=[
    ['/inheritance-missing-heir.html','연락두절 상속인'],
    ['/inheritance-minor-heir.html','미성년 상속인'],
    ['/inheritance-overseas-heir.html','해외거주·외국인 상속인'],
    ['/inheritance-substitute-succession.html','대습상속'],
    ['/inheritance-division.html','상속재산분할']
  ];
  const renunciationItems=[
    ['/renunciation-after.html','상속포기 후 절차'],
    ['/limited-acceptance-liquidation.html','한정승인 후 청산절차']
  ];
  const inheritanceAllowed=new Set(['/inheritance.html',...inheritanceItems.map(([p])=>p)]);
  const renunciationAllowed=new Set(['/renunciation.html',...renunciationItems.map(([p])=>p)]);
  const isInheritance=inheritanceAllowed.has(PATH);
  const isRenunciation=renunciationAllowed.has(PATH);
  if(!isInheritance && !isRenunciation) return;
  const items=isRenunciation?renunciationItems:inheritanceItems;
  const selectLabel=isRenunciation?'상속포기·한정승인 세부안내':'상속등기 세부안내';

  const mount=()=>{
    const actions=document.querySelector('.subhero .buttons,.subhero .actions,.hero .buttons,.hero .actions');
    if(actions && !actions.querySelector('.dg-native-detail-select-wrap')){
      const old=[...actions.querySelectorAll('a,button,select')].find(el=>el.textContent.includes(selectLabel));
      if(old && !old.classList.contains('dg-native-detail-select')) old.remove();

      const wrap=document.createElement('label');
      wrap.className='dg-native-detail-select-wrap';
      const select=document.createElement('select');
      select.className='dg-native-detail-select';
      select.setAttribute('aria-label',selectLabel);

      const head=document.createElement('option');
      head.value=''; head.textContent=selectLabel; head.selected=true;
      select.appendChild(head);

      items.forEach(([href,label])=>{
        const o=document.createElement('option');
        o.value=href; o.textContent=label;
        select.appendChild(o);
      });

      select.addEventListener('change',()=>{
        if(select.value) location.href=select.value;
        else select.selectedIndex=0;
      });
      wrap.appendChild(select);
      actions.appendChild(wrap);
    }

    if(!document.getElementById('dg-native-detail-select-style')){
      const style=document.createElement('style');
      style.id='dg-native-detail-select-style';
      style.textContent=`
        .dg-native-detail-select-wrap{position:relative;display:inline-flex;min-width:210px;min-height:48px}
        .dg-native-detail-select{width:100%;min-height:48px;padding:0 38px 0 16px;border:1px solid #84c9ed;border-radius:8px;background:#fff;color:#20242b;font:inherit;font-size:15px;font-weight:900;box-shadow:0 8px 18px rgba(54,169,225,.20);appearance:auto;-webkit-appearance:menulist;cursor:pointer}
        @media(max-width:700px){.dg-native-detail-select-wrap{flex:1 1 210px;min-width:0}.dg-native-detail-select{font-size:15px}}
      `;
      document.head.appendChild(style);
    }

    if(PATH==='/inheritance.html'){
      const hub=document.querySelector('.dg-inheritance-linkhub');
      if(hub){
        hub.classList.remove('white');
        hub.style.setProperty('background','#eef6fb','important');
        hub.style.setProperty('background-color','#eef6fb','important');
        hub.style.setProperty('background-image','none','important');
        hub.style.setProperty('border-top','0','important');
        hub.style.setProperty('border-bottom','0','important');
        hub.style.setProperty('box-shadow','none','important');
        const hubContainer=hub.querySelector('.container');
        if(hubContainer){hubContainer.style.setProperty('background','transparent','important');hubContainer.style.setProperty('background-color','transparent','important');}
      }
    }
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();