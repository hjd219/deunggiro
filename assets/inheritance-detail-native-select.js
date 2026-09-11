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
    if(actions && !actions.querySelector('.dg-native-detail-select-wrap')){
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
        if(hubContainer){
          hubContainer.style.setProperty('background','transparent','important');
          hubContainer.style.setProperty('background-color','transparent','important');
        }
      }

      const grid=document.querySelector('.dg-inheritance-linkhub-grid');
      if(grid){
        const keywords=['연락두절','미성년자','해외·외국국적','대습상속','상속재산분할'];
        [...grid.querySelectorAll('a')].forEach((card,i)=>{
          if(card.querySelector('.dg-case-head')) return;
          const strong=card.querySelector('strong');
          if(!strong) return;
          strong.textContent=keywords[i]||strong.textContent;
          const head=document.createElement('div');
          head.className='dg-case-head';
          const badge=document.createElement('span');
          badge.className='dg-case-badge';
          badge.textContent='사례';
          strong.before(head);
          head.appendChild(badge);
          head.appendChild(strong);
        });
      }

      const docs=document.querySelector('#documents');
      if(docs){
        const container=docs.querySelector('.container');
        const title=docs.querySelector('.title');
        const desc=docs.querySelector('.desc');
        if(container && title && desc){
          container.innerHTML='';

          const docsWrap=document.createElement('div');
          docsWrap.className='dg-docs-wrap-v3';
          docsWrap.appendChild(title);
          docsWrap.appendChild(desc);

          const docsGrid=document.createElement('div');
          docsGrid.className='docs-grid dg-docs-grid-v2';
          docsGrid.innerHTML=`
            <div class="docs-card dg-docs-card-v2">
              <h3><span class="dg-docs-badge">망인 서류</span></h3>
              <ul>
                <li>피상속인 기본증명서(상세)</li>
                <li>피상속인 가족관계증명서(상세)</li>
                <li>피상속인 혼인관계증명서(상세)</li>
                <li>피상속인 입양관계증명서(상세)</li>
                <li>피상속인 친양자입양관계증명서(상세)</li>
                <li>피상속인 주민등록말소자초본</li>
                <li>피상속인 제적등본(출생부터 사망까지)</li>
              </ul>
            </div>
            <div class="docs-card dg-docs-card-v2">
              <h3><span class="dg-docs-badge">상속인 서류</span></h3>
              <ul>
                <li>상속인 가족관계증명서(상세)</li>
                <li>상속인 기본증명서(상세)</li>
                <li>상속인 주민등록초본</li>
                <li>상속인 도장</li>
              </ul>
              <div class="dg-docs-subhead">협의한 경우</div>
              <ul>
                <li>상속재산분할협의서</li>
                <li>상속인 전원의 인감증명서</li>
                <li>상속인 전원의 인감도장</li>
              </ul>
              <p class="dg-docs-note">※ 협의분할이 아닌 법정상속등기 등 사건 유형에 따라 일부 서류는 달라질 수 있습니다.</p>
            </div>`;
          docsWrap.appendChild(docsGrid);
          container.appendChild(docsWrap);
        }
      }

      if(!document.getElementById('dg-inheritance-case-card-style')){
        const style=document.createElement('style');
        style.id='dg-inheritance-case-card-style';
        style.textContent=`
          html body section.section.dg-inheritance-linkhub,
          html body section.dg-inheritance-linkhub,
          html body .dg-inheritance-linkhub{
            background:#eef6fb!important;
            background-color:#eef6fb!important;
            background-image:none!important;
            border-top:0!important;
            border-bottom:0!important;
            box-shadow:none!important
          }
          html body .dg-inheritance-linkhub::before,
          html body .dg-inheritance-linkhub::after{background:transparent!important;background-image:none!important}
          html body .dg-inheritance-linkhub>.container,
          html body .dg-inheritance-linkhub .container{background:transparent!important;background-color:transparent!important;background-image:none!important}
          .dg-inheritance-linkhub-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:12px!important;align-items:stretch!important}
          .dg-inheritance-linkhub-grid a{box-sizing:border-box!important;width:100%!important;min-width:0!important;height:118px!important;min-height:118px!important;padding:18px 16px 16px!important;display:flex!important;flex-direction:column!important;justify-content:flex-start!important;background:#fff!important;border:1.5px solid #69b8ee!important;border-radius:14px!important}
          .dg-inheritance-linkhub-grid a:hover{border-color:#36a9e1!important;transform:translateY(-2px)!important;box-shadow:0 8px 22px rgba(25,41,68,.08)!important}
          .dg-case-head{display:flex!important;align-items:center!important;gap:7px!important;min-width:0!important;white-space:nowrap!important}
          .dg-case-badge{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;height:21px!important;padding:0 8px!important;border-radius:999px!important;background:#2fa6ef!important;color:#fff!important;font-size:11px!important;font-weight:800!important;line-height:21px!important;margin:0!important}
          .dg-inheritance-linkhub-grid strong{display:block!important;margin:0!important;color:#24384f!important;font-size:15px!important;font-weight:800!important;line-height:1.35!important;letter-spacing:-.3px!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important}
          .dg-inheritance-linkhub-grid a>span:not(.dg-case-badge){display:block!important;margin-top:12px!important;color:#3f4f63!important;font-size:12px!important;font-weight:700!important;line-height:1.45!important}

          .inheritance-pc-lower .docs-section{margin:0!important;padding:22px!important;max-width:none!important;width:100%!important;background:#fff!important;border:1px solid #dfe5ec!important;border-radius:18px!important;box-shadow:0 10px 28px rgba(31,41,55,.045)!important}
          .inheritance-pc-lower .docs-section>.container{width:100%!important;max-width:none!important;padding:0!important}
          #documents .dg-docs-wrap-v3{width:100%!important;max-width:none!important;margin:0!important;background:transparent!important;border:0!important;border-radius:0!important;padding:0!important;box-shadow:none!important}
          #documents .title{max-width:none!important;margin:4px 0 14px!important;font-size:25px!important;line-height:1.3!important;letter-spacing:-1px!important}
          #documents .desc{max-width:none!important;margin:0 0 14px!important;font-size:12px!important;line-height:1.6!important}
          #documents .dg-docs-grid-v2{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;column-gap:18px!important;row-gap:14px!important;width:100%!important;max-width:none!important;margin:0!important;align-items:stretch!important}
          #documents .dg-docs-card-v2{height:100%!important;background:#fff!important;border:1.5px solid #9fd4f3!important;border-radius:14px!important;padding:12px 6px!important;box-shadow:none!important}
          #documents .dg-docs-card-v2 h3{display:block!important;margin:0 0 12px!important;padding:0!important;background:transparent!important;border:0!important;border-radius:0!important;box-shadow:none!important;outline:0!important;font-size:13px!important;line-height:1!important}
          #documents .dg-docs-card-v2 h3::before,#documents .dg-docs-card-v2 h3::after{content:none!important;display:none!important}
          #documents .dg-docs-badge{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:28px!important;padding:0 11px!important;border-radius:8px!important;background:#eef7fd!important;border:1px solid #9fd4f3!important;box-shadow:none!important;outline:none!important;color:#168dca!important;font-size:13px!important;font-weight:900!important;line-height:1!important}
          #documents .dg-docs-card-v2 ul{margin:0!important;padding-left:18px!important;color:#24384f!important;font-size:13px!important;line-height:1.45!important}
          #documents .dg-docs-card-v2 li{margin:0!important;padding:8px 0!important;border:0!important;box-shadow:none!important}
          #documents .dg-docs-card-v2 li+li{border-top:1px solid #b9d6e8!important}
          #documents .dg-docs-subhead{display:inline-flex!important;align-items:center!important;min-height:26px!important;margin:14px 0 4px!important;padding:0 9px!important;border-radius:7px!important;background:#f3f9fd!important;border:1px solid #b8dcef!important;color:#2a6f98!important;font-size:12px!important;font-weight:900!important}
          #documents .dg-docs-note{margin:12px 0 0!important;padding-top:10px!important;border-top:1px dashed #abd0e7!important;color:#4f6073!important;font-size:12px!important;font-weight:700!important;line-height:1.55!important}

          @media(max-width:1000px){.dg-inheritance-linkhub-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
          @media(max-width:700px){
            .dg-inheritance-linkhub-grid{grid-template-columns:1fr 1fr!important;gap:8px!important}
            .dg-inheritance-linkhub-grid a{height:108px!important;min-height:108px!important;padding:14px 12px!important}
            .dg-inheritance-linkhub-grid strong{font-size:13px!important}
            .dg-case-badge{height:19px!important;padding:0 7px!important;font-size:10px!important;line-height:19px!important}
            .dg-inheritance-linkhub-grid a>span:not(.dg-case-badge){margin-top:9px!important;font-size:10.5px!important}
            .inheritance-pc-lower .docs-section{padding:18px!important}
            #documents .dg-docs-grid-v2{grid-template-columns:1fr!important;gap:12px!important;max-width:none!important}
            #documents .title,#documents .desc{max-width:none!important}
          }
        `;
        document.head.appendChild(style);
      }
    }
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
