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
 var isCase=function(p){return /(?:^\s*\[?처리사례\]?|처리사례|해결사례|진행사례|등기 사례|선임 사례)/.test(p.title||'')};
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
  var mode='all',query='',order=null,loaded=Array.isArray(all);
  var data=(all||[]).filter(function(p){return p&&p.slug&&cats.includes(p.category)});
  function filtered(){
   var list=data.filter(function(p){return (!query||((p.title||'')+' '+(p.summary||'')+' '+(p.keywords||'')).toLowerCase().includes(query))&&(mode!=='case'||isCase(p))});
   if(mode==='popular'){list=list.filter(function(p){return order&&order[p.slug]>0}).sort(function(a,b){return order[b.slug]-order[a.slug]||(b.date||'').localeCompare(a.date||'')})}
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
   track.innerHTML=list.length?list.map(card).join(''):'<div class="dg-blog-message">'+(mode==='popular'?'최근 30일 조회수 데이터가 아직 없거나 집계를 연결하지 못했습니다.':'해당하는 게시글이 없습니다.')+'</div>';
   var n=list.length;status.textContent=n+'개 글';
   note.textContent=mode==='popular'?'최근 30일 방문 기준 · 실제 집계된 글만 표시':'';
   track.scrollLeft=0;
   requestAnimationFrame(updateArrows);
  }
  tabs.forEach(function(button){button.addEventListener('click',function(){
   mode=button.getAttribute('data-mode');
   tabs.forEach(function(t){t.setAttribute('aria-selected',String(t===button))});
   if(mode==='popular'&&order===null){
     note.textContent='최근 30일 인기글 불러오는 중';
     track.innerHTML='<div class="dg-blog-message">조회수 집계를 확인하고 있습니다.</div>';
     status.textContent='불러오는 중';
     updateArrows();
     getRankings(key).then(function(r){order=r;if(mode==='popular')render()}).catch(function(){order={};if(mode==='popular')render()});
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
    roots.forEach(function(root){setup(root,null)});
  });
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();