(()=>{'use strict';
const q=document.getElementById('inheritance-query'),list=document.getElementById('inheritance-results'),toggle=document.getElementById('inheritance-toggle'),go=document.getElementById('inheritance-search-button');
if(!q||!list||!toggle||!go)return;
const fixed=[
 {title:'법인등기 한눈에 보기',href:'#documents',type:'법인등기'},
 {title:'법인설립 필요서류·비용',href:'#service-1',type:'업무안내'},
 {title:'변경등기 · 임원변경 · 상호변경 · 목적변경 · 본점이전',href:'#service-2',type:'업무안내'},
 {title:'자본금증자 필요서류·비용',href:'#service-3',type:'업무안내'},
 {title:'회사계속등기 · 해산간주 · 부활등기',href:'#service-4',type:'업무안내'},
 {title:'전자서명·인증',href:'#electronic-auth',type:'세부안내'},
 {title:'과태료 예상기준표',href:'#penalty-guide',type:'세부안내'},
 {title:'법인등기 자주 묻는 질문',href:'#corp-faq',type:'세부안내'},
 {title:'법인설립 비용 계산',href:'/corporate-calculator.html?job=est',type:'계산기'},
 {title:'변경등기 비용 계산',href:'/corporate-calculator.html?v=20260910-clean',type:'계산기'},
 {title:'자본금증자 비용 계산',href:'/corporate-calculator.html?job=inc',type:'계산기'}
]
fetch('/assets/posts.json').then(r=>r.ok?r.json():[]).then(data=>{if(Array.isArray(data))items=items.concat(data.filter(p=>p&&p.category==='법인등기').map(p=>({title:p.title||'',href:p.href||p.url||'',type:'처리사례'})).filter(x=>x.title&&x.href));}).catch(()=>{});
function render(all=false){const s=q.value.trim().toLowerCase();const a=(all||!s)?items:items.filter(x=>x.title.toLowerCase().includes(s));list.innerHTML=a.slice(0,12).map(x=>'<li><a href="'+x.href+'"><span class="result-type">'+x.type+'</span>'+x.title+'</a></li>').join('')||'<li class="inheritance-empty">검색 결과가 없습니다.</li>';list.classList.add('is-open');q.setAttribute('aria-expanded','true');}
function close(){list.classList.remove('is-open');q.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>list.classList.contains('is-open')?close():render(true));
q.addEventListener('input',()=>render(false));q.addEventListener('focus',()=>{if(q.value.trim())render(false)});
go.addEventListener('click',()=>{const a=list.querySelector('a');if(a)location.href=a.getAttribute('href');else render(false)});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go.click()}if(e.key==='Escape')close()});
document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-finder-inline'))close()});
})();