(()=>{
  const PATH=location.pathname;
  const items=[
    ['/inheritance-missing-heir.html','연락두절 상속인'],
    ['/inheritance-minor-heir.html','미성년 상속인'],
    ['/inheritance-overseas-heir.html','해외거주·외국인 상속인'],
    ['/inheritance-substitute-succession.html','대습상속'],
    ['/inheritance-division.html','상속재산분할']
  ];
  const allowed=new Set(['/inheritance.html',...items.map(([p])=>p)]);
  if(!allowed.has(PATH)) return;

  const mount=()=>{
    const actions=document.querySelector('.subhero .buttons,.subhero .actions,.hero .buttons,.hero .actions');
    if(!actions || actions.querySelector('.dg-native-detail-select-wrap')) return;

    const old=[...actions.querySelectorAll('a,button,select')].find(el=>el.textContent.includes('상속등기 세부안내'));
    if(old && !old.classList.contains('dg-native-detail-select')) old.remove();

    const wrap=document.createElement('label');
    wrap.className='dg-native-detail-select-wrap';
    const select=document.createElement('select');
    select.className='dg-native-detail-select';
    select.setAttribute('aria-label','상속등기 세부안내');

    const head=document.createElement('option');
    head.value=''; head.textContent='상속등기 세부안내'; head.selected=true;
    select.appendChild(head);

    items.forEach(([href,label])=>{
      const o=document.createElement('option');
      o.value=href; o.textContent=label;
      select.appendChild(o);
    });

    select.addEventListener('change',()=>{
      if(select.value) location.href=select.value;
    });
    wrap.appendChild(select);
    actions.appendChild(wrap);

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
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
