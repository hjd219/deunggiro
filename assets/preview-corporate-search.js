(()=>{'use strict';
const q=document.getElementById('inheritance-query'),list=document.getElementById('inheritance-results'),toggle=document.getElementById('inheritance-toggle'),go=document.getElementById('inheritance-search-button');
if(!q||!list||!toggle||!go)return;

const fixed=[
 {title:'법인등기 한눈에 보기',keywords:'법인등기 법인',href:'#documents',type:'메인안내'},
 {title:'법인설립 필요서류·비용',keywords:'법인설립 설립 신규회사',href:'#service-1',type:'업무안내'},
 {title:'변경등기',keywords:'변경등기 임원변경 대표이사변경 상호변경 목적변경 본점이전 관외이전 중임 감사',href:'#service-2',type:'업무안내'},
 {title:'자본금증자',keywords:'자본금증자 증자 일반증자 가수금증자 신주',href:'#service-3',type:'업무안내'},
 {title:'회사계속등기',keywords:'회사계속 해산간주 청산종결 부활등기',href:'#service-4',type:'업무안내'},
 {title:'1인 법인 설립 절차·비용·필요서류',keywords:'1인법인 법인설립 설립절차 설립비용 필요서류 임원구성 조사보고인',href:'/posts/naver-224258524096.html',type:'핵심안내'},
 {title:'임원변경·본점이전·목적추가 절차와 비용',keywords:'임원변경 대표이사변경 본점주소이전 본점이전 목적추가 변경등기 비용',href:'/posts/naver-224356297494.html',type:'핵심안내'},
 {title:'법인 본점주소 이전 절차·서류·비용',keywords:'본점이전 관내이전 관외이전 주소이전 동일상호 필요서류 비용',href:'/posts/naver-224334189167.html',type:'핵심안내'},
 {title:'감사 임기만료·중임·취임·퇴임등기',keywords:'감사 임기만료 중임 취임 퇴임 임원변경 의결권',href:'/posts/naver-224259683352.html',type:'핵심안내'},
 {title:'해산간주·회사계속·부활등기',keywords:'해산간주 청산종결간주 회사계속 회사계속등기 부활등기',href:'/posts/naver-224363628938.html',type:'핵심안내'},
 {title:'전자서명·인증',keywords:'전자서명 인증 공동인증서 금융인증서 전자증명서',href:'#electronic-auth',type:'세부안내'},
 {title:'과태료 예상기준표',keywords:'과태료 지연 임기만료 등기해태',href:'#penalty-guide',type:'세부안내'},
 {title:'법인등기 자주 묻는 질문',keywords:'FAQ 질문 임기 과태료 회사계속',href:'#corp-faq',type:'세부안내'},
 {title:'법인설립 비용 계산',keywords:'법인설립 비용 수수료 계산기',href:'/corporate-calculator.html?job=est',type:'계산기'},
 {title:'변경등기 비용 계산',keywords:'변경등기 임원변경 본점이전 상호변경 목적변경 비용 계산기',href:'/corporate-calculator.html?v=20260910-clean',type:'계산기'},
 {title:'자본금증자 비용 계산',keywords:'증자 비용 계산기',href:'/corporate-calculator.html?job=inc',type:'계산기'},
 {title:'1인 법인 설립',keywords:'법인설립 1인법인 조사보고인',href:'/posts/naver-224411175706.html',type:'처리사례'},
 {title:'대표이사 사망 후 변경',keywords:'변경등기 대표이사 사망 임원변경',href:'/posts/naver-224411086807.html',type:'처리사례'},
 {title:'감사 중임·의결권 3%',keywords:'변경등기 감사 중임 의결권 3%',href:'/posts/naver-224411143025.html',type:'처리사례'},
 {title:'본점 관외이전',keywords:'변경등기 본점이전 관외이전 동일상호',href:'/posts/naver-224411109357.html',type:'처리사례'},
 {title:'회사계속·부활등기',keywords:'회사계속 해산간주 청산종결 부활등기',href:'/posts/naver-224411074752.html',type:'처리사례'}
];
let items=[...fixed];
fetch('/assets/posts.json').then(r=>r.ok?r.json():[]).then(data=>{
 if(!Array.isArray(data))return;
 for(const p of data){
  if(!p||p.category!=='법인등기')continue;
  const href=p.href||p.url||'',title=p.title||'';
  if(title&&href&&!items.some(x=>x.href===href))items.push({title,keywords:title,href,type:'처리사례'});
 }
}).catch(()=>{});

const norm=s=>(s||'').toLowerCase().replace(/\s+/g,'');
function matches(x,s){const n=norm(s);return norm(x.title+' '+(x.keywords||'')).includes(n);}
function render(all=false){
 const s=q.value.trim();
 const a=(all||!s)?items:items.filter(x=>matches(x,s));
 list.innerHTML=a.slice(0,20).map(x=>'<li><a href="'+x.href+'"><span class="result-type">'+x.type+'</span>'+x.title+'</a></li>').join('')||'<li class="inheritance-empty">검색 결과가 없습니다.</li>';
 list.classList.add('is-open');q.setAttribute('aria-expanded','true');
}
function close(){list.classList.remove('is-open');q.setAttribute('aria-expanded','false');}
toggle.addEventListener('click',()=>list.classList.contains('is-open')?close():render(true));
q.addEventListener('input',()=>render(false));
q.addEventListener('focus',()=>{if(q.value.trim())render(false)});
go.addEventListener('click',()=>{const a=list.querySelector('a');if(a)location.href=a.getAttribute('href');else render(false)});
q.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();go.click()}if(e.key==='Escape')close()});
document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-finder-inline'))close()});
})();