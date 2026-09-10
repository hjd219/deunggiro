/* DETAIL_DROPDOWN_V1 */
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.dg-detail-menu').forEach(menu=>{
    const btn=menu.querySelector('.dg-detail-menu-toggle');
    const list=menu.querySelector('.dg-detail-menu-list');
    if(!btn||!list)return;
    const close=()=>{menu.classList.remove('open');btn.setAttribute('aria-expanded','false')};
    btn.addEventListener('click',e=>{
      e.preventDefault();
      const open=!menu.classList.contains('open');
      document.querySelectorAll('.dg-detail-menu.open').forEach(other=>{
        if(other!==menu){other.classList.remove('open');const b=other.querySelector('.dg-detail-menu-toggle');if(b)b.setAttribute('aria-expanded','false')}
      });
      menu.classList.toggle('open',open);
      btn.setAttribute('aria-expanded',open?'true':'false');
    });
    list.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
    document.addEventListener('click',e=>{if(!menu.contains(e.target))close()});
    document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
  });
});
