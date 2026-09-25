/* INHERITANCE_SEARCH_V1 */
(function(){
 const input=document.getElementById('inheritance-query'),toggle=document.getElementById('inheritance-toggle'),list=document.getElementById('inheritance-results'),search=document.getElementById('inheritance-search-button');
 if(!input||!toggle||!list||!search)return;
 const status=document.querySelector('.inheritance-search-status');
 if(!status)return;
 const fixed=[
 {title:'상속포기·한정승인 절차',href:'#inheritance-overview',type:'페이지'},
 {title:'상속포기·한정승인 필요서류',href:'#documents',type:'페이지'},
 {title:'상속포기·한정승인 자주 묻는 질문',href:'#ren-faq',type:'페이지'},
 {title:'상속포기 후 절차',href:'/renunciation-after.html',type:'세부페이지'},
 {title:'사망신고 전 고인 예금 인출',href:'/deceased-deposit-withdrawal.html',type:'세부페이지'},
 {title:'한정승인 후 청산절차',href:'/limited-acceptance-liquidation.html',type:'세부페이지'},
 {title:'인천 상속포기 절차·기간·필요서류',href:'/posts/inheritance-renunciation-incheon-procedure-documents-1ifftk.html',type:'핵심 안내'},
 {title:'상속포기 신청기간과 후순위 상속인',href:'/posts/naver-224354174521.html',type:'핵심 안내'},
 {title:'한정승인 기한·절차',href:'/posts/naver-224296496196.html',type:'핵심 안내'},
 {title:'특별한정승인 절차',href:'/posts/naver-224302457067.html',type:'핵심 안내'}
]
 let posts=[];
 const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
 const open=()=>{list.classList.add('is-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};
 const close=()=>{list.classList.remove('is-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};
 function render(query=''){
   const key=clean(query),items=[...fixed,...posts].filter(x=>!key||clean(x.title+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).slice(0,18);
   list.innerHTML='';
   status.textContent=key?'검색 결과 '+items.length+'개':'상속포기·한정승인 관련 항목 '+items.length+'개';status.classList.add('is-active');
   if(!items.length){const li=document.createElement('li');li.className='inheritance-empty';li.textContent='상속포기·한정승인 관련 검색 결과가 없습니다.';list.appendChild(li);open();return}
   items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='result-type';tag.textContent=x.type||'관련 글';a.appendChild(tag);a.appendChild(document.createTextNode(x.title));li.appendChild(a);list.appendChild(li)});open();
 }
 fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&p.category==='상속포기·한정승인').map(p=>({title:p.title,summary:p.summary,keywords:p.keywords,href:'/posts/'+encodeURIComponent(p.slug)+'.html',type:'관련 글'}));if(document.activeElement===input||input.value)render(input.value)}).catch(()=>{});
 toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});
 input.addEventListener('focus',()=>render(input.value));
 input.addEventListener('click',()=>render(input.value));
 input.addEventListener('input',()=>render(input.value));
 input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});
 search.addEventListener('click',()=>render(input.value));
 document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-combo'))close()});
})();
