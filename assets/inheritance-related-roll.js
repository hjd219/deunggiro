/* AUTO_SEQUENTIAL_RELATED_V3 */
(function(){
  const box=document.getElementById('auto-related-posts');
  if(!box) return;
  const category=box.dataset.category;
  const badge=box.dataset.badge || category;
  const esc=s=>String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
  let posts=[], rowIndex=0, nextIndex=0, timer=null, paused=false;

  function itemHtml(p){
    return '<span class="related-badge">'+esc(badge)+'</span><span class="related-title seq-roll-title">'+esc(p.title)+'</span><span class="related-arrow">→</span>';
  }
  function hrefFor(p){ return '/posts/'+encodeURIComponent(p.slug)+'.html'; }

  function initialRender(){
    const count=Math.min(4,posts.length);
    box.innerHTML='';
    for(let i=0;i<count;i++){
      const a=document.createElement('a');
      a.href=hrefFor(posts[i]);
      a.innerHTML=itemHtml(posts[i]);
      box.appendChild(a);
    }
    nextIndex=count;
    rowIndex=0;
  }

  function rollOne(){
    if(paused || posts.length<=4) return;
    const rows=box.querySelectorAll('a');
    if(!rows.length) return;
    const row=rows[rowIndex % rows.length];
    const title=row.querySelector('.seq-roll-title');
    const p=posts[nextIndex % posts.length];
    if(!title) return;
    title.classList.remove('seq-roll-in');
    title.classList.add('seq-roll-out');
    setTimeout(()=>{
      row.href=hrefFor(p);
      title.textContent=p.title;
      title.classList.remove('seq-roll-out');
      void title.offsetWidth;
      title.classList.add('seq-roll-in');
      nextIndex=(nextIndex+1)%posts.length;
      rowIndex=(rowIndex+1)%rows.length;
    },280);
  }

  function play(){
    if(posts.length<=4) return;
    clearInterval(timer);
    timer=setInterval(rollOne,3000);
  }
  function stop(){ if(timer){ clearInterval(timer); timer=null; } }

  fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'})
    .then(r=>{if(!r.ok) throw new Error('posts'); return r.json();})
    .then(data=>{
      posts=data.filter(p=>p.category===category).sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
      if(!posts.length) return;
      initialRender();
      play();
      box.addEventListener('mouseenter',()=>{paused=true; stop();});
      box.addEventListener('mouseleave',()=>{paused=false; play();});
    })
    .catch(()=>{});
})();
