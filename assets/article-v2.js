document.addEventListener('DOMContentLoaded',()=>{
  document.body.classList.add('article-v2');
  if(!document.getElementById('article-nav-style')){
    const style=document.createElement('style');
    style.id='article-nav-style';
    style.textContent=`body.article-v2 .article-prev-next{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;align-items:stretch;margin-top:38px;padding-top:28px;border-top:1px solid #e7edf3}body.article-v2 .article-nav-item{min-height:92px;border:1px solid #dce5ef;border-radius:12px;background:#f8fbfe;text-decoration:none!important;transition:.18s;display:flex;flex-direction:column;justify-content:center;padding:15px 17px;min-width:0}body.article-v2 .article-nav-item strong{display:block;font-size:13px;line-height:1.5;color:#263442;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}body.article-v2 .article-nav-kicker{display:block;margin-bottom:5px;color:#36a9e1;font-size:11px;font-weight:900}body.article-v2 .article-nav-next{text-align:right}body.article-v2 a.article-nav-item:hover{background:#36a9e1!important;border-color:#36a9e1!important;color:#fff!important;transform:translateY(-2px)}body.article-v2 a.article-nav-item:hover *{color:#fff!important}body.article-v2 .article-nav-disabled{opacity:.48;background:#f7f8fa;cursor:default}body.article-v2 .article-prev-next + .related{margin-top:14px!important;padding-top:0!important;border-top:0!important;justify-content:center!important;gap:10px!important;flex-wrap:wrap!important}@media(max-width:700px){body.article-v2 .article-prev-next{grid-template-columns:1fr;gap:8px;margin-top:30px;padding-top:22px}body.article-v2 .article-nav-item{min-height:66px;padding:12px 14px}body.article-v2 .article-nav-next{text-align:left}body.article-v2 .article-prev-next + .related{display:grid!important;grid-template-columns:1fr!important}body.article-v2 .article-prev-next + .related .btn{width:100%!important}}`;
    document.head.appendChild(style);
  }
  const escText=v=>String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
  const categoryOf=c=>{c=String(c||'').trim();if(c==='상속등기')return '상속등기';if(c==='상속포기·한정승인'||c.includes('상속포기')||c.includes('한정승인'))return '상속포기·한정승인';if(c==='법인등기'||c.includes('법인'))return '법인등기';if(c==='부동산등기'||c.includes('부동산'))return '부동산등기';if(c==='가사'||c.includes('가사'))return '가사';return c||'기타'};
  async function buildArticleNavigation(){
    const article=document.querySelector('.article');if(!article||document.querySelector('.article-prev-next'))return;
    const match=location.pathname.match(/\/posts\/([^/]+)\.html$/i);if(!match)return;
    const currentSlug=decodeURIComponent(match[1]);
    try{
      const r=await fetch('/data/posts.json',{cache:'no-store'});if(!r.ok)throw new Error('posts.json '+r.status);
      const posts=await r.json();if(!Array.isArray(posts)||!posts.length)return;
      const current=posts.find(p=>String(p.slug||'').replace(/\.html$/i,'')===currentSlug);if(!current)return;
      const category=categoryOf(current.category),same=posts.filter(p=>categoryOf(p.category)===category);
      const index=same.findIndex(p=>String(p.slug||'').replace(/\.html$/i,'')===currentSlug);if(index<0)return;
      const older=same[index+1]||null,newer=same[index-1]||null;
      const link=p=>`/posts/${encodeURIComponent(String(p.slug||'').replace(/\.html$/i,''))}.html`;
      const nav=document.createElement('nav');nav.className='article-prev-next';nav.setAttribute('aria-label',category+' 법률정보 이전글 다음글');
      nav.innerHTML=(older?`<a class="article-nav-item article-nav-prev" href="${link(older)}"><span class="article-nav-kicker">← 이전 ${category} 글</span><strong>${escText(older.title)}</strong></a>`:`<span class="article-nav-item article-nav-disabled"><span class="article-nav-kicker">← 이전 ${category} 글</span><strong>이전 글이 없습니다</strong></span>`)+(newer?`<a class="article-nav-item article-nav-next" href="${link(newer)}"><span class="article-nav-kicker">다음 ${category} 글 →</span><strong>${escText(newer.title)}</strong></a>`:`<span class="article-nav-item article-nav-disabled article-nav-next"><span class="article-nav-kicker">다음 ${category} 글 →</span><strong>다음 글이 없습니다</strong></span>`);
      const related=article.querySelector('.related');
      const buttons=`<a class="btn btn-border" href="/posts.html?category=${encodeURIComponent(category)}">${category} 법률정보 목록</a><a class="btn btn-primary" href="tel:0324251500">032-425-1500 상담</a>`;
      if(related){related.parentNode.insertBefore(nav,related);related.innerHTML=buttons}else{article.appendChild(nav);const actions=document.createElement('div');actions.className='related';actions.innerHTML=buttons;article.appendChild(actions)}
    }catch(e){console.warn('이전·다음 글 네비게이션을 불러오지 못했습니다.',e)}
  }
  buildArticleNavigation();
});
