(()=>{
  const header=document.querySelector('header.header');
  if(header){
    header.innerHTML=`<div class="container header-inner">
      <a class="logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a>
      <nav class="nav">
        <a href="/inheritance.html" aria-current="page">상속등기</a>
        <a href="/renunciation.html">상속포기·한정승인</a>
        <a href="/corporate.html">법인등기</a>
        <a href="/realestate.html">부동산등기</a>
        <a href="/family.html">가사</a>
        <a href="/posts.html">법률정보</a>
      </nav>
      <button type="button" class="mobile-menu-btn" id="mobile-menu-btn" aria-controls="mobile-menu-panel" aria-expanded="false">☰ 메뉴</button>
    </div>`;
    header.insertAdjacentHTML('afterend',`<div class="mobile-menu-panel" id="mobile-menu-panel" aria-hidden="true"><div class="mobile-menu-grid"><a href="/">홈</a><a href="/inheritance.html">상속등기</a><a href="/renunciation.html">상속포기·한정승인</a><a href="/corporate.html">법인등기</a><a href="/realestate.html">부동산등기</a><a href="/family.html">가사</a><a href="/posts.html">법률정보</a></div><button type="button" class="mobile-menu-close" id="mobile-menu-close">메뉴 닫기 ↑</button></div>`);
  }

  const footer=document.querySelector('footer.footer');
  if(footer){
    footer.innerHTML=`<div class="container footer-route-grid">
      <div>
        <div class="footer-brand">등기로</div>
        <div class="footer-office">현재두 법무사 사무소</div>
        <div class="footer-info">
          <div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div>
          <div><strong>전화</strong> <a href="tel:0324251500">032-425-1500</a></div>
        </div>
        <div class="footer-channel-row">
          <a class="footer-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="footer-social-icon naver-icon">N</span>네이버 블로그</a>
          <span class="footer-social-dot">·</span>
          <a class="footer-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="footer-social-icon youtube-icon">▶</span>유튜브</a>
        </div>
      </div>
      <div class="footer-route">
        <div class="footer-route-title">찾아오시는 길</div>
        <div class="footer-route-sub">인천가정법원 옆 · 인성빌딩 2층</div>
        <div class="footer-route-list">
          <div><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div>
          <div><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div>
          <div><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div>
        </div>
        <div class="footer-route-actions">
          <a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a>
          <a href="tel:0324251500">방문문의 032-425-1500</a>
        </div>
      </div>
    </div>`;
  }

  const btn=document.getElementById('mobile-menu-btn');
  const panel=document.getElementById('mobile-menu-panel');
  const close=document.getElementById('mobile-menu-close');
  if(btn&&panel){
    const setOpen=(open)=>{
      panel.classList.toggle('open',open);
      panel.setAttribute('aria-hidden',open?'false':'true');
      btn.setAttribute('aria-expanded',open?'true':'false');
      document.body.classList.toggle('mobile-menu-open',open);
    };
    btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
    if(close) close.addEventListener('click',()=>setOpen(false));
    panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
    document.addEventListener('keydown',e=>{if(e.key==='Escape') setOpen(false)});
  }

  /* DETAIL_PROCESS_ICONS_FAQ_V2 */
  const style=document.createElement('style');
  style.textContent=`
    .proc-icon{width:62px!important;height:62px!important;border:1px solid #b9def0!important;border-radius:15px!important;background:#fff!important;display:grid!important;place-items:center!important;margin:0 auto 15px!important;font-size:0!important;box-shadow:0 4px 10px rgba(31,71,104,.035)!important}
    .proc-icon svg{width:34px!important;height:34px!important;display:block!important}
    .faq{display:block!important;margin-top:14px!important}
    .faq-table{width:100%;border-collapse:collapse;background:#fff;font-size:14px;table-layout:fixed}
    .faq-table th,.faq-table td{border:1px solid #d6e2ea;padding:12px 13px;text-align:left;vertical-align:middle;line-height:1.55}
    .faq-table th{width:27%;background:#f1f6f9;color:#17304a;font-weight:900}
    .faq-table td{color:#29445d;background:#fff}
    .faq-kicker{font-size:11px;color:#168dca;font-weight:900;letter-spacing:.04em;margin-bottom:5px}
    @media(max-width:560px){.faq-table{font-size:12.5px}.faq-table th{width:36%;padding:10px}.faq-table td{padding:10px}.proc-icon{width:58px!important;height:58px!important}.proc-icon svg{width:31px!important;height:31px!important}}
  `;
  document.head.appendChild(style);

  const svgs={
    doc:`<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M13 7h20l5 5v29H13z" fill="none" stroke="#3e91ef" stroke-width="2.8" stroke-linejoin="round"/><path d="M33 7v7h6M19 20h12M19 26h9" fill="none" stroke="#3e91ef" stroke-width="2.8" stroke-linecap="round"/><circle cx="33" cy="34" r="6" fill="#3e91ef"/><path d="m30 34 2 2 4-5" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    search:`<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="10" y="8" width="23" height="28" rx="4" fill="none" stroke="#2bbfa6" stroke-width="2.7"/><path d="M16 16h11M16 22h8" fill="none" stroke="#2bbfa6" stroke-width="2.7" stroke-linecap="round"/><circle cx="33" cy="31" r="7" fill="#fff" stroke="#2bbfa6" stroke-width="2.7"/><path d="m38 36 5 5" stroke="#2bbfa6" stroke-width="2.7" stroke-linecap="round"/></svg>`,
    scale:`<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8v29M15 12h18M11 39h26" fill="none" stroke="#d3a31d" stroke-width="2.8" stroke-linecap="round"/><path d="M14 15 8 27h12zm20 0-6 12h12z" fill="none" stroke="#d3a31d" stroke-width="2.4" stroke-linejoin="round"/><path d="M18 8h12" stroke="#596879" stroke-width="3" stroke-linecap="round"/></svg>`,
    people:`<svg viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="16" r="5" fill="#8d62d9"/><circle cx="14" cy="20" r="4" fill="#a47ce4"/><circle cx="34" cy="20" r="4" fill="#a47ce4"/><path d="M16 38c0-7 3-11 8-11s8 4 8 11" fill="#8d62d9"/><path d="M6 38c0-6 3-10 8-10 2 0 3 .4 4 1M42 38c0-6-3-10-8-10-2 0-3 .4-4 1" fill="#a47ce4"/></svg>`,
    home:`<svg viewBox="0 0 48 48" aria-hidden="true"><path d="m7 24 17-14 17 14" fill="none" stroke="#45b96e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 22v18h24V22M20 40V28h8v12" fill="none" stroke="#45b96e" stroke-width="3" stroke-linejoin="round"/><circle cx="36" cy="12" r="5" fill="#45b96e"/><path d="m33.5 12 1.8 1.8 3.2-4" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  };
  const iconFor=(label,index)=>{
    const t=(label||'').replace(/\s/g,'');
    if(/상속등기|등기신청|취득세/.test(t)) return 'home';
    if(/협의|대습자|특별대리인|번역|정리/.test(t)) return 'people';
    if(/방법|판단|심판|인증|상속분|이해상반/.test(t)) return 'scale';
    if(/주소|재산|연락|대리인|사망순서/.test(t)) return 'search';
    if(/상속인|가족|신분|서류/.test(t)) return 'doc';
    return ['doc','search','scale','people','home'][Math.min(index,4)];
  };
  document.querySelectorAll('.process-row .proc').forEach((proc,i)=>{
    const box=proc.querySelector('.proc-icon');
    const label=proc.querySelector('b')?.textContent||'';
    if(box) box.innerHTML=svgs[iconFor(label,i)]||svgs.doc;
  });

  const faqData={
    '/inheritance-missing-heir.html':[
      ['연락이 안 되는 상속인을 빼고 협의할 수 있나요?','협의분할은 원칙적으로 상속인 전원이 참여해야 합니다.'],
      ['연락두절 상태에서도 상속등기를 먼저 할 수 있나요?','사안에 따라 법정지분 등기 등 가능한 방법을 검토할 수 있습니다.'],
      ['주소도 모르는 경우에는 어떻게 하나요?','가족관계와 확인 가능한 주소자료를 먼저 정리한 뒤 송달 및 법원절차 가능성을 검토합니다.']
    ],
    '/inheritance-overseas-heir.html':[
      ['해외 상속인이 한국에 입국해야 하나요?','적절한 위임과 인증서류를 갖추면 국내 입국 없이 진행 가능한 경우가 있습니다.'],
      ['아포스티유가 항상 필요한가요?','서류 종류와 발급국, 인증방식에 따라 달라질 수 있습니다.'],
      ['미국 시민권자와 영주권자의 서류가 같은가요?','국적과 체류자격이 다르면 필요한 주소증명·서명·인증 방식도 달라질 수 있습니다.']
    ],
    '/inheritance-minor-heir.html':[
      ['미성년 상속인이 있으면 특별대리인이 항상 필요한가요?','항상 필요한 것은 아니며 법정대리인과 미성년자 사이의 이해상반 여부를 먼저 판단합니다.'],
      ['부모가 미성년 자녀를 대신해 협의할 수 있나요?','부모의 공동상속 여부와 협의내용에 따라 직접 대리 가능 여부가 달라집니다.'],
      ['특별대리인이 필요하면 등기를 바로 못 하나요?','필요한 경우 먼저 특별대리인 선임결정을 받은 뒤 협의와 등기절차를 진행합니다.']
    ],
    '/inheritance-substitute-succession.html':[
      ['대습상속은 언제 발생하나요?','원래 상속인이 될 사람이 피상속인보다 먼저 사망한 경우 등 법정요건을 확인합니다.'],
      ['대습상속인의 배우자도 상속인이 되나요?','혼인관계와 사망시점 등 법정요건을 함께 확인해야 합니다.'],
      ['대습상속 지분은 어떻게 계산하나요?','피대습자가 받을 상속분을 기준으로 대습상속인들의 지분을 계산합니다.']
    ],
    '/inheritance-division.html':[
      ['상속인 전원이 합의하지 못하면 어떻게 하나요?','가정법원의 상속재산분할심판을 통해 분할방법을 정하는 절차를 검토할 수 있습니다.'],
      ['한 명이 부동산을 받고 다른 상속인에게 돈을 줄 수 있나요?','협의 또는 심판에서 특정 상속인의 단독취득과 정산금 지급 방식이 가능합니다.'],
      ['연락두절 상속인이 있어도 분할심판이 가능한가요?','상속인 전원을 당사자로 특정하여 법원절차를 진행하는 방안을 검토할 수 있습니다.']
    ]
  };
  const rows=faqData[location.pathname];
  if(rows){
    let faqSection=[...document.querySelectorAll('article .section')].find(s=>s.querySelector('.kicker')?.textContent.trim()==='FAQ');
    if(!faqSection){
      faqSection=document.createElement('section');
      faqSection.className='section';
      document.querySelector('article')?.appendChild(faqSection);
    }
    faqSection.innerHTML=`<div class="faq-kicker">FAQ</div><h2>자주 묻는 질문</h2><div class="faq"><table class="faq-table"><tbody>${rows.map(r=>`<tr><th>${r[0]}</th><td>${r[1]}</td></tr>`).join('')}</tbody></table></div>`;
  }
})();