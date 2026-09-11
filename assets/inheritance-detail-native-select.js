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

  const addStyle=(id,css)=>{
    if(document.getElementById(id)) return;
    const style=document.createElement('style');
    style.id=id;
    style.textContent=css;
    document.head.appendChild(style);
  };

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
      select.addEventListener('change',()=>{ if(select.value) location.href=select.value; });
      wrap.appendChild(select);
      actions.appendChild(wrap);
    }

    addStyle('dg-native-detail-select-style',`
      .dg-native-detail-select-wrap{position:relative;display:inline-flex;min-width:210px;min-height:48px}
      .dg-native-detail-select{width:100%;min-height:48px;padding:0 38px 0 16px;border:1px solid #84c9ed;border-radius:8px;background:#fff;color:#20242b;font:inherit;font-size:15px;font-weight:900;box-shadow:0 8px 18px rgba(54,169,225,.20);appearance:auto;-webkit-appearance:menulist;cursor:pointer}
      @media(max-width:700px){.dg-native-detail-select-wrap{flex:1 1 210px;min-width:0}.dg-native-detail-select{font-size:15px}}
    `);

    if(PATH==='/inheritance.html'){
      const grid=document.querySelector('.dg-inheritance-linkhub-grid');
      if(grid){
        const keywords=['연락두절','미성년자','해외·외국국적','대습상속','상속재산분할'];
        [...grid.querySelectorAll('a')].forEach((card,i)=>{
          if(card.querySelector('.dg-case-head')) return;
          const strong=card.querySelector('strong');
          if(!strong) return;
          strong.textContent=keywords[i]||strong.textContent;
          const caseHead=document.createElement('div');
          caseHead.className='dg-case-head';
          const badge=document.createElement('span');
          badge.className='dg-case-badge';
          badge.textContent='사례';
          strong.before(caseHead);
          caseHead.appendChild(badge);
          caseHead.appendChild(strong);
        });
      }

      addStyle('dg-inheritance-case-card-style',`
        .dg-inheritance-linkhub-grid{grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:12px!important;align-items:stretch!important}
        .dg-inheritance-linkhub-grid a{box-sizing:border-box!important;width:100%!important;min-width:0!important;height:118px!important;min-height:118px!important;padding:18px 16px 16px!important;display:flex!important;flex-direction:column!important;justify-content:flex-start!important;background:#eaf6ff!important;border:1.5px solid #69b8ee!important;border-radius:14px!important}
        .dg-inheritance-linkhub-grid a:hover{border-color:#36a9e1!important;transform:translateY(-2px)!important;box-shadow:0 8px 22px rgba(25,41,68,.08)!important}
        .dg-case-head{display:flex!important;align-items:center!important;gap:7px!important;min-width:0!important;white-space:nowrap!important}
        .dg-case-badge{display:inline-flex!important;align-items:center!important;justify-content:center!important;flex:0 0 auto!important;height:21px!important;padding:0 8px!important;border-radius:999px!important;background:#2fa6ef!important;color:#fff!important;font-size:11px!important;font-weight:800!important;line-height:21px!important;margin:0!important}
        .dg-inheritance-linkhub-grid strong{display:block!important;margin:0!important;color:#24384f!important;font-size:15px!important;font-weight:800!important;line-height:1.35!important;letter-spacing:-.3px!important;white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important}
        .dg-inheritance-linkhub-grid a>span:not(.dg-case-badge){display:block!important;margin-top:12px!important;color:#3f4f63!important;font-size:12px!important;font-weight:700!important;line-height:1.45!important}
        @media(max-width:1000px){.dg-inheritance-linkhub-grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}}
        @media(max-width:700px){.dg-inheritance-linkhub-grid{grid-template-columns:1fr 1fr!important;gap:8px!important}.dg-inheritance-linkhub-grid a{height:108px!important;min-height:108px!important;padding:14px 12px!important}.dg-inheritance-linkhub-grid strong{font-size:13px!important}.dg-case-badge{height:19px!important;padding:0 7px!important;font-size:10px!important;line-height:19px!important}.dg-inheritance-linkhub-grid a>span:not(.dg-case-badge){margin-top:9px!important;font-size:10.5px!important}}
      `);

      const docsTitle=[...document.querySelectorAll('h2')].find(el=>el.textContent.trim()==='필요서류');
      const docsSection=docsTitle&&docsTitle.closest('section');
      if(docsSection && !docsSection.querySelector('.dg-docs-panel')){
        docsSection.innerHTML=`
          <div class="container">
            <div class="dg-docs-panel">
              <h2 class="dg-docs-title">필요서류</h2>
              <p class="dg-docs-desc">업무 유형별 기본 필요서류입니다. 사건 내용과 당사자 구성에 따라 추가서류가 필요할 수 있습니다.</p>
              <div class="dg-docs-grid">
                <article class="dg-docs-card">
                  <div class="dg-docs-head"><span class="dg-docs-badge">망인 서류</span></div>
                  <ul class="dg-docs-list">
                    <li>피상속인 기본증명서(상세)</li>
                    <li>피상속인 가족관계증명서(상세)</li>
                    <li>피상속인 혼인관계증명서(상세)</li>
                    <li>피상속인 입양관계증명서(상세)</li>
                    <li>피상속인 친양자입양관계증명서(상세)</li>
                    <li>피상속인 주민등록말소자초본</li>
                    <li>피상속인 제적등본(출생부터 사망까지)</li>
                  </ul>
                </article>
                <article class="dg-docs-card">
                  <div class="dg-docs-head"><span class="dg-docs-badge">상속인 서류</span></div>
                  <ul class="dg-docs-list">
                    <li>상속인 가족관계증명서(상세)</li>
                    <li>상속인 기본증명서(상세)</li>
                    <li>상속인 주민등록초본</li>
                    <li>상속인 도장</li>
                  </ul>
                  <div class="dg-docs-subhead">협의한 경우</div>
                  <ul class="dg-docs-list dg-docs-list-extra">
                    <li>상속재산분할협의서</li>
                    <li>상속인 전원의 인감증명서</li>
                    <li>상속인 전원의 인감도장</li>
                  </ul>
                  <div class="dg-docs-note">※ 협의분할이 아닌 법정상속등기 등 사건 유형에 따라 일부 서류는 달라질 수 있습니다.</div>
                </article>
              </div>
            </div>
          </div>`;
      }

      addStyle('dg-inheritance-docs-style',`
        .dg-docs-panel{width:min(100%,700px);margin:0 auto;background:#eaf6ff;border:1.5px solid #8bc8ed;border-radius:18px;padding:22px 10px 24px}
        .dg-docs-title{width:100%;max-width:640px;margin:0 auto;font-size:28px;font-weight:900;letter-spacing:-1px;color:#14263f}
        .dg-docs-desc{width:100%;max-width:640px;margin:8px auto 18px;color:#41536a;font-size:13px;font-weight:700;line-height:1.7}
        .dg-docs-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:18px;row-gap:14px;width:100%;max-width:640px;margin:0 auto;align-items:stretch}
        .dg-docs-card{background:#fff;border:1.5px solid #8bc8ed;border-radius:14px;padding:12px 10px;min-width:0;height:100%;display:flex;flex-direction:column}
        .dg-docs-head{display:flex;align-items:center;gap:8px;margin-bottom:10px}
        .dg-docs-badge{display:inline-flex;align-items:center;justify-content:center;min-height:28px;padding:0 11px;border-radius:8px;background:#e7f5ff;border:1px solid #9ed3f2;color:#178ccb;font-size:13px;font-weight:900}
        .dg-docs-list{margin:0;padding-left:18px}
        .dg-docs-list li{padding:7px 0;border-bottom:1px solid #b9d6e8;font-size:13px;line-height:1.4;color:#14263f}
        .dg-docs-list li:last-child{border-bottom:0}
        .dg-docs-subhead{display:inline-flex;align-items:center;align-self:flex-start;min-height:26px;margin:14px 0 4px;padding:0 9px;border-radius:7px;background:#f3f9fd;border:1px solid #b8dcef;color:#2a6f98;font-size:12px;font-weight:900}
        .dg-docs-list-extra{margin-top:0}
        .dg-docs-note{margin-top:12px;padding-top:10px;border-top:1px dashed #abd0e7;color:#4f6073;font-size:12px;font-weight:700}
        @media(max-width:720px){.dg-docs-panel{width:100%;padding:20px 8px 22px}.dg-docs-title,.dg-docs-desc,.dg-docs-grid{max-width:100%}.dg-docs-grid{grid-template-columns:1fr;column-gap:0;row-gap:12px}}
      `);
    }
  };

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',mount);
  else mount();
})();
