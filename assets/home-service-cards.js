(()=>{
  function applyHomeServiceCards(){
    if(location.pathname!=='/'&&location.pathname!=='/index.html') return;
    const card=document.querySelector('.quick-item.quick-rich.c4');
    if(!card) return;
    const title=card.querySelector('h3');
    const desc=card.querySelector('p');
    if(title) title.textContent='상속포기·한정승인';
    if(desc) desc.textContent='상속 빚 대응';
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',applyHomeServiceCards);
  else applyHomeServiceCards();
})();
