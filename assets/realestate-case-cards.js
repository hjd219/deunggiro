(()=>{
  if(location.pathname!=='/realestate.html') return;
  const mount=()=>{
    if(document.querySelector('.dg-realestate-casehub')) return;
    const main=document.querySelector('.re-main');
    if(!main) return;
    const section=document.createElement('section');
    section.className='dg-realestate-casehub';
    section.innerHTML=`<div class="container"><div class="dg-realestate-casehead"><h2>부동산등기 이런 경우도 확인하세요</h2><p>실제로 진행한 부동산등기 처리사례를 바로 확인하세요.</p></div><div class="dg-realestate-casegrid">
      <a href="/posts/naver-224413365255.html"><div class="dg-realestate-cardhead"><span>사례</span><strong>이혼 재산분할 아파트 이전</strong></div><p>이혼 재산분할을 원인으로 소유권이전등기를 진행한 사례</p></a>
      <a href="/posts/naver-224413471424.html"><div class="dg-realestate-cardhead"><span>사례</span><strong>전세권자 직접 경매·낙찰</strong></div><p>보증금을 받지 못해 직접 경매신청 후 낙찰받은 사례</p></a>
      <a href="/posts/naver-224413495528.html"><div class="dg-realestate-cardhead"><span>사례</span><strong>가압류·임차권등기 말소</strong></div><p>오래된 가압류와 임차권등기명령을 말소한 사례</p></a>
      <a href="/posts/naver-224411287172.html"><div class="dg-realestate-cardhead"><span>사례</span><strong>유언대용신탁 귀속등기</strong></div><p>신탁 설정 후 특정 자녀에게 부동산을 귀속등기한 사례</p></a>
      <a href="/posts/naver-224411310050.html"><div class="dg-realestate-cardhead"><span>사례</span><strong>부모·자식 간 주택 매매</strong></div><p>취득세와 취득자금까지 소명하며 이전등기한 사례</p></a>
    </div></div>`;
    main.insertAdjacentElement('afterend',section);
    const style=document.createElement('style');
    style.textContent=`
      .dg-realestate-casehub{padding:30px 0 42px;background:#eef6fb}
      .dg-realestate-casehead{margin-bottom:16px}.dg-realestate-casehead h2{margin:7px 0 10px;color:#24384f;font-size:36px;font-weight:900;line-height:1.3;letter-spacing:-2px}.dg-realestate-casehead p{margin:0 0 34px;color:#657487;font-size:13px;line-height:1.6}
      .dg-realestate-casegrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;align-items:stretch}
      .dg-realestate-casegrid a{box-sizing:border-box;min-width:0;height:132px;padding:18px 16px 16px;display:flex;flex-direction:column;background:#fff;border:1.5px solid #69b8ee;border-radius:14px;text-decoration:none;transition:.18s ease;overflow:hidden}
      .dg-realestate-casegrid a:hover{border-color:#36a9e1;transform:translateY(-2px);box-shadow:0 8px 22px rgba(25,41,68,.08)}
      .dg-realestate-cardhead{display:flex;align-items:flex-start;gap:7px;min-width:0}.dg-realestate-cardhead span{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;height:21px;padding:0 8px;border-radius:999px;background:#2fa6ef;color:#fff;font-size:11px;font-weight:800;line-height:21px}.dg-realestate-cardhead strong{display:block;min-width:0;color:#24384f;font-size:14px;font-weight:800;line-height:1.35;letter-spacing:-.45px;white-space:normal;word-break:keep-all;overflow-wrap:break-word}.dg-realestate-casegrid p{margin:10px 0 0;color:#3f4f63;font-size:11.5px;font-weight:700;line-height:1.45;word-break:keep-all}
      @media(max-width:1000px){.dg-realestate-casegrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
      @media(max-width:700px){.dg-realestate-casehub{padding:22px 0 32px}.dg-realestate-casehead h2{font-size:30px;letter-spacing:-1.4px}.dg-realestate-casehead p{margin-bottom:24px}.dg-realestate-casegrid{grid-template-columns:1fr 1fr;gap:8px}.dg-realestate-casegrid a{height:122px;padding:14px 12px}.dg-realestate-cardhead strong{font-size:12.5px}.dg-realestate-cardhead span{height:19px;padding:0 7px;font-size:10px;line-height:19px}.dg-realestate-casegrid p{margin-top:8px;font-size:10.5px}}
    `;
    document.head.appendChild(style);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();