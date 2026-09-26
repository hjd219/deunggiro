/* SERVICE_SEARCH_V1 — shared scoped search for practice pages */
(function(){
 const path=location.pathname;
 const configs={
  inheritance:{
   match:/^\/inheritance(?:\.html|\/|-(?:missing-heir|minor-heir|overseas-heir|substitute-succession|division)\.html)?$/,
   categories:['상속등기','상속재산분할'],label:'상속등기',
   hub:{title:'상속등기 전체 안내',href:'/inheritance.html',type:'업무페이지'},
   hubPath:'/inheritance.html',
   fixed:[
    {title:'연락두절·행방불명 상속인',href:'/inheritance-missing-heir.html',type:'세부안내'},
    {title:'미성년자 상속인',href:'/inheritance-minor-heir.html',type:'세부안내'},
    {title:'해외거주·외국국적 상속인',href:'/inheritance-overseas-heir.html',type:'세부안내'},
    {title:'대습상속',href:'/inheritance-substitute-succession.html',type:'세부안내'},
    {title:'상속재산분할',href:'/inheritance-division.html',type:'세부안내'},
    {title:'상속등기 비용계산',keywords:'상속등기 비용 수수료 취득세 계산',href:'/acquisition-calculator.html?mode=inherit&v=20260910-accountfix',type:'계산기'},
    {title:'사망 후 전체 상속절차·필요서류',href:'/posts/naver-224399413497.html',type:'핵심안내'},
    {title:'인천 상속등기 절차·필요서류·취득세',href:'/posts/inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban.html',type:'핵심안내'}
   ]
  },
  renunciation:{
   match:/^\/renunciation(?:\.html|\/|-(?:after-procedure|deceased-deposit|death-insurance|limited-acceptance-liquidation)\.html)?$/,
   categories:['상속포기·한정승인'],label:'상속포기·한정승인',
   hub:{title:'상속포기·한정승인 전체 안내',href:'/renunciation.html',type:'업무페이지'},
   hubPath:'/renunciation.html',
   fixed:[
    {title:'상속포기 후 절차',keywords:'상속포기 후 절차 결정 수리 후순위',href:'/renunciation-after-procedure.html',type:'세부안내'},
    {title:'사망신고 전 고인 예금 인출',keywords:'사망신고 전 고인 예금 인출 사망자 예금',href:'/renunciation-deceased-deposit.html',type:'세부안내'},
    {title:'상속포기 전 사망보험금·해지환급금',keywords:'사망보험금 해지환급금 상속포기 보험금',href:'/renunciation-death-insurance.html',type:'세부안내'},
    {title:'한정승인 후 청산절차',keywords:'한정승인 후 청산절차 신문공고 상속재산파산 채권자',href:'/renunciation-limited-acceptance-liquidation.html',type:'세부안내'},
    {title:'인천 상속포기 절차·기간·필요서류',href:'/posts/inheritance-renunciation-incheon-procedure-documents-1ifftk.html',type:'핵심안내'},
    {title:'상속포기 신청기간과 후순위 상속인',href:'/posts/naver-224354174521.html',type:'핵심안내'},
    {title:'한정승인 기한·절차',href:'/posts/naver-224296496196.html',type:'핵심안내'},
    {title:'특별한정승인 절차',href:'/posts/naver-224302457067.html',type:'관련 법률정보'}
   ]
  },
  corporate:{
   match:/^\/corporate(?:\.html|\/)?$/,categories:['법인등기'],label:'법인등기',
   fixed:[
    {title:'1인 법인 설립 절차·비용·필요서류',keywords:'1인법인 법인설립 설립절차 설립비용 필요서류 임원구성 조사보고인',href:'/posts/naver-224258524096.html',type:'핵심안내'},
    {title:'임원변경·본점이전·목적추가 절차와 비용',keywords:'임원변경 대표이사변경 본점주소이전 본점이전 목적추가 변경등기 비용',href:'/posts/naver-224356297494.html',type:'핵심안내'},
    {title:'법인 본점주소 이전 절차·서류·비용',keywords:'본점이전 관내이전 관외이전 주소이전 동일상호 필요서류 비용',href:'/posts/naver-224334189167.html',type:'핵심안내'},
    {title:'법인설립 비용 계산',keywords:'법인설립 비용 수수료 계산기',href:'/corporate-calculator.html?job=est',type:'계산기'},
    {title:'변경등기 비용 계산',keywords:'변경등기 임원변경 본점이전 상호변경 목적변경 비용 계산기',href:'/corporate-calculator.html?v=20260910-clean',type:'계산기'},
    {title:'자본금증자 비용 계산',keywords:'증자 비용 계산기',href:'/corporate-calculator.html?job=inc',type:'계산기'}
   ]
  },
  realestate:{
   match:/^\/realestate(?:\.html|\/)?$/,categories:['부동산등기'],label:'부동산등기',
   fixed:[
    {title:'상속·증여·매매 등기 필요서류',keywords:'상속 증여 매매 부동산등기 필요서류 준비서류',href:'/posts/naver-224242416419.html',type:'핵심안내'},
    {title:'등기권리증 분실 시 해결방법',keywords:'등기권리증 등기필증 분실 확인서면 매매',href:'/posts/sale-real-estate-guide-bvcdri.html',type:'핵심안내'},
    {title:'취득세 계산',keywords:'취득세 계산기 매매 증여 재산분할',href:'/acquisition-calculator.html',type:'계산기'}
   ]
  },
  family:{
   match:/^\/family(?:\.html|\/)?$/,categories:['가사'],label:'가사',
   fixed:[
    {title:'협의이혼 절차 총정리',keywords:'협의이혼 절차 이혼합의서 숙려기간',href:'/posts/naver-224258629169.html',type:'핵심안내'},
    {title:'친권자 변경 기준',keywords:'친권자 변경 공동친권 단독친권',href:'/posts/naver-224269144558.html',type:'핵심안내'},
    {title:'성년후견·한정후견 총정리',keywords:'치매 고령 부모 성년후견 한정후견 임의후견',href:'/posts/naver-224254351514.html',type:'핵심안내'}
   ]
  }
 };
 const cfg=Object.values(configs).find(x=>x.match.test(path));
 if(!cfg)return;
 const input=document.getElementById('inheritance-query'),toggle=document.getElementById('inheritance-toggle'),list=document.getElementById('inheritance-results'),search=document.getElementById('inheritance-search-button'),status=document.querySelector('.inheritance-search-status');
 if(!input||!toggle||!list||!search||!status)return;
 let posts=[];
 const fixedHrefs=new Set(cfg.fixed.map(x=>x.href));
 const onHub=cfg.hubPath&&(path===cfg.hubPath||path===cfg.hubPath.replace('.html','')||path===cfg.hubPath.replace('.html','/'));
 const clean=s=>String(s||'').toLowerCase().replace(/\s+/g,'');
 const open=()=>{list.classList.add('is-open');document.body.classList.add('dg-search-open');input.setAttribute('aria-expanded','true');toggle.textContent='▲'};
 const close=()=>{list.classList.remove('is-open');document.body.classList.remove('dg-search-open');input.setAttribute('aria-expanded','false');toggle.textContent='▼'};
 const base=()=>[...(cfg.hub&&!onHub?[cfg.hub]:[]),...cfg.fixed,...posts];
 function score(x,key){if(!key)return 0;const t=clean(x.title),k=clean(x.keywords),s=clean(x.summary);let n=0;if(t===key)n+=120;else if(t.startsWith(key))n+=90;else if(t.includes(key))n+=70;if(k.includes(key))n+=35;if(s.includes(key))n+=15;if(x.type==='핵심안내')n+=20;return n}
 function render(query=''){
  const key=clean(query);let items=base();
  if(key)items=items.filter(x=>clean(x.title+' '+(x.summary||'')+' '+(x.keywords||'')).includes(key)).map((x,i)=>({...x,_score:score(x,key),_order:i})).sort((a,b)=>b._score-a._score||a._order-b._order);
  items=items.slice(0,18);list.innerHTML='';
  status.textContent=key?'검색 결과 '+items.length+'개':cfg.label+' 관련 항목 '+items.length+'개';status.classList.add('is-active');
  if(!items.length){const li=document.createElement('li');li.className='inheritance-empty';li.textContent=cfg.label+' 관련 검색 결과가 없습니다.';list.appendChild(li);open();return}
  items.forEach(x=>{const li=document.createElement('li'),a=document.createElement('a'),tag=document.createElement('span');a.href=x.href;tag.className='result-type';tag.textContent=x.type||'관련 법률정보';a.appendChild(tag);a.appendChild(document.createTextNode(x.title));li.appendChild(a);list.appendChild(li)});open()
 }
 fetch('/data/posts.json?v='+Date.now(),{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(data=>{
  posts=(Array.isArray(data)?data:[]).filter(p=>p&&p.slug&&cfg.categories.includes(p.category)).map(p=>({title:p.title,summary:p.summary,keywords:p.keywords,href:'/posts/'+encodeURIComponent(String(p.slug).replace('.html',''))+'.html',type:'관련 법률정보'})).filter(p=>!fixedHrefs.has(p.href));
  if(document.activeElement===input||input.value)render(input.value)
 }).catch(()=>{});
 toggle.addEventListener('click',e=>{e.stopPropagation();list.classList.contains('is-open')?close():render(input.value)});
 input.addEventListener('focus',()=>render(input.value));input.addEventListener('click',()=>render(input.value));input.addEventListener('input',()=>render(input.value));
 input.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();render(input.value)}if(e.key==='Escape')close()});
 search.addEventListener('click',()=>render(input.value));
 document.addEventListener('click',e=>{if(!e.target.closest('.inheritance-combo')&&!e.target.closest('.inheritance-finder-inline'))close()});
})();
