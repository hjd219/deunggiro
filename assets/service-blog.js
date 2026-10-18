/* DG_SERVICE_BLOG_CAROUSEL_V1 */
(function(){
 'use strict';
 var cfg={
  inheritance:['상속등기','상속재산분할'],
  renunciation:['상속포기·한정승인'],
  corporate:['법인등기'],
  realestate:['부동산등기'],
  family:['가사']
 };
 var id='project-b08e5f3c-fa49-4ae6-933',api='AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do';
 var base='https://firestore.googleapis.com/v1/projects/'+id+'/databases/default/documents/';
 var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})};
 var explicitCaseSlugs={'realestate-naver-224434182517':1,'realestate-naver-224434200680':1,'family-naver-224434219104':1};
 var isCase=function(p){return /^\s*\[(?:처리사례|해결사례|진행사례)\]/.test(p.title||'')||!!explicitCaseSlugs[p.slug]};
 var featured={"inheritance":["inheritance-naver-224440231991","naver-224283775649","naver-224277482133","naver-224286164764","naver-224286296559","naver-224277586827","naver-224239720854","naver-224410898313"],"renunciation":["renunciation-naver-224441307964","renunciation-naver-224441320334","renunciation-naver-224432746077","naver-224239766795","naver-224239702465","naver-221988345481","naver-224278798851","naver-224286147004"],"corporate":["corporate-naver-224425670405","naver-224230217554","naver-224235350490","naver-224236741197","naver-224238290942","naver-224242199243","naver-224242232710","naver-224250873284"],"realestate":["naver-224242416419","naver-224309218026","naver-224400625408","naver-224289926337","naver-224285020929","naver-224353211876","naver-224245108178","naver-224266729920"],"family":["naver-224258629169","naver-224268863328","naver-224254351514","naver-224254656540","naver-224255633337","naver-224294791896","naver-224271354288","family-naver-224434219104"]};
 var localDay=function(d){var ps=new Intl.DateTimeFormat('en-US',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(d),a={};ps.forEach(function(x){a[x.type]=x.value});return 'd'+a.year+a.month+a.day};
 var days=Array.from({length:30},function(_,i){return localDay(new Date(Date.now()-i*86400000))});
 var cache={};
 function getRankings(key){
  if(cache[key])return cache[key];
  cache[key]=(async function(){
    var counts={},next='';
    do{
     var url=base+'blog_views_'+key+'?pageSize=200&key='+encodeURIComponent(api)+(next?'&pageToken='+encodeURIComponent(next):'');
     var r=await fetch(url,{cache:'no-store'});
     if(!r.ok)throw Error('Unavailable '+r.status);
     var j=await r.json();
     (j.documents||[]).forEach(function(doc){
       var slug=String(doc.name||'').split('/').pop(),f=doc.fields||{},sum=0;
       days.forEach(function(k){sum+=Number(((f[k]||{}).integerValue)||0)});
       counts[slug]=sum;
     });
     next=j.nextPageToken||'';
    }while(next);
    return counts;
  })();
  return cache[key];
 }
 function shortTitle(raw){
 var s=String(raw||'').replace(/^\s*(?:\[[^\]]{1,45}\]\s*)+/g,'').replace(/^\s*\(처리사례\)\s*/,'').replace(/\s+/g,' ').trim();
 var part=s.split(/\s*[｜|]\s*/)[0].trim();if(part.length>=7)s=part;
 s=s.replace(/^인천\s+(?=\S)/,'').replace(/\s*(?:쉽게\s*정리|완벽\s*정리|핵심\s*정리|총정리|완벽하게\s*정리)\s*$/,'').trim();
 if(s.length<=24)return s;
 var cut=s.slice(0,24),last=cut.lastIndexOf(' ');if(last>=15)cut=cut.slice(0,last);else cut=s.slice(0,22);
 return cut.replace(/[\s,，·]+$/,'')+'…';
 }
 function card(p){
  var href='/posts/'+encodeURIComponent(p.slug)+'.html';
  var image=p.thumbnail||'/favicon.png';
  return '<a class="dg-blog-card" href="'+esc(href)+'" aria-label="'+esc(p.title)+'"><img class="dg-blog-thumb" loading="lazy" decoding="async" src="'+esc(image)+'" alt="" onerror="this.onerror=null;this.src=\'/favicon.png\'"><div class="dg-blog-card-content"><time datetime="'+esc(p.date)+'">'+esc(p.date||'')+'</time><h3 title="'+esc(p.title)+'">'+esc(shortTitle(p.title))+'</h3></div></a>';
 }
 function setup(root,all){
  var key=root.getAttribute('data-dg-blog');
  var cats=cfg[key];if(!cats)return;
  var track=root.querySelector('.dg-blog-track'),search=root.querySelector('.dg-blog-search input'),tabs=root.querySelectorAll('.dg-blog-tab'),status=root.querySelector('.dg-blog-status'),note=root.querySelector('.dg-blog-note');
  var prev=root.querySelector('[data-dg-prev]'),next=root.querySelector('[data-dg-next]');
  var mode='all',query='',order=null,rankingPending=false,loaded=Array.isArray(all);
  var data=(all||[]).filter(function(p){return p&&p.slug&&cats.includes(p.category)});
  function filtered(){
   var list=data.filter(function(p){return (!query||((p.title||'')+' '+(p.summary||'')+' '+(p.keywords||'')).toLowerCase().includes(query))&&(mode!=='case'||isCase(p))});
   if(mode==='popular'){
    var scores=order||{},priority={},picks=featured[key]||[];
    picks.forEach(function(slug,i){priority[slug]=i});
    list.sort(function(a,b){
      var bv=Number(scores[b.slug]||0),av=Number(scores[a.slug]||0);
      if(bv!==av)return bv-av;
      var aRank=Object.prototype.hasOwnProperty.call(priority,a.slug)?priority[a.slug]:1000;
      var bRank=Object.prototype.hasOwnProperty.call(priority,b.slug)?priority[b.slug]:1000;
      return aRank-bRank||(b.date||'').localeCompare(a.date||'');
    });
    list=list.slice(0,12);
   }
   return list;
  }
  function updateArrows(){
   var max=track.scrollWidth-track.clientWidth;
   prev.disabled=track.scrollLeft<5;
   next.disabled=track.scrollLeft>=max-5||max<5;
  }
  function render(){
   if(!loaded)return;
   var list=filtered();
   track.innerHTML=list.length?list.map(card).join(''):'<div class="dg-blog-message">해당하는 게시글이 없습니다.</div>';
   var n=list.length;status.textContent=n+'개 글';
   var measured=mode==='popular'&&data.some(function(p){return order&&Number(order[p.slug])>0});
   note.textContent=mode==='popular'?(rankingPending?'조회수 확인 중 · 추천글 먼저 표시':measured?'최근 30일 조회수 우선 · 그 외 추천글':'조회수 미집계 · 추천글 임시 표시'):'';
   track.scrollLeft=0;
   requestAnimationFrame(updateArrows);
  }
  tabs.forEach(function(button){button.addEventListener('click',function(){
   mode=button.getAttribute('data-mode');
   tabs.forEach(function(t){t.setAttribute('aria-selected',String(t===button))});
   if(mode==='popular'&&order===null){
     // Display editorial selections immediately until genuine view counts arrive.
     order={};rankingPending=true;render();
     getRankings(key).then(function(r){order=r;rankingPending=false;if(mode==='popular')render()}).catch(function(){order={};rankingPending=false;if(mode==='popular')render()});
   }else render();
  })});
  search.addEventListener('input',function(){query=search.value.trim().toLowerCase();render()});
  prev.addEventListener('click',function(){track.scrollBy({left:-Math.max(track.clientWidth*.8,180),behavior:'smooth'})});
  next.addEventListener('click',function(){track.scrollBy({left:Math.max(track.clientWidth*.8,180),behavior:'smooth'})});
  track.addEventListener('scroll',updateArrows,{passive:true});
  window.addEventListener('resize',updateArrows,{passive:true});
  if(loaded){
   // Server HTML already contains the complete article set. Keep these nodes intact
   // on first load to prevent horizontal scroll jumps and needless image reloads.
   var initialLinks=Array.prototype.map.call(track.querySelectorAll(':scope > a.dg-blog-card[href]'),function(a){return a.getAttribute('href')});
   var currentLinks=data.map(function(p){return '/posts/'+encodeURIComponent(p.slug)+'.html'});
   var same=initialLinks.length===currentLinks.length&&initialLinks.every(function(href,i){return href===currentLinks[i]});
   if(same){status.textContent=data.length+'개 글';requestAnimationFrame(updateArrows)}
   else render();
  }else updateArrows();
 }
 function init(){
  var roots=[].slice.call(document.querySelectorAll('.dg-service-blog[data-dg-blog]'));
  if(!roots.length)return;
  fetch('/data/posts.json',{cache:'no-store'}).then(function(r){if(!r.ok)throw Error('posts');return r.json()}).then(function(posts){
    roots.forEach(function(root){setup(root,posts)});
  }).catch(function(){
    // Keep all server-rendered links and working tabs if the data feed is unavailable.
    roots.forEach(function(root){
      var cats=cfg[root.getAttribute('data-dg-blog')]||[];
      var posts=Array.prototype.map.call(root.querySelectorAll('.dg-blog-track > a.dg-blog-card'),function(a){
        var href=a.getAttribute('href')||'',t=a.querySelector('time'),img=a.querySelector('img');
        return {slug:decodeURIComponent(href.split('/').pop().replace(/\.html$/,'')),title:a.getAttribute('aria-label')||'',date:t?t.getAttribute('datetime'):'',thumbnail:img?img.getAttribute('src'):'',category:cats[0]};
      });
      setup(root,posts);
    });
  });
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();