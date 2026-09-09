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
})();