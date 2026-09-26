(()=>{'use strict';
const q=document.getElementById('inheritance-query'),list=document.getElementById('inheritance-results'),toggle=document.getElementById('inheritance-toggle'),go=document.getElementById('inheritance-search-button');
if(!q||!list||!toggle||!go)return;
const fixed=[
{title:'부동산등기 한눈에 보기',keywords:'부동산등기 인천 소유권이전 필요서류 비용',href:'#documents',type:'메인안내'},
{title:'매매 소유권이전등기',keywords:'매매등기 매도인 매수인 거래신고 취득세',href:'#service-1',type:'업무안내'},
{title:'증여 소유권이전등기',keywords:'증여등기 증여자 수증자 가족간 증여 취득세',href:'#service-2',type:'업무안내'},
{title:'상속 소유권이전등기',keywords:'상속등기 협의분할 피상속인 상속인 제적등본',href:'#service-3',type:'업무안내'},
{title:'이혼 재산분할등기',keywords:'재산분할 협의이혼 재판이혼 아파트 소유권이전',href:'#service-4',type:'업무안내'},
{title:'근저당권 설정·말소',keywords:'근저당 설정 말소 담보 대출 해지증서',href:'#mortgage-guide',type:'업무안내'},
{title:'상속등기 상세안내',keywords:'상속등기 공동상속 단독상속 협의분할',href:'/inheritance.html',type:'핵심안내'},
{title:'상속·증여·매매 등기 필요서류',keywords:'상속 증여 매매 부동산등기 필요서류 준비서류',href:'/posts/naver-224242416419.html',type:'핵심안내'},
{title:'등기권리증 분실 시 해결방법',keywords:'등기권리증 등기필증 분실 확인서면 매매',href:'/posts/sale-real-estate-guide-bvcdri.html',type:'핵심안내'},
{title:'부모·자식 간 부동산 매매',keywords:'부모 자식 가족간 부동산 매매 증여',href:'/posts/naver-224271484086.html',type:'핵심안내'},
{title:'미등기 건물 매매',keywords:'미등기 건물 매매 보존등기',href:'/posts/naver-224250931942.html',type:'핵심안내'},
{title:'신탁등기된 부동산',keywords:'신탁등기 신탁원부 전세 보증금',href:'/posts/naver-224246353949.html',type:'핵심안내'},
{title:'근저당·공장저당 담보설정',keywords:'근저당 공장저당 선박근저당 담보설정',href:'/posts/naver-224254103385.html',type:'핵심안내'},
{title:'취득세 계산',keywords:'취득세 계산기 매매 증여 재산분할',href:'/acquisition-calculator.html',type:'계산기'},
{title:'부동산등기 자주 묻는 질문',keywords:'FAQ 질문 권리증 취득세 가족간매매 증여 매매',href:'#realestate-faq',type:'세부안내'},
{title:'이혼 재산분할 아파트 이전',keywords:'재산분할 이혼 아파트 소유권이전',href:'/posts/naver-224413365255.html',type:'처리사례'},
{title:'전세권자 직접 경매·낙찰',keywords:'전세권 임차인 보증금 경매 낙찰',href:'/posts/naver-224413471424.html',type:'처리사례'},
{title:'가압류·임차권등기 말소',keywords:'가압류 압류 임차권등기 말소',href:'/posts/naver-224413495528.html',type:'처리사례'},
{title:'유언대용신탁 귀속등기',keywords:'유언대용신탁 신탁 귀속등기 자녀',href:'/posts/naver-224411287172.html',type:'처리사례'},
{title:'부모·자식 간 주택 매매 처리사례',keywords:'부모 자식 주택 매매 취득세 취득자금',href:'/posts/naver-224411310050.html',type:'처리사례'}
];
let items=[...fixed];
const fixedHrefs=new Set(fixed.map(x=>x.href));
fetch('/assets/posts.json').then(r=>r.ok?r.json():[]).then(data=>{if(!Array.isArray(data))return;for(const p of data){if(!p||p.category!=='부동산등기')continue;const href=p.href||p.url||'',title=p.title||'';if(title&&href&&!items.some(x=>x.href===href))items.push({title,keywords:title,href,type:'처리사례'});}}).catch(()=>{});
const norm=s=>(s||'').toLowerCase().replace(/\s+/g,'');
function score(x,key){const t=norm(x.title),k=norm(x.keywords),s=norm(x.summary);let n=0;if(t===key)n+=120;else if(t.startsWith(key))n+=90;else if(t.includes(key))n+=70;if(k.includes(key))n+=35;if(s.includes(key))n+=15;if(x.type==='핵심안내')n+=20;return n;}
function matches(x,s){const n=norm(s);return norm(x.title+' '+(x.keywords||'')).includes(n);}
function render(all=false){const s=q.value.trim(),key=norm(s);const a=(all||!s)?items:items.filter(x=>matches(x,s)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order);list.innerHTML=a.slice(0,20).map(x=>'<li><a href="'+x.href+'"><span class="result-type">'+x.type+'</span>'+x.title+'</a></li>').join('')||'<li class="inheritance-empty">검색 결과가 없습니다.</li>';list.classList.add('is-open');q.setAttribute('aria-expanded','true');}
function close(){list.classList.remove('is-open');q.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>list.classList.contains('is-open')?close():render(true));
q.addEventListener('input',()=>render(false));q.addEventListener('focus',()=>{if(q.value.trim())render(false)});
go.addEventListener('click',()=>{const a=list.querySelector('a');if(a)location.href=a.getAttribute('href');else render(false)});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go.click()}if(e.key==='Escape')close()});
document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-finder-inline'))close()});
})();