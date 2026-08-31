document.addEventListener('DOMContentLoaded',()=>{
  const current=location.pathname;
  const navItems=[['/','홈'],['/inheritance.html','상속등기'],['/renunciation.html','상속포기·한정승인'],['/corporate.html','법인등기'],['/realestate.html','부동산등기'],['/family.html','가사'],['/posts.html','법률정보']];
  const activePath=()=> current.startsWith('/posts/')?'/posts.html':current;
  const navHtml=navItems.map(([href,label])=>`<a href="${href}"${activePath()===href?' aria-current="page"':''}>${label}</a>`).join('');
  const header=`<header class="dg-shell-header"><div class="dg-shell-inner"><a class="dg-shell-logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="dg-shell-nav">${navHtml}</nav><button class="dg-shell-mobile-menu-btn" id="dg-shell-menu-btn" type="button" aria-expanded="false">☰ 메뉴</button><a class="dg-shell-mobile-call" href="tel:0324251500">전화상담</a></div></header><div class="dg-shell-mobile-panel" id="dg-shell-mobile-panel" aria-hidden="true"><div class="dg-shell-mobile-grid">${navHtml}</div><button class="dg-shell-mobile-close" id="dg-shell-menu-close" type="button">메뉴 닫기 ↑</button></div>`;
  const contact=`<section class="dg-shell-contact"><div class="dg-shell-contact-grid"><div><div class="dg-shell-label">CONSULTATION</div><h2>복잡한 등기절차, 등기로에서 확인하세요.</h2><p>상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.</p></div><a class="dg-shell-phone" href="tel:0324251500">032-425-1500</a></div></section>`;
  const footer=`<footer class="dg-shell-footer"><div class="dg-shell-footer-grid"><div><div class="dg-shell-footer-brand">등기로</div><div class="dg-shell-footer-office">현재두 법무사 사무소</div><div class="dg-shell-footer-info"><div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong> <a href="tel:0324251500">032-425-1500</a></div></div><div class="dg-shell-channel-row"><a class="dg-shell-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon naver">N</span>네이버 블로그</a><span class="dg-shell-dot">·</span><a class="dg-shell-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon youtube">▶</span>유튜브</a></div></div><div class="dg-shell-route"><div class="dg-shell-route-title">찾아오시는 길</div><div class="dg-shell-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="dg-shell-route-list"><div class="dg-shell-route-item"><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="dg-shell-route-actions"><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a><a href="tel:0324251500">방문문의 032-425-1500</a></div></div></div></footer>`;

  const replaceFirst=(selectors,html)=>{for(const s of selectors){const el=document.querySelector(s);if(el){el.outerHTML=html;return true}}return false};
  if(!replaceFirst(['header.header','header.dg-shell-header'],header)) document.body.insertAdjacentHTML('afterbegin',header);
  if(!replaceFirst(['section.contact','section.cta','section.dg-shell-contact'],contact)) document.body.insertAdjacentHTML('beforeend',contact);
  if(!replaceFirst(['footer.footer','footer.dg-shell-footer'],footer)) document.body.insertAdjacentHTML('beforeend',footer);

  if(current==='/renunciation.html'){
    const h1=document.querySelector('.service-hero h1,.subhero h1,.hero h1');
    if(h1){h1.style.fontSize='clamp(38px,4.6vw,56px)';h1.style.letterSpacing='-3px';h1.style.whiteSpace='nowrap'}
    const mobile=document.createElement('style');
    mobile.textContent='@media(max-width:700px){.service-hero h1,.subhero h1,.hero h1{font-size:clamp(30px,8vw,40px)!important;letter-spacing:-2px!important;white-space:normal!important}}';
    document.head.appendChild(mobile);
  }

  const btn=document.getElementById('dg-shell-menu-btn'),panel=document.getElementById('dg-shell-mobile-panel'),close=document.getElementById('dg-shell-menu-close');
  if(btn&&panel){const setOpen=o=>{panel.classList.toggle('open',o);panel.setAttribute('aria-hidden',o?'false':'true');btn.setAttribute('aria-expanded',o?'true':'false')};btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));close?.addEventListener('click',()=>setOpen(false));panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)})}
});
