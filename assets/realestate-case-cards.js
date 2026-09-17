(()=>{
  if(location.pathname!=='/realestate.html') return;
  const mount=()=>{
    if(document.querySelector('.dg-realestate-casehub')) return;
    const main=document.querySelector('.re-main');
    if(!main) return;
    const href='/posts.html?tab=case%3A%EB%B6%80%EB%8F%99%EC%82%B0%EB%93%B1%EA%B8%B0';
    const section=document.createElement('section');
    section.className='dg-realestate-casehub';
    section.innerHTML=`<div class="container"><div class="dg-realestate-casehead"><div class="dg-realestate-kicker">실제 처리사례</div><h2>부동산등기 처리사례</h2><p>일반적인 설명보다 실제 진행 과정에서 문제가 된 상황을 중심으로 확인하세요.</p></div><div class="dg-realestate-casegrid">
      <a href="${href}"><div class="dg-realestate-cardhead"><span>사례</span><strong>등기권리증 분실</strong></div><p>권리증이 없는 경우의 이전등기</p></a>
      <a href="${href}"><div class="dg-realestate-cardhead"><span>사례</span><strong>주소 불일치</strong></div><p>오래된 등기의 주소가 다른 경우</p></a>
      <a href="${href}"><div class="dg-realestate-cardhead"><span>사례</span><strong>미등기 건물</strong></div><p>건축물대장이 있는 건물의 보존등기</p></a>
      <a href="${href}"><div class="dg-realestate-cardhead"><span>사례</span><strong>오래된 가압류</strong></div><p>채권이 남아 있지 않은 가압류 말소</p></a>
      <a href="${href}"><div class="dg-realestate-cardhead"><span>사례</span><strong>임차권등기 말소</strong></div><p>오래된 임차권등기를 정리하는 경우</p></a>
    </div></div>`;
    main.insertAdjacentElement('afterend',section);
    const style=document.createElement('style');
    style.textContent=`
      .dg-realestate-casehub{padding:30px 0 42px;background:#eef6fb}
      .dg-realestate-casehead{margin-bottom:16px}.dg-realestate-kicker{color:#2fa6ef;font-size:11px;font-weight:900;margin-bottom:5px}.dg-realestate-casehead h2{margin:0;color:#24384f;font-size:25px;line-height:1.3;letter-spacing:-.8px}.dg-realestate-casehead p{margin:7px 0 0;color:#657487;font-size:13px}
      .dg-realestate-casegrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;align-items:stretch}
      .dg-realestate-casegrid a{box-sizing:border-box;height:118px;padding:18px 16px 16px;display:flex;flex-direction:column;background:#fff;border:1.5px solid #69b8ee;border-radius:14px;text-decoration:none;transition:.18s ease}
      .dg-realestate-casegrid a:hover{border-color:#36a9e1;transform:translateY(-2px);box-shadow:0 8px 22px rgba(25,41,68,.08)}
      .dg-realestate-cardhead{display:flex;align-items:center;gap:7px;white-space:nowrap}.dg-realestate-cardhead span{display:inline-flex;align-items:center;justify-content:center;height:21px;padding:0 8px;border-radius:999px;background:#2fa6ef;color:#fff;font-size:11px;font-weight:800;line-height:21px}.dg-realestate-cardhead strong{color:#24384f;font-size:15px;font-weight:800;line-height:1.35;letter-spacing:-.3px}.dg-realestate-casegrid p{margin:12px 0 0;color:#3f4f63;font-size:12px;font-weight:700;line-height:1.45}
      @media(max-width:1000px){.dg-realestate-casegrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
      @media(max-width:700px){.dg-realestate-casehub{padding:22px 0 32px}.dg-realestate-casehead h2{font-size:22px}.dg-realestate-casegrid{grid-template-columns:1fr 1fr;gap:8px}.dg-realestate-casegrid a{height:108px;padding:14px 12px}.dg-realestate-cardhead strong{font-size:13px}.dg-realestate-cardhead span{height:19px;padding:0 7px;font-size:10px;line-height:19px}.dg-realestate-casegrid p{margin-top:9px;font-size:10.5px}}
    `;
    document.head.appendChild(style);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();