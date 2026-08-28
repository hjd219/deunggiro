(()=>{
  const path=location.pathname;
  if(!path.startsWith('/posts/'))return;

  const esc=v=>String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
  const normalize=c=>{
    c=String(c||'').trim();
    if(c.includes('상속포기')||c.includes('한정승인'))return '상속포기·한정승인';
    if(c.includes('상속재산분할'))return '상속재산분할';
    if(c.includes('상속'))return '상속등기';
    if(c.includes('법인'))return '법인등기';
    if(c.includes('부동산'))return '부동산등기';
    if(c.includes('가사'))return '가사';
    return c||'법률정보';
  };
  const copy={
    '상속등기':['상속등기 절차와 준비서류를 확인해드립니다.','상속인·부동산·취득세 등 사건별로 필요한 절차를 확인하세요.'],
    '상속포기·한정승인':['상속포기·한정승인 기한과 준비서류를 확인해드립니다.','3개월 기간과 상속재산·채무 상황에 따라 준비할 내용을 확인하세요.'],
    '상속재산분할':['상속재산분할 분쟁 절차를 확인해드립니다.','협의가 어렵거나 연락두절·협조거부가 있는 경우 진행방법을 확인하세요.'],
    '법인등기':['법인등기 변경사항과 준비서류를 확인해드립니다.','대표이사·상호·목적·본점이전·증자 등 사건별 필요서류를 확인하세요.'],
    '부동산등기':['부동산등기 절차와 준비서류를 확인해드립니다.','매매·증여·근저당·가압류 등 등기 유형별로 필요한 내용을 확인하세요.'],
    '가사':['가사사건 절차와 준비서류를 확인해드립니다.','이혼·개명 등 사건별 진행절차와 필요한 서류를 확인하세요.'],
    '법률정보':['관련 절차와 준비서류를 확인해드립니다.','현재 상황에 맞는 진행방법과 필요한 서류를 확인하세요.']
  };

  async function run(){
    if(document.querySelector('.dg-topic-cta'))return;
    const match=path.match(/\/posts\/([^/]+)\.html$/i);if(!match)return;
    let category='법률정보';
    try{
      const r=await fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'});
      if(r.ok){
        const posts=await r.json();
        const slug=decodeURIComponent(match[1]);
        const me=posts.find(p=>String(p.slug||'').replace(/\.html$/i,'')===slug);
        if(me)category=normalize(me.category);
      }
    }catch(e){}

    if(!document.getElementById('dg-topic-cta-style')){
      const s=document.createElement('style');
      s.id='dg-topic-cta-style';
      s.textContent='.dg-topic-cta{margin:34px 0 8px;padding:24px;border:1px solid #bfe5f8;border-radius:14px;background:#f5fbff}.dg-topic-cta-kicker{font-size:11px;font-weight:900;color:#36a9e1;letter-spacing:.8px}.dg-topic-cta h2{margin:5px 0 8px!important;font-size:24px!important;line-height:1.4!important;letter-spacing:-1px!important}.dg-topic-cta p{margin:0 0 16px!important;color:#5c6875!important;font-size:14px!important}.dg-topic-cta-actions{display:flex;gap:8px;flex-wrap:wrap}.dg-topic-cta a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 16px;border-radius:8px;font-weight:900;text-decoration:none!important}.dg-topic-call{background:#36a9e1;color:#fff!important}.dg-topic-list{background:#fff;color:#20344a!important;border:1px solid #cfdde8}@media(max-width:700px){.dg-topic-cta{padding:19px 16px;margin-top:28px}.dg-topic-cta h2{font-size:20px!important}.dg-topic-cta-actions{display:grid;grid-template-columns:1fr}.dg-topic-cta a{width:100%}}';
      document.head.appendChild(s);
    }

    const [title,desc]=copy[category]||copy['법률정보'];
    const box=document.createElement('section');
    box.className='dg-topic-cta';
    box.setAttribute('aria-label','상담 안내');
    box.innerHTML=`<div class="dg-topic-cta-kicker">CONSULTATION</div><h2>${esc(title)}</h2><p>${esc(desc)}</p><div class="dg-topic-cta-actions"><a class="dg-topic-call" href="tel:0324251500">032-425-1500 전화상담</a><a class="dg-topic-list" href="/posts.html?category=${encodeURIComponent(category)}">같은 분야 글 보기</a></div>`;

    const article=document.querySelector('.article');
    if(!article)return;
    const related=article.querySelector('.related');
    if(related)related.parentNode.insertBefore(box,related);
    else article.appendChild(box);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();
