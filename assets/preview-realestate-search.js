/* UNIFIED_SERVICE_SEARCH_V2 */
(function(){
 const input=document.getElementById('inheritance-query'),toggle=document.getElementById('inheritance-toggle'),list=document.getElementById('inheritance-results'),search=document.getElementById('inheritance-search-button');
 if(!input||!toggle||!list||!search)return;
 const status=document.querySelector('.inheritance-search-status');
 const fixed=[
 {title:"상속등기 상세안내",keywords:"상속등기 공동상속 단독상속 협의분할",href:"/inheritance.html",type:"핵심안내"},
 {title:"상속·증여·매매 등기 필요서류",keywords:"상속 증여 매매 부동산등기 필요서류 준비서류",href:"/posts/naver-224242416419.html",type:"핵심안내"},
 {title:"등기권리증 분실 시 해결방법",keywords:"등기권리증 등기필증 분실 확인서면 매매",href:"/posts/sale-real-estate-guide-bvcdri.html",type:"핵심안내"},
 {title:"취득세 계산",keywords:"취득세 계산기 매매 증여 재산분할",href:"/acquisition-calculator.html",type:"계산기"}
 ];
 let posts=[];
 const fixedHrefs=new Set(fixed.map(x=>x.href));
 const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
 const open=()=>{list.classList.add('is-open');document.body.classList.add('dg-search-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};
 const close=()=>{list.classList.remove('is-open');document.body.classList.remove('dg-search-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};
 function score(x,key){if(!key)return 0;const t=clean(x.title),k=clean(x.keywords),s=clean(x.summary);let n=0;if(t===key)n+=120;else if(t.startsWith(key))n+=90;else if(t.includes(key))n+=70;if(k.includes(key))n+=35;if(s.includes(key))n+=15;if(x.type==='핵심안내')n+=20;return n;}
 function render(query=''){
  const key=clean(query);let items;
  if(!key)items=[...fixed,...posts].slice(0,18);
  else items=[...fixed,...posts].filter(x=>clean(x.title+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order).slice(0,18);
  list.innerHTML='';
  if(status){status.textContent=key?'검색 결과 '+items.length+'개':'부동산등기 관련 항목 '+items.length+'개';status.classList.add('is-active');}
  if(!items.length){const li=document.createElement('li');li.className='inheritance-empty';li.textContent='부동산등기 관련 검색 결과가 없습니다.';list.appendChild(li);open();return;}
  items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='result-type';tag.textContent=x.type||'관련 법률정보';a.appendChild(tag);a.appendChild(document.createTextNode(x.title));li.appendChild(a);list.appendChild(li);});open();
 }
 fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{
  posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&p.category==="부동산등기").map(p=>({title:p.title,summary:p.summary,keywords:p.keywords,href:'/posts/'+encodeURIComponent(String(p.slug).replace('.html',''))+'.html',type:'관련 법률정보'})).filter(p=>!fixedHrefs.has(p.href));
  if(document.activeElement===input||input.value)render(input.value);
 }).catch(()=>{});
 toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});
 input.addEventListener('focus',()=>render(input.value));
 input.addEventListener('click',()=>render(input.value));
 input.addEventListener('input',()=>render(input.value));
 input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});
 search.addEventListener('click',()=>render(input.value));
 document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-combo')&&!e.target.closest('.inheritance-finder-inline'))close()});
})();
