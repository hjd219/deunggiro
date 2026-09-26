(()=>{'use strict';
const q=document.getElementById('inheritance-query'),list=document.getElementById('inheritance-results'),toggle=document.getElementById('inheritance-toggle'),go=document.getElementById('inheritance-search-button');
if(!q||!list||!toggle||!go)return;
const fixed=[
{title:'협의이혼 절차 총정리',keywords:'협의이혼 절차 이혼합의서 숙려기간',href:'/posts/naver-224258629169.html',type:'핵심안내'},
{title:'친권자 변경 기준',keywords:'친권자 변경 공동친권 단독친권',href:'/posts/naver-224269144558.html',type:'핵심안내'},
{title:'성년후견·한정후견 총정리',keywords:'치매 고령 부모 성년후견 한정후견 임의후견',href:'/posts/naver-224254351514.html',type:'핵심안내'},
{title:'개명신청 절차·준비서류',keywords:'개명 신청 절차 준비서류 허가조건 기각사유',href:'/posts/naver-224254656540.html',type:'관련 법률정보'},
{title:'성본변경 허가 신청',keywords:'성본변경 아이 성 변경 친부 동의',href:'/posts/naver-224255633337.html',type:'관련 법률정보'},
{title:'이혼·재혼 후 자녀 성본변경',keywords:'성본변경 친모 계부 이혼 재혼',href:'/posts/naver-224415922992.html',type:'처리사례'},
{title:'한글 이름 유지·한자만 개명',keywords:'개명 한자 이름 변경',href:'/posts/naver-224415724984.html',type:'처리사례'},
{title:'며느리의 성년후견인 선임',keywords:'성년후견 며느리 시어머니 주택연금',href:'/posts/naver-224413510561.html',type:'처리사례'}
];
let items=[...fixed];
const fixedHrefs=new Set(fixed.map(x=>x.href));
fetch('/assets/posts.json').then(r=>r.ok?r.json():[]).then(data=>{if(!Array.isArray(data))return;for(const p of data){if(!p||p.category!=='가사')continue;const href=p.href||p.url||'',title=p.title||'';if(title&&href&&!items.some(x=>x.href===href))items.push({title,keywords:title,href,type:'관련 법률정보'});}}).catch(()=>{});
const norm=s=>(s||'').toLowerCase().replace(/\s+/g,'');
function score(x,key){const t=norm(x.title),k=norm(x.keywords),s=norm(x.summary);let n=0;if(t===key)n+=120;else if(t.startsWith(key))n+=90;else if(t.includes(key))n+=70;if(k.includes(key))n+=35;if(s.includes(key))n+=15;if(x.type==='핵심안내')n+=20;return n;}
function matches(x,s){const n=norm(s);return norm(x.title+' '+(x.keywords||'')).includes(n);}
function render(all=false){const s=q.value.trim(),key=norm(s);const a=(all||!s)?items:items.filter(x=>matches(x,s)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order);list.innerHTML=a.slice(0,20).map(x=>'<li><a href="'+x.href+'"><span class="result-type">'+x.type+'</span>'+x.title+'</a></li>').join('')||'<li class="inheritance-empty">검색 결과가 없습니다.</li>';document.body.classList.add('dg-search-open');list.classList.add('is-open');q.setAttribute('aria-expanded','true');}
function close(){document.body.classList.remove('dg-search-open');list.classList.remove('is-open');q.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>list.classList.contains('is-open')?close():render(true));
toggle.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle.click()}});
q.addEventListener('input',()=>render(false));q.addEventListener('focus',()=>{if(q.value.trim())render(false)});
go.addEventListener('click',()=>{const a=list.querySelector('a');if(a)location.href=a.getAttribute('href');else render(false)});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go.click()}if(e.key==='Escape')close()});
document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-finder-inline'))close()});
})();