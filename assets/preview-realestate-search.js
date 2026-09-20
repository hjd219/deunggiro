(()=>{const input=document.querySelector('.hero-ai input'),btn=document.querySelector('.hero-ai button'),box=document.querySelector('.hero-ai-results');if(!input||!box)return;const data=[
{title:'부동산등기 한눈에 보기',href:'#documents',type:'부동산등기',keywords:'인천 부동산등기 소유권이전 필요서류 비용'},
{title:'매매 소유권이전등기',href:'#service-1',type:'업무',keywords:'매매등기 매도인 매수인 거래신고 취득세'},
{title:'증여 소유권이전등기',href:'#service-2',type:'업무',keywords:'증여등기 증여자 수증자 가족간 증여 취득세'},
{title:'이혼 재산분할등기',href:'#service-3',type:'업무',keywords:'재산분할 협의이혼 재판이혼 소유권이전'},
{title:'상속 소유권이전등기',href:'#service-3a',type:'업무',keywords:'상속등기 협의분할 피상속인 상속인 제적등본'},
{title:'상속등기 상세안내',href:'/inheritance.html',type:'핵심안내',keywords:'상속등기 공동상속 단독상속 협의분할'},
{title:'근저당권 설정·말소',href:'#service-4',type:'업무',keywords:'근저당 설정 말소 담보 대출 해지증서'},
{title:'등기 전 꼭 확인하세요',href:'.corporate-support-row',type:'안내',keywords:'등기권리증 인감증명서 인감도장 서류 유효기간'},
{title:'취득세 계산',href:'/acquisition-calculator.html',type:'계산기',keywords:'취득세 계산기 매매 증여 재산분할'},
{title:'자주 묻는 질문',href:'#realestate-faq',type:'FAQ',keywords:'권리증 분실 취득세 가족간매매 증여 매매'}
];
function esc(s){return s.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function run(){const q=input.value.trim().toLowerCase();if(!q){box.innerHTML='';box.hidden=true;return}const a=data.filter(x=>(x.title+' '+x.keywords+' '+x.type).toLowerCase().includes(q)).slice(0,10);box.innerHTML=a.length?a.map(x=>'<a href="'+esc(x.href)+'"><b>'+esc(x.title)+'</b><small>'+esc(x.type)+'</small></a>').join(''):'<div class="hero-ai-empty">검색 결과가 없습니다.</div>';box.hidden=false}
input.addEventListener('input',run);input.addEventListener('focus',()=>{if(input.value.trim())run()});input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();run()}});if(btn)btn.addEventListener('click',run);document.addEventListener('click',e=>{if(!e.target.closest('.hero-ai'))box.hidden=true});
})();