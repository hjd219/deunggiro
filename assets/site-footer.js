/* SITE_FOOTER_COMPACT_V2 - 공통 하단 푸터. 기존/중간 푸터 제거 후 1개만 생성 */
(function(){
  if(window.__dgFooterReady)return;
  window.__dgFooterReady=true;
  const current=location.pathname;

  const style=document.createElement('style');
  style.id='dg-compact-footer-v2';
  style.textContent=`
.dg-shell-footer{background:#0f2d3f!important;color:#e9f2f6!important;padding:24px max(24px,calc((100% - 1180px)/2)) 14px!important;box-sizing:border-box!important}
.dg-shell-footer-grid{display:grid!important;grid-template-columns:1fr 1fr!important;gap:34px!important;align-items:start!important}
.dg-shell-footer-brand{font-size:20px!important;line-height:1.15!important;font-weight:900!important;color:#fff!important;margin:0 0 3px!important}
.dg-shell-footer-office{font-size:12px!important;line-height:1.35!important;font-weight:800!important;color:#d6e5ec!important;margin:0 0 10px!important}
.dg-shell-footer-info{display:grid!important;gap:3px!important;font-size:11px!important;line-height:1.45!important;color:#c7d8e1!important}
.dg-shell-footer-info strong{color:#fff!important;margin-right:5px!important}.dg-shell-footer a{color:inherit!important;text-decoration:none!important}
.dg-shell-channel-row{display:flex!important;align-items:center!important;gap:7px!important;margin-top:9px!important;font-size:11px!important;color:#d6e5ec!important}
.dg-shell-social{display:inline-flex!important;align-items:center!important;gap:5px!important}.dg-shell-social-icon{display:inline-flex!important;align-items:center!important;justify-content:center!important;width:18px!important;height:18px!important;border-radius:4px!important;background:#fff!important;color:#0f2d3f!important;font-size:10px!important;font-weight:900!important}
.dg-shell-route{border-left:1px solid rgba(255,255,255,.15)!important;padding-left:30px!important}.dg-shell-route-title{font-size:18px!important;line-height:1.2!important;font-weight:900!important;color:#fff!important;margin:0 0 3px!important}.dg-shell-route-sub{font-size:11px!important;color:#b9ccd6!important;margin-bottom:8px!important}
.dg-shell-route-list{display:grid!important;gap:3px!important}.dg-shell-route-item{display:flex!important;gap:7px!important;font-size:11px!important;line-height:1.4!important;color:#d0dee5!important}.dg-shell-route-item b{color:#fff!important}
.dg-shell-route-actions{display:flex!important;flex-direction:column!important;align-items:flex-start!important;gap:5px!important;margin-top:9px!important}.dg-shell-route-actions a{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:28px!important;padding:0 10px!important;border:1px solid rgba(255,255,255,.34)!important;border-radius:5px!important;background:transparent!important;color:#fff!important;font-size:10px!important;font-weight:850!important}
.dg-shell-route-actions a:hover,.dg-shell-route-actions a:focus{background:rgba(255,255,255,.08)!important}
.dg-shell-legal{display:flex!important;justify-content:space-between!important;align-items:center!important;gap:15px!important;margin-top:14px!important;padding-top:10px!important;border-top:1px solid rgba(255,255,255,.13)!important;font-size:9px!important;line-height:1.35!important;color:#91a9b5!important}.dg-shell-legal nav{display:flex!important;gap:7px!important;align-items:center!important}
@media(max-width:700px){.dg-shell-footer{padding:20px 18px 12px!important}.dg-shell-footer-grid{grid-template-columns:1fr!important;gap:18px!important}.dg-shell-route{border-left:0!important;border-top:1px solid rgba(255,255,255,.13)!important;padding:15px 0 0!important}.dg-shell-legal{align-items:flex-start!important;flex-direction:column!important;gap:6px!important;margin-top:12px!important}.dg-shell-route-actions{flex-direction:row!important;flex-wrap:wrap!important}}
`;
  document.head.appendChild(style);

  const genericContact={title:'복잡한 등기절차, 현재두 법무사가 직접 상담!',desc:'상담부터 등기 완료까지, 직접 확인합니다.'};
  const contact=`<section class="dg-shell-contact" id="contact"><div class="dg-shell-contact-grid"><div class="dg-shell-contact-copy"><h2>${genericContact.title}</h2><p>${genericContact.desc}</p></div><a class="dg-shell-phone" href="tel:0324251500">032-425-1500 상담</a></div></section>`;
  const footer=`<footer class="dg-shell-footer"><div class="dg-shell-footer-grid"><div><div class="dg-shell-footer-brand">등기로</div><div class="dg-shell-footer-office">현재두 법무사 사무소</div><div class="dg-shell-footer-info"><div><strong>주소</strong>인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong><a href="tel:0324251500">032-425-1500</a></div><div><strong>이메일</strong><a href="mailto:hjd21@naver.com">hjd21@naver.com</a></div></div><div class="dg-shell-channel-row"><a class="dg-shell-social" href="https://blog.naver.com/hjd21" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon">N</span>네이버 블로그</a><span>·</span><a class="dg-shell-social" href="https://youtube.com/channel/UCHs3WtBFAiV8bOsQUB-n-Ew?si=tTUgTZWRKg98bvYa" target="_blank" rel="noopener noreferrer"><span class="dg-shell-social-icon">▶</span>유튜브</a></div></div><div class="dg-shell-route"><div class="dg-shell-route-title">찾아오시는 길</div><div class="dg-shell-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="dg-shell-route-list"><div class="dg-shell-route-item"><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div class="dg-shell-route-item"><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="dg-shell-route-actions"><a href="tel:0324251500">방문문의 032-425-1500</a><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a></div></div></div><div class="dg-shell-legal"><span>Copyright © 2026 현재두 법무사 사무소</span><nav aria-label="법적 안내"><a href="/privacy.html">개인정보처리방침</a><span>·</span><a href="/disclaimer.html">면책고지</a></nav></div></footer>`;

  const managedContactPaths=new Set(['/','/index.html','/posts.html','/inheritance.html','/renunciation.html','/corporate.html','/realestate.html','/family.html','/acquisition-calculator.html','/corporate-calculator.html']);
  const detailNoContactPaths=new Set(['/inheritance-missing-heir.html','/inheritance-overseas-heir.html','/inheritance-minor-heir.html','/inheritance-substitute-succession.html','/inheritance-division.html','/renunciation-after.html','/limited-acceptance-liquidation.html']);
  const replaceFirst=(selectors,html)=>{for(const s of selectors){const el=document.querySelector(s);if(el){el.outerHTML=html;return true}}return false};
  if(managedContactPaths.has(current)){if(!replaceFirst(['section.contact','section.cta','section.dg-shell-contact'],contact))document.body.insertAdjacentHTML('beforeend',contact)}else if(!detailNoContactPaths.has(current)&&!document.querySelector('section.contact,section.cta,section.dg-shell-contact'))document.body.insertAdjacentHTML('beforeend',contact);

  /* 기존/중간/중복 푸터를 모두 제거하고 페이지 맨 마지막에 공통 푸터 하나만 둔다 */
  document.querySelectorAll('footer').forEach(el=>el.remove());
  document.body.insertAdjacentHTML('beforeend',footer);
})();
