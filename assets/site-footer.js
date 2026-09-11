/* SITE_FOOTER_V1 - 상담영역/푸터 전용. 공통 헤더와 분리 */
(function(){
  if(window.__dgFooterReady) return;
  window.__dgFooterReady=true;

  const current=location.pathname;
  const genericContact={title:'복잡한 등기절차, 등기로에서 확인하세요.',desc:'상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.'};
  const contactByPath={
    '/inheritance.html':{title:'일반적인 상속등기로 해결되지 않는 경우',desc:'상속인이 연락되지 않거나, 미성년자·해외 상속인이 포함된 경우처럼 일반적인 절차로 해결되지 않는 경우에는 가족관계와 현재 상황을 확인한 후 진행방법을 안내합니다.'},
    '/renunciation.html':{title:'상속채무가 복잡하거나 3개월이 지난 경우',desc:'채무 규모가 불분명하거나 후순위 상속인, 미성년자, 특별한정승인처럼 일반적인 상속포기·한정승인만으로 판단하기 어려운 경우에는 상속관계와 채무 상황을 확인한 후 진행방법을 안내합니다.'},
    '/corporate.html':{title:'법인등기 내용이 여러 가지 함께 변경되는 경우',desc:'임원변경과 본점이전, 상호·목적변경, 증자처럼 여러 등기사항이 함께 변경되거나 과밀지역 여부·주주구성에 따라 절차가 달라지는 경우에는 현재 법인상태를 확인한 후 진행방법을 안내합니다.'},
    '/realestate.html':{title:'일반적인 매매·증여등기와 다른 경우',desc:'외국인·재외국민이 포함되거나 신탁부동산, 재산분할, 근저당 설정·말소처럼 확인할 사항이 많은 경우에는 계약관계와 등기상태를 확인한 후 필요한 절차와 서류를 안내합니다.'},
    '/family.html':{title:'가족관계와 이해관계가 복잡한 경우',desc:'미성년자 친권·특별대리인, 성년후견·한정후견, 개명·가족관계등록 정정처럼 당사자 관계에 따라 절차가 달라지는 경우에는 현재 가족관계를 확인한 후 진행방법을 안내합니다.'}
  };
  const contactInfo=contactByPath[current]||genericContact;
  const contact=`<section class="dg-shell-contact" id="contact"><div class="dg-shell-contact-grid"><div class="dg-shell-contact-copy"><h2>${contactInfo.title}</h2><p>${contactInfo.desc}</p></div><a class="dg-shell-phone" href="tel:0324251500">032-425-1500 상담</a></div></section>`;
  const footer=`<footer class="dg-shell-footer"><div class="dg-shell-footer-grid"><div><div class="dg-shell-footer-brand">등기로</div><div class="dg-shell-footer-office">현재두 법무사 사무소</div><div class="dg-shell-footer-info"><div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong> <a href="tel:0324251500">032-425-1500</a></div><div><strong>이메일</strong> <a href="mailto:hjd21@naver.com">hjd21@naver.com</a></div></div><div class="dg-shell-channel-row"><a class="dg-shell-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon naver">N</span>네이버 블로그</a><span class="dg-shell-dot">·</span><a class="dg-shell-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon youtube">▶</span>유튜브</a></div></div><div class="dg-shell-route"><div class="dg-shell-route-title">찾아오시는 길</div><div class="dg-shell-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="dg-shell-route-list"><div class="dg-shell-route-item"><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="dg-shell-route-actions"><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a><a href="tel:0324251500">방문문의 032-425-1500</a></div></div></div><div class="dg-shell-legal"><span>Copyright © 2026 현재두 법무사 사무소</span><nav aria-label="법적 안내"><a href="/privacy.html">개인정보처리방침</a><span>·</span><a href="/disclaimer.html">면책고지</a></nav></div></footer>`;
  const replaceFirst=(selectors,html)=>{for(const s of selectors){const el=document.querySelector(s);if(el){el.outerHTML=html;return true}}return false};

  const managedContactPaths=new Set(['/','/index.html','/posts.html','/inheritance.html','/renunciation.html','/corporate.html','/realestate.html','/family.html','/acquisition-calculator.html','/corporate-calculator.html']);
  const detailNoContactPaths=new Set(['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html']);
  if(managedContactPaths.has(current)){
    if(!replaceFirst(['section.contact','section.cta','section.dg-shell-contact'],contact)) document.body.insertAdjacentHTML('beforeend',contact);
  }else if(!detailNoContactPaths.has(current)&&!document.querySelector('section.contact,section.cta,section.dg-shell-contact')){
    document.body.insertAdjacentHTML('beforeend',contact);
  }
  if(!replaceFirst(['footer.footer','footer.dg-shell-footer'],footer)) document.body.insertAdjacentHTML('beforeend',footer);

  const syncContactCopyWidth=()=>{
    const copy=document.querySelector('.dg-shell-contact-copy');
    if(!copy) return;
    const heading=copy.querySelector('h2');
    const desc=copy.querySelector('p');
    if(!heading||!desc) return;
    desc.style.maxWidth='';
    requestAnimationFrame(()=>{
      const width=Math.ceil(heading.getBoundingClientRect().width);
      if(width>0) desc.style.maxWidth=width+'px';
    });
  };
  syncContactCopyWidth();
  let contactResizeTimer;
  window.addEventListener('resize',()=>{
    clearTimeout(contactResizeTimer);
    contactResizeTimer=setTimeout(syncContactCopyWidth,120);
  });
})();
