/* INHERITANCE_SEARCH_V1 */
(function(){
 const input=document.getElementById('inheritance-query'),toggle=document.getElementById('inheritance-toggle'),list=document.getElementById('inheritance-results'),search=document.getElementById('inheritance-search-button');
 if(!input||!toggle||!list||!search)return;
 const status=document.querySelector('.inheritance-search-status');
 if(!status)return;
 const fixed=[{title:'연락두절·행방불명 상속인',href:'/inheritance-missing-heir.html',type:'세부안내'},{title:'미성년자 상속인',href:'/inheritance-minor-heir.html',type:'세부안내'},{title:'해외거주·외국국적 상속인',href:'/inheritance-overseas-heir.html',type:'세부안내'},{title:'대습상속',href:'/inheritance-substitute-succession.html',type:'세부안내'},{title:'상속재산분할',href:'/inheritance-division.html',type:'세부안내'},{title:'상속등기 비용계산',href:'/acquisition-calculator.html?mode=inherit&v=20260910-accountfix',type:'계산기'},{title:'사망 후 전체 상속절차·필요서류',href:'/posts/naver-224399413497.html',type:'핵심안내'},{title:'인천 상속등기 절차·필요서류·취득세',href:'/posts/inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban.html',type:'핵심안내'}];
 const hubItem={title:'상속등기 전체 안내',href:'/inheritance.html',type:'업무페이지'};
 const onHub=location.pathname==='/inheritance.html'||location.pathname==='/inheritance'||location.pathname==='/inheritance/';
 let posts=[];
 const coreSlugs=new Set(['inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban','naver-224399413497']);
 const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
 const open=()=>{list.classList.add('is-open');document.body.classList.add('dg-search-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};
 const close=()=>{list.classList.remove('is-open');document.body.classList.remove('dg-search-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};
 function score(x,key){
   if(!key)return 0;
   const title=clean(x.title),keywords=clean(x.keywords),summary=clean(x.summary);
   let s=0;
   if(title===key)s+=120;
   else if(title.startsWith(key))s+=90;
   else if(title.includes(key))s+=70;
   if(keywords.includes(key))s+=35;
   if(summary.includes(key))s+=15;
   if(x.isCore)s+=20;
   return s;
 }
 function render(query=''){
   const key=clean(query);
   let items;
   if(!key){
     items=[...(onHub?[]:[hubItem]),...fixed,...posts].slice(0,18);
   }else{
     items=[...(onHub?[]:[hubItem]),...fixed,...posts].filter(x=>clean(x.title+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order).slice(0,18);
   }
   list.innerHTML='';
   status.textContent=key?'검색 결과 '+items.length+'개':'상속등기 관련 항목 '+items.length+'개';status.classList.add('is-active');
   if(!items.length){const li=document.createElement('li');li.className='inheritance-empty';li.textContent='상속등기 관련 검색 결과가 없습니다.';list.appendChild(li);open();return}
   items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='result-type';tag.textContent=x.type||'관련 글';a.appendChild(tag);a.appendChild(document.createTextNode(x.title));li.appendChild(a);list.appendChild(li)});open();
 }
 fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&['상속등기','상속재산분할'].includes(p.category)).map(p=>({title:p.title,summary:p.summary,keywords:p.keywords,href:'/posts/'+encodeURIComponent(p.slug)+'.html',type:'관련 법률정보',isCore:coreSlugs.has(String(p.slug||'').replace('.html',''))}));if(document.activeElement===input||input.value)render(input.value)}).catch(()=>{});
 toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});
 input.addEventListener('focus',()=>render(input.value));
 input.addEventListener('click',()=>render(input.value));
 input.addEventListener('input',()=>render(input.value));
 input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});
 search.addEventListener('click',()=>render(input.value));
 document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-combo'))close()});
})();
