document.addEventListener('DOMContentLoaded',()=>{
  document.body.classList.add('article-v2');

  const oldHeader=document.querySelector('header.header');
  if(oldHeader){
    oldHeader.outerHTML=`<header class="header"><div class="container header-inner"><a class="logo" href="/"><span>등기로</span><small>현재두 법무사 사무소 · 인천</small></a><nav class="nav"><a href="/">홈</a><a href="/inheritance.html">상속등기</a><a href="/renunciation.html">상속포기·한정승인</a><a href="/corporate.html">법인등기</a><a href="/realestate.html">부동산등기</a><a href="/family.html">가사</a><a href="/posts.html" aria-current="page">법률정보</a></nav><button type="button" class="mobile-menu-btn" id="article-mobile-menu-btn" aria-expanded="false">☰ 메뉴</button><a class="mobile-only" href="tel:0324251500">전화상담</a></div></header><div class="mobile-menu-panel" id="article-mobile-menu-panel" aria-hidden="true"><div class="mobile-menu-grid"><a href="/">홈</a><a href="/inheritance.html">상속등기</a><a href="/renunciation.html">상속포기·한정승인</a><a href="/corporate.html">법인등기</a><a href="/realestate.html">부동산등기</a><a href="/family.html">가사</a><a href="/posts.html">법률정보</a></div><button type="button" class="mobile-menu-close" id="article-mobile-menu-close">메뉴 닫기 ↑</button></div>`;
  }

  const oldCta=document.querySelector('section.cta');
  if(oldCta){
    oldCta.outerHTML=`<section class="contact" id="contact"><div class="container contact-grid"><div><div class="label">CONSULTATION</div><h2>복잡한 등기절차, 등기로에서 확인하세요.</h2><p>상속 · 법인 · 부동산 등 필요한 절차와 준비서류를 확인할 수 있습니다.</p></div><a class="phone" href="tel:0324251500">032-425-1500</a></div></section>`;
  }

  const oldFooter=document.querySelector('footer.footer');
  if(oldFooter){
    oldFooter.outerHTML=`<footer class="footer"><div class="container footer-route-grid"><div><div class="footer-brand">등기로</div><div class="footer-office">현재두 법무사 사무소</div><div class="footer-info"><div><strong>주소</strong> 인천 미추홀구 경원대로 873, 201호(주안동, 인성빌딩) · 인천가정법원 옆</div><div><strong>전화</strong> <a href="tel:0324251500" style="color:#fff;font-weight:800">032-425-1500</a></div></div></div><div class="footer-route"><div class="footer-route-title">찾아오시는 길</div><div class="footer-route-sub">인천가정법원 옆 · 인성빌딩 2층</div><div class="footer-route-list"><div><span>🚇</span><span><b>1호선</b> 주안역·간석역 1번 출구 도보 이용</span></div><div><span>🚇</span><span><b>인천지하철 2호선</b> 석바위시장역 하차 후 석바위 지하상가 5번 출구 도보 이용</span></div><div><span>⏱</span><span><b>도보시간</b> 간석역 약 15분 · 주안역 약 19분 · 석바위시장역 약 12분</span></div></div><div class="footer-route-actions"><a href="https://map.naver.com/p/search/%EC%9D%B8%EC%B2%9C%20%EB%AF%B8%EC%B6%94%ED%99%80%EA%B5%AC%20%EA%B2%BD%EC%9B%90%EB%8C%80%EB%A1%9C%20873" target="_blank" rel="noopener noreferrer">네이버 지도에서 보기 →</a><a href="tel:0324251500">방문문의 032-425-1500</a></div></div></div></footer>`;
  }

  const btn=document.getElementById('article-mobile-menu-btn');
  const panel=document.getElementById('article-mobile-menu-panel');
  const close=document.getElementById('article-mobile-menu-close');
  if(btn&&panel){
    const setOpen=open=>{
      panel.classList.toggle('open',open);
      panel.setAttribute('aria-hidden',open?'false':'true');
      btn.setAttribute('aria-expanded',open?'true':'false');
    };
    btn.addEventListener('click',()=>setOpen(!panel.classList.contains('open')));
    close?.addEventListener('click',()=>setOpen(false));
    panel.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)});
  }

  function escText(v){
    return String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
  }

  async function buildArticleNavigation(){
    const article=document.querySelector('.article');
    if(!article || document.querySelector('.article-prev-next'))return;

    const match=location.pathname.match(/\/posts\/([^/]+)\.html$/i);
    if(!match)return;
    const currentSlug=decodeURIComponent(match[1]);

    try{
      const r=await fetch('/data/posts.json',{cache:'no-store'});
      if(!r.ok)throw new Error('posts.json '+r.status);
      const posts=await r.json();
      if(!Array.isArray(posts) || !posts.length)return;

      const index=posts.findIndex(p=>String(p.slug||'').replace(/\.html$/i,'')===currentSlug);
      if(index<0)return;

      /* posts.json은 최신 글이 앞쪽. 왼쪽 이전 글=시간상 이전(더 오래된 글), 오른쪽 다음 글=더 최근 글 */
      const older=posts[index+1]||null;
      const newer=posts[index-1]||null;

      const nav=document.createElement('nav');
      nav.className='article-prev-next';
      nav.setAttribute('aria-label','법률정보 이전글 다음글');

      const olderHtml=older
        ? `<a class="article-nav-item article-nav-prev" href="/posts/${encodeURIComponent(String(older.slug||'').replace(/\.html$/i,''))}.html"><span class="article-nav-kicker">← 이전 글</span><strong>${escText(older.title)}</strong></a>`
        : `<span class="article-nav-item article-nav-disabled"><span class="article-nav-kicker">← 이전 글</span><strong>이전 글이 없습니다</strong></span>`;

      const newerHtml=newer
        ? `<a class="article-nav-item article-nav-next" href="/posts/${encodeURIComponent(String(newer.slug||'').replace(/\.html$/i,''))}.html"><span class="article-nav-kicker">다음 글 →</span><strong>${escText(newer.title)}</strong></a>`
        : `<span class="article-nav-item article-nav-disabled article-nav-next"><span class="article-nav-kicker">다음 글 →</span><strong>다음 글이 없습니다</strong></span>`;

      nav.innerHTML=`${olderHtml}<a class="article-nav-list" href="/posts.html">법률정보 목록</a>${newerHtml}`;

      const related=article.querySelector('.related');
      if(related){
        related.parentNode.insertBefore(nav,related);
        related.innerHTML='<a class="btn btn-primary" href="tel:0324251500">032-425-1500 상담</a>';
      }else{
        article.appendChild(nav);
      }
    }catch(e){
      console.warn('이전·다음 글 네비게이션을 불러오지 못했습니다.',e);
    }
  }

  buildArticleNavigation();
});
