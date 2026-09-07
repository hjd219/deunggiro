(()=>{const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');const fixedByCategory={
'상속포기·한정승인':[
 {title:'상속포기·한정승인 절차',href:'#ren-process',type:'페이지'},
 {title:'상속포기·한정승인 필요서류',href:'#ren-documents',type:'페이지'},
 {title:'상속포기·한정승인 자주 묻는 질문',href:'#ren-faq',type:'페이지'}
],
'법인등기':[
 {title:'법인등기 필요서류',href:'#documents',type:'페이지'},
 {title:'법인등기 비용계산',href:'/corporate-calculator.html',type:'계산기'},
 {title:'법인등기 자주 묻는 질문',href:'#corp-faq',type:'페이지'}
],
'부동산등기':[
 {title:'부동산등기 업무별 필요서류',href:'#realestate-guide',type:'페이지'},
 {title:'부동산등기 비용계산',href:'/acquisition-calculator.html',type:'계산기'},
 {title:'근저당 설정·말소 필요서류',href:'#mortgageSetDocs',type:'페이지'}
],
'가사':[
 {title:'가사 주요 업무',href:'#family-services',type:'페이지'},
 {title:'가사 필요서류',href:'#documents',type:'페이지'},
 {title:'가사 자주 묻는 질문',href:'#family-faq',type:'페이지'}
]
};document.querySelectorAll('.dg-section-finder').forEach(root=>{const input=root.querySelector('.dg-section-query'),toggle=root.querySelector('.dg-section-toggle'),list=root.querySelector('.dg-section-results'),search=root.querySelector('.dg-section-search-button'),status=root.querySelector('.dg-section-search-status'),category=root.dataset.category||'';if(!input||!toggle||!list||!search)return;let posts=[];const fixed=fixedByCategory[category]||[];const open=()=>{list.classList.add('is-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};const close=()=>{list.classList.remove('is-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};function render(query=''){const key=clean(query);const postItems=posts.map(x=>({title:x.title||'',summary:x.summary||'',keywords:x.keywords||'',href:'/posts/'+encodeURIComponent(String(x.slug).replace(/\.html$/,''))+'.html',type:'관련 글'}));const items=[...fixed,...postItems].filter(x=>!key||clean((x.title||'')+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).slice(0,18);list.innerHTML='';if(status){status.textContent=key?'검색 결과 '+items.length+'개':category+' 관련 항목 '+items.length+'개';status.classList.add('is-active')}if(!items.length){const li=document.createElement('li');li.className='dg-section-empty';li.textContent='관련 검색 결과가 없습니다.';list.appendChild(li);open();return}items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='dg-section-result-type';tag.textContent=x.type||'관련 글';a.appendChild(tag);a.appendChild(document.createTextNode(x.title||''));li.appendChild(a);list.appendChild(li)});open()}fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&p.category===category);if(document.activeElement===input||input.value)render(input.value)}).catch(()=>{});toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});input.addEventListener('focus',()=>render(input.value));input.addEventListener('click',()=>render(input.value));input.addEventListener('input',()=>render(input.value));input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});search.addEventListener('click',()=>render(input.value));document.addEventListener('click',e=>{if(!root.contains(e.target))close()})})})();