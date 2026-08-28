document.addEventListener('DOMContentLoaded',()=>{
  document.body.classList.add('article-v2');
  if(location.pathname==='/posts/incheon-procedure-documents-c8y2vn.html'){
    document.body.classList.add('legacy-post-clean');
    const legacyStyle=document.createElement('style');
    legacyStyle.id='legacy-post-clean-style';
    legacyStyle.textContent=`body.legacy-post-clean .article-body #printPost1{display:block!important;width:100%!important;max-width:100%!important;margin:0!important;padding:0!important;table-layout:auto!important;overflow:visible!important}body.legacy-post-clean .article-body #printPost1>tbody,body.legacy-post-clean .article-body #printPost1>tbody>tr,body.legacy-post-clean .article-body #printPost1>tbody>tr>td.bcc{display:block!important;width:100%!important;max-width:100%!important}body.legacy-post-clean .article-body #printPost1 td.bcr{display:none!important}body.legacy-post-clean .article-body .wrap_rabbit,body.legacy-post-clean .article-body .se-viewer,body.legacy-post-clean .article-body .se-main-container{width:100%!important;max-width:100%!important;margin-left:0!important;margin-right:0!important;padding-left:0!important;padding-right:0!important}body.legacy-post-clean .article-body .se-component-content{width:100%!important;max-width:100%!important;margin-left:0!important;margin-right:0!important;padding-left:0!important;padding-right:0!important}body.legacy-post-clean .article-body .se-module-horizontalLine,body.legacy-post-clean .article-body .se-hr{width:100%!important;max-width:100%!important}body.legacy-post-clean .article-body .se-section-table{width:100%!important;max-width:100%!important}body.legacy-post-clean .article-body .se-section-table img{display:block!important;width:auto!important;max-width:100%!important;height:auto!important;margin:18px 0!important}body.legacy-post-clean .article-body .se-text-paragraph{font-size:16px!important;line-height:1.8!important;white-space:normal!important;margin:0 0 12px!important}body.legacy-post-clean .article-body .se-text-paragraph span{line-height:inherit!important}body.legacy-post-clean .article-body .se-component.se-text{margin-top:26px!important}body.legacy-post-clean .article-body .se-component.se-horizontalLine{margin-top:24px!important}body.legacy-post-clean .article-body .se-module-horizontalLine{padding:18px 0!important}body.legacy-post-clean .article-body .se-text-list{margin:6px 0 14px!important;padding-left:24px!important;font-size:16px!important}body.legacy-post-clean .article-body .se-text-list .se-text-paragraph{margin-bottom:4px!important}@media(max-width:700px){body.legacy-post-clean .article-body .se-text-paragraph{font-size:16px!important;line-height:1.78!important}body.legacy-post-clean .article-body .se-component.se-text{margin-top:22px!important}body.legacy-post-clean .article-body .se-component-content{padding-left:0!important;padding-right:0!important}}`;
    document.head.appendChild(legacyStyle);
  }
  if(!document.getElementById('article-nav-style')){
    const style=document.createElement('style');
    style.id='article-nav-style';
    style.textContent=`body.article-v2 .article-prev-next{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;align-items:stretch;margin-top:38px;padding-top:28px;border-top:1px solid #e7edf3}body.article-v2 .article-nav-item{min-height:92px;border:1px solid #dce5ef;border-radius:12px;background:#f8fbfe;text-decoration:none!important;transition:.18s;display:flex;flex-direction:column;justify-content:center;padding:15px 17px;min-width:0}body.article-v2 .article-nav-item strong{display:block;font-size:13px;line-height:1.5;color:#263442;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}body.article-v2 .article-nav-kicker{display:block;margin-bottom:5px;color:#36a9e1;font-size:11px;font-weight:900}body.article-v2 .article-nav-next{text-align:right}body.article-v2 a.article-nav-item:hover{background:#36a9e1!important;border-color:#36a9e1!important;color:#fff!important;transform:translateY(-2px)}body.article-v2 a.article-nav-item:hover *{color:#fff!important}body.article-v2 .article-nav-disabled{opacity:.48;background:#f7f8fa;cursor:default}@media(max-width:700px){body.article-v2 .article-prev-next{grid-template-columns:1fr;gap:8px;margin-top:30px;padding-top:22px}body.article-v2 .article-nav-item{min-height:66px;padding:12px 14px}body.article-v2 .article-nav-next{text-align:left}}`;
    document.head.appendChild(style);
  }
  const escText=v=>String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
  const categoryOf=c=>{c=String(c||'').trim();if(c==='상속등기')return '상속등기';if(c==='상속포기·한정승인'||c.includes('상속포기')||c.includes('한정승인'))return '상속포기·한정승인';if(c==='법인등기'||c.includes('법인'))return '법인등기';if(c==='부동산등기'||c.includes('부동산'))return '부동산등기';if(c==='가사'||c.includes('가사'))return '가사';return c||'기타'};
  function removeLegacyActions(article){
    article.querySelectorAll('.related').forEach(el=>{
      const text=(el.textContent||'').replace(/\s+/g,' ');
      if(text.includes('법률정보 목록')||text.includes('032-425-1500 상담'))el.remove();
    });
  }
  async function buildArticleNavigation(){
    const article=document.querySelector('.article');if(!article)return;
    removeLegacyActions(article);
    const existing=[...article.querySelectorAll('.article-prev-next')];
    existing.slice(1).forEach(el=>el.remove());
    if(existing.length)return;
    if(article.dataset.navBuilding==='1')return;
    article.dataset.navBuilding='1';
    const match=location.pathname.match(/\/posts\/([^/]+)\.html$/i);if(!match){delete article.dataset.navBuilding;return;}
    const currentSlug=decodeURIComponent(match[1]);
    try{
      const r=await fetch('/data/posts.json',{cache:'no-store'});if(!r.ok)throw new Error('posts.json '+r.status);
      const posts=await r.json();if(!Array.isArray(posts)||!posts.length){delete article.dataset.navBuilding;return;}
      const current=posts.find(p=>String(p.slug||'').replace(/\.html$/i,'')===currentSlug);if(!current){delete article.dataset.navBuilding;return;}
      const category=categoryOf(current.category),same=posts.filter(p=>categoryOf(p.category)===category).sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
      const index=same.findIndex(p=>String(p.slug||'').replace(/\.html$/i,'')===currentSlug);if(index<0){delete article.dataset.navBuilding;return;}
      const older=same[index+1]||null,newer=same[index-1]||null;
      const link=p=>`/posts/${encodeURIComponent(String(p.slug||'').replace(/\.html$/i,''))}.html`;
      const nav=document.createElement('nav');nav.className='article-prev-next';nav.setAttribute('aria-label',category+' 법률정보 이전글 다음글');
      nav.innerHTML=(older?`<a class="article-nav-item article-nav-prev" href="${link(older)}"><span class="article-nav-kicker">← 이전 ${category} 글</span><strong>${escText(older.title)}</strong></a>`:`<span class="article-nav-item article-nav-disabled"><span class="article-nav-kicker">← 이전 ${category} 글</span><strong>이전 글이 없습니다</strong></span>`)+(newer?`<a class="article-nav-item article-nav-next" href="${link(newer)}"><span class="article-nav-kicker">다음 ${category} 글 →</span><strong>${escText(newer.title)}</strong></a>`:`<span class="article-nav-item article-nav-disabled article-nav-next"><span class="article-nav-kicker">다음 ${category} 글 →</span><strong>다음 글이 없습니다</strong></span>`);
      const related=article.querySelector('.related');
      if(related)related.parentNode.insertBefore(nav,related);else article.appendChild(nav);
      removeLegacyActions(article);
    }catch(e){delete article.dataset.navBuilding;console.warn('이전·다음 글 네비게이션을 불러오지 못했습니다.',e)}
  }
  buildArticleNavigation();
});
