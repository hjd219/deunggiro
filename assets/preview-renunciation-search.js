/* INHERITANCE_SEARCH_V1 */
(function(){
 const input=document.getElementById('inheritance-query'),toggle=document.getElementById('inheritance-toggle'),list=document.getElementById('inheritance-results'),search=document.getElementById('inheritance-search-button');
 if(!input||!toggle||!list||!search)return;
 const status=document.querySelector('.inheritance-search-status');
 if(!status)return;
 const fixed=[
 
 
 
 {title:'상속포기 후 절차',href:'/renunciation-after-procedure.html',type:'세부안내'},
 {title:'사망신고 전 고인 예금 인출',href:'/renunciation-deceased-deposit.html',type:'세부안내'},
 {title:'상속포기 전 사망보험금·해지환급금',href:'/renunciation-death-insurance.html',type:'세부안내'},
 {title:'한정승인 후 청산절차',href:'/renunciation-limited-acceptance-liquidation.html',type:'세부안내'},
 {title:'인천 상속포기 절차·기간·필요서류',href:'/posts/inheritance-renunciation-incheon-procedure-documents-1ifftk.html',type:'핵심안내'},
 {title:'상속포기 신청기간과 후순위 상속인',href:'/posts/naver-224354174521.html',type:'핵심안내'},
 {title:'한정승인 기한·절차',href:'/posts/naver-224296496196.html',type:'핵심안내'},
 {title:'특별한정승인 절차',href:'/posts/naver-224302457067.html',type:'관련 법률정보'}
]
 const hubItem={title:'상속포기·한정승인 전체 안내',href:'/renunciation.html',type:'업무페이지'};
 const onHub=location.pathname==='/renunciation.html'||location.pathname==='/renunciation'||location.pathname==='/renunciation/';
 let posts=[];
 const coreHrefs=new Set(fixed.filter(x=>x.type==='핵심안내').map(x=>x.href));
 const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
 const open=()=>{list.classList.add('is-open');document.body.classList.add('dg-search-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};
 const close=()=>{list.classList.remove('is-open');document.body.classList.remove('dg-search-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};
 function score(x,key){const t=clean(x.title),k=clean(x.keywords),s=clean(x.summary);let n=0;if(t===key)n+=120;else if(t.startsWith(key))n+=90;else if(t.includes(key))n+=70;if(k.includes(key))n+=35;if(s.includes(key))n+=15;if(x.isCore)n+=20;return n;}
 function render(query=''){
   const key=clean(query);
   let items;
   if(!key)items=[...(onHub?[]:[hubItem]),...fixed,...posts].slice(0,18);
   else{items=[...(onHub?[]:[hubItem]),...fixed,...posts].filter(x=>clean(x.title+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order).slice(0,18);}
   list.innerHTML='';
   status.textContent=key?'검색 결과 '+items.length+'개':'상속포기·한정승인 관련 항목 '+items.length+'개';status.classList.add('is-active');
   if(!items.length){const li=document.createElement('li');li.className='inheritance-empty';li.textContent='상속포기·한정승인 관련 검색 결과가 없습니다.';list.appendChild(li);open();return}
   items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='result-type';tag.textContent=x.type||'관련 글';a.appendChild(tag);a.appendChild(document.createTextNode(x.title));li.appendChild(a);list.appendChild(li)});open();
 }
 fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&p.category==='상속포기·한정승인').map(p=>({title:p.title,summary:p.summary,keywords:p.keywords,href:'/posts/'+encodeURIComponent(p.slug)+'.html',type:'관련 법률정보',isCore:coreHrefs.has('/posts/'+String(p.slug).replace('.html','')+'.html')}));if(document.activeElement===input||input.value)render(input.value)}).catch(()=>{});
 toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});
 input.addEventListener('focus',()=>render(input.value));
 input.addEventListener('click',()=>render(input.value));
 input.addEventListener('input',()=>render(input.value));
 input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});
 search.addEventListener('click',()=>render(input.value));
 document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-combo'))close()});
})();
