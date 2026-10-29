/* 등기로 공통 상단 메뉴: 가로 배치 + 세로 드롭다운 (2026-10-29) */
(function(){
if(window.__dgUnifiedNav)return;window.__dgUnifiedNav=true;
const groups=[
['상속등기','/inheritance.html',[['상속등기 종합안내','/inheritance.html'],['상속재산분할','/inheritance-division.html'],['연락두절 상속인','/inheritance-missing-heir.html'],['해외거주 상속인','/inheritance-overseas-heir.html'],['미성년자 상속인','/inheritance-minor-heir.html'],['대습상속','/inheritance-substitute-succession.html'],['상속재산분할협의서 작성','/inheritance.html#dg-inherit-agreement'],['상속등기비용 계산기','/acquisition-calculator.html?mode=inherit']]],
['상속포기·한정승인','/renunciation.html',[['상속포기·한정승인 종합안내','/renunciation.html'],['상속포기 전 사망보험금·해지환급금','/renunciation-death-insurance.html'],['사망신고 전 고인 예금 인출','/renunciation-deceased-deposit.html'],['상속포기 후 절차','/renunciation-after-procedure.html'],['한정승인 후 청산절차','/renunciation-limited-acceptance-liquidation.html'],['상속포기·한정승인 비용 계산기','/renunciation-calculator.html']]],
['법인등기','/corporate.html',[['법인등기 종합안내','/corporate.html'],['법인설립','/corporate.html#documents'],['변경등기','/corporate.html#documents'],['자본금증자','/corporate.html#documents'],['회사계속등기','/corporate.html#documents'],['법인등기 비용 계산기','/corporate-calculator.html']]],
['부동산등기','/realestate.html',[['부동산등기 종합안내','/realestate.html'],['매매등기','/realestate.html#documents'],['증여등기','/realestate.html#documents'],['상속등기','/realestate.html#documents'],['이혼 재산분할등기','/realestate.html#documents'],['신탁등기','/realestate.html#trust-guide'],['근저당권 설정·말소','/realestate.html#mortgage-guide'],['취득세 계산기','/acquisition-calculator.html']]],
['가사','/family.html',[['가사 종합안내','/family.html'],['협의이혼·재산분할','/family.html#documents'],['친권·양육권·특별대리인','/family.html#documents'],['성년·미성년후견','/family.html#documents'],['성본변경·개명·친생관계','/family.html#documents'],['이혼합의서 작성','/family.html#dg-divorce-chapter']]],
['편의기능','/posts.html',[['상속 자가진단','/inheritance-self-check.html'],['상속등기비용 계산기','/acquisition-calculator.html?mode=inherit'],['상속포기·한정승인 비용 계산기','/renunciation-calculator.html'],['법인등기 비용 계산기','/corporate-calculator.html'],['취득세 계산기','/acquisition-calculator.html'],['상속재산분할협의서 작성','/inheritance.html#dg-inherit-agreement'],['이혼합의서 작성','/family.html#dg-divorce-chapter'],['블로그·법률정보','/posts.html']]]
];
const style=document.createElement('style');style.textContent=`
body>header{position:fixed!important;top:0!important;left:0!important;right:0!important;z-index:1200!important;overflow:visible!important;background:transparent!important}
body>header .nav{overflow:visible!important}
#dg-global-nav{display:flex;align-items:center;gap:3px}
#dg-global-nav .dg-item{position:relative}
#dg-global-nav .dg-main{display:inline-flex;align-items:center;padding:10px 7px;border:0;background:transparent;color:#fff!important;text-decoration:none;font:800 13px/1.4 -apple-system,BlinkMacSystemFont,"Malgun Gothic",sans-serif;border-radius:7px;white-space:nowrap;cursor:pointer}
#dg-global-nav .dg-item:hover>.dg-main,#dg-global-nav .dg-item:focus-within>.dg-main,#dg-global-nav .dg-item.is-open>.dg-main{background:rgba(26,124,184,.80)!important}
#dg-global-nav .dg-dropdown{display:none;position:absolute;left:0;top:100%;width:280px;max-height:70vh;overflow-y:auto;background:#fff!important;border:1px solid #dce9f1;border-radius:10px;padding:10px;box-shadow:0 15px 35px rgba(12,35,51,.24);z-index:2000}
#dg-global-nav .dg-item.is-open>.dg-dropdown,#dg-global-nav .dg-item:hover>.dg-dropdown,#dg-global-nav .dg-item:focus-within>.dg-dropdown{display:block}
#dg-global-nav .dg-dropdown a{display:block!important;opacity:1!important;visibility:visible!important;-webkit-text-fill-color:#171b23!important;color:#171b23!important;background:#fff!important;border:1px solid transparent;border-radius:7px;text-decoration:none;font:750 13px/1.5 -apple-system,BlinkMacSystemFont,"Malgun Gothic",sans-serif;padding:11px 10px;white-space:normal}
#dg-global-nav .dg-dropdown a:hover,#dg-global-nav .dg-dropdown a:focus-visible{background:#eaf6ff!important;color:#087db7!important;-webkit-text-fill-color:#087db7!important;border-color:#78bce7!important}
@media(max-width:950px){#dg-global-nav{display:none!important} }
#dg-shell-mobile-panel .dg-unified-mobile{margin:14px 0}
.dg-unified-mobile details{border-bottom:1px solid #e5edf2;padding:4px 0}
.dg-unified-mobile summary{cursor:pointer;color:#18364a;font-weight:800;font-size:14px;padding:12px 4px}
.dg-unified-mobile details a{display:block;padding:9px 14px!important;font-size:13px;color:#263c4e;text-decoration:none}
.dg-unified-mobile details a:hover{background:#eaf6ff;color:#087db7}
`;document.head.appendChild(style);
const nav=document.querySelector('body>header nav.menu');if(nav){
 const root=document.createElement('nav');root.id='dg-global-nav';root.setAttribute('aria-label','전체 업무 메뉴');
 const home=document.createElement('a');home.className='dg-main';home.href='/';home.textContent='홈';root.appendChild(home);
 const close=()=>root.querySelectorAll('.dg-item.is-open').forEach(e=>e.classList.remove('is-open'));
 groups.forEach(([label,href,links])=>{
 const item=document.createElement('div');item.className='dg-item';
 const a=document.createElement('a');a.href=href;a.className='dg-main';a.textContent=label+' ▾';item.appendChild(a);
 const dd=document.createElement('div');dd.className='dg-dropdown';
 links.forEach(([name,url])=>{const link=document.createElement('a');link.href=url;link.textContent=name;dd.appendChild(link)});
 item.appendChild(dd);item.addEventListener('mouseenter',()=>{close();item.classList.add('is-open')});
 a.addEventListener('click',e=>{if(e.target===a&&e.detail===0)return;});root.appendChild(item);
 });
 document.addEventListener('pointerdown',e=>{if(!root.contains(e.target))close()});
 window.addEventListener('scroll',close,{passive:true});window.addEventListener('wheel',close,{passive:true});
 nav.replaceWith(root);
}
const mobile=document.getElementById('dg-shell-mobile-panel');if(mobile){
 const area=mobile.querySelector('.dg-mm-body');if(area){
 const section=document.createElement('div');section.className='dg-unified-mobile';
 groups.forEach(([label,href,links])=>{const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent=label;details.appendChild(summary);links.forEach(([name,url])=>{let a=document.createElement('a');a.href=url;a.textContent=name;details.appendChild(a)});section.appendChild(details)});
 const old=area.querySelector('.dg-mm-grid');if(old)old.replaceWith(section);else area.prepend(section);
 }
}
})();