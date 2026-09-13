/* SITE_FOOTER_V1 - 상담영역/푸터 전용. 공통 헤더와 분리 */
(function(){
  if(window.__dgFooterReady) return;
  window.__dgFooterReady=true;

  const current=location.pathname;
  const genericContact={title:'복잡한 등기절차, 현재두 법무사가 직접 상담!',desc:'상담부터 등기 완료까지, 직접 확인합니다.'};
  const contactInfo=genericContact;
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
