(()=>{'use strict';
const q=document.getElementById('inheritance-query'),list=document.getElementById('inheritance-results'),toggle=document.getElementById('inheritance-toggle'),go=document.getElementById('inheritance-search-button');
if(!q||!list||!toggle||!go)return;
const fixed=[
{title:'가사 주요 업무',keywords:'가사 인천 이혼 후견 개명 필요서류',href:'#documents',type:'메인안내'},
{title:'이혼·재산분할',keywords:'협의이혼 재판이혼 재산분할 위자료',href:'#service-1',type:'업무안내'},
{title:'친권·양육권',keywords:'친권 양육권 양육비 면접교섭 미성년 자녀',href:'#service-2',type:'업무안내'},
{title:'성년후견·한정후견',keywords:'성년후견 한정후견 특정후견 후견인',href:'#service-3',type:'업무안내'},
{title:'개명·성본변경·가족관계등록',keywords:'개명 성본변경 가족관계등록부 정정 등록부창설',href:'#service-4',type:'업무안내'},
{title:'가사 필요서류',keywords:'가사 필요서류 이혼 개명 후견',href:'#family-docs',type:'세부안내'},
{title:'가사 진행 전 확인사항',keywords:'관할 법원 미성년 자녀 추가서류',href:'#family-check',type:'세부안내'},
{title:'협의이혼 절차 총정리',keywords:'협의이혼 절차 이혼합의서 숙려기간',href:'/posts/naver-224258629169.html',type:'핵심안내'},
{title:'친권자 변경 기준',keywords:'친권자 변경 공동친권 단독친권',href:'/posts/naver-224269144558.html',type:'핵심안내'},
{title:'성년후견·한정후견 총정리',keywords:'치매 고령 부모 성년후견 한정후견 임의후견',href:'/posts/naver-224254351514.html',type:'핵심안내'},
{title:'개명신청 절차·준비서류',keywords:'개명 신청 절차 준비서류 허가조건 기각사유',href:'/posts/naver-224254656540.html',type:'핵심안내'},
{title:'성본변경 허가 신청',keywords:'성본변경 아이 성 변경 친부 동의',href:'/posts/naver-224255633337.html',type:'핵심안내'},
{title:'가사 자주 묻는 질문',keywords:'FAQ 질문 이혼 재산분할 친권 후견',href:'#family-faq',type:'세부안내'},
{title:'이혼·재혼 후 자녀 성본변경',keywords:'성본변경 친모 계부 이혼 재혼',href:'/posts/naver-224415922992.html',type:'처리사례'},
{title:'한글 이름 유지·한자만 개명',keywords:'개명 한자 이름 변경',href:'/posts/naver-224415724984.html',type:'처리사례'},
{title:'며느리의 성년후견인 선임',keywords:'성년후견 며느리 시어머니 주택연금',href:'/posts/naver-224413510561.html',type:'처리사례'}
];
let items=[...fixed];
fetch('/assets/posts.json').then(r=>r.ok?r.json():[]).then(data=>{if(!Array.isArray(data))return;for(const p of data){if(!p||p.category!=='가사')continue;const href=p.href||p.url||'',title=p.title||'';if(title&&href&&!items.some(x=>x.href===href))items.push({title,keywords:title,href,type:'법률정보'});}}).catch(()=>{});
const norm=s=>(s||'').toLowerCase().replace(/\s+/g,'');
function matches(x,s){const n=norm(s);return norm(x.title+' '+(x.keywords||'')).includes(n);}
function render(all=false){const s=q.value.trim();const a=(all||!s)?items:items.filter(x=>matches(x,s));list.innerHTML=a.slice(0,20).map(x=>'<li><a href="'+x.href+'"><span class="result-type">'+x.type+'</span>'+x.title+'</a></li>').join('')||'<li class="inheritance-empty">검색 결과가 없습니다.</li>';list.classList.add('is-open');q.setAttribute('aria-expanded','true');}
function close(){list.classList.remove('is-open');q.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>list.classList.contains('is-open')?close():render(true));
toggle.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle.click()}});
q.addEventListener('input',()=>render(false));q.addEventListener('focus',()=>{if(q.value.trim())render(false)});
go.addEventListener('click',()=>{const a=list.querySelector('a');if(a)location.href=a.getAttribute('href');else render(false)});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go.click()}if(e.key==='Escape')close()});
document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-finder-inline'))close()});
})();