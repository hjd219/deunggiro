(()=>{
  function applyHomeServiceCards(){
    if(location.pathname!=='/'&&location.pathname!=='/index.html') return;
    const card=document.querySelector('.quick-item.quick-rich.c4');
    if(card){
      const title=card.querySelector('h3');
      const desc=card.querySelector('p');
      if(title) title.textContent='상속포기·한정승인';
      if(desc) desc.textContent='상속 빚 대응';
    }

    // 메인 히어로의 중복 업무 바로가기 태그 제거
    const tags=document.querySelector('.hero .tags');
    if(tags) tags.remove();

    // iOS 모바일에서 페이지 하단을 지나 계속 끌려 내려가는 현상 방지
    if(!document.getElementById('dg-mobile-bottom-scroll-fix')){
      const style=document.createElement('style');
      style.id='dg-mobile-bottom-scroll-fix';
      style.textContent=`
        @media(max-width:800px){
          html,body{
            height:auto!important;
            min-height:0!important;
            max-height:none!important;
            overflow-x:hidden!important;
            overscroll-behavior-y:none!important;
          }
          body.home{
            overflow-y:auto!important;
          }
          .dg-shell-footer{
            margin-bottom:0!important;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',applyHomeServiceCards);
  else applyHomeServiceCards();
})();
