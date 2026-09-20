(()=>{const input=document.querySelector('.hero-ai input'),btn=document.querySelector('.hero-ai button'),box=document.querySelector('.hero-ai-results');if(!input||!box)return;const data=[
{title:'부동산등기 한눈에 보기',href:'#documents',type:'부동산등기',keywords:'부동산등기 매매 증여 재산분할 근저당'},
{title:'매매등기',href:'#service-1',type:'업무',keywords:'매매 소유권이전 매도인 매수인 필요서류'},
{title:'증여등기',href:'#service-2',type:'업무',keywords:'증여 수증자 증여자 필요서류'},
{title:'이혼 재산분할등기',href:'#service-3',type:'업무',keywords:'이혼 재산분할 협의이혼 재판이혼'},
{title:'근저당권 설정·말소',href:'#service-4',type:'업무',keywords:'근저당 설정 말소 담보 대출'},
{title:'등기 전 꼭 확인하세요',href:'.corporate-support-row',type:'안내',keywords:'등기권리증 인감증명서 인감도장 유효기간'},
{title:'자주 묻는 질문',href:'#realestate-faq',type:'FAQ',keywords:'권리증 분실 취득세 가족간매매 증여 매매'},
{title:'부동산 취득세 계산기',href:'/acquisition-calculator.html',type:'계산기',keywords:'취득세 매매 증여 재산분할 계산기'}];
function esc(s){return s.replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
function run(){const q=input.value.trim().toLowerCase();if(!q){box.innerHTML='';box.hidden=true;return}const a=data.filter(x=>(x.title+' '+x.keywords).toLowerCase().includes(q)).slice(0,8);box.innerHTML=a.length?a.map(x=>'<a href="'+esc(x.href)+'"><b>'+esc(x.title)+'</b><small>'+esc(x.type)+'</small></a>').join(''):'<div class="hero-ai-empty">검색 결과가 없습니다.</div>';box.hidden=false}
input.addEventListener('input',run);input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();run()}});if(btn)btn.addEventListener('click',run);
})();