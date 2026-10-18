/* DG_BLOG_POPULARITY_V1: anonymous post visits, 30-minute session deduplication */
(function(){
  'use strict';
  if(!location.pathname.startsWith('/posts/')||!location.pathname.endsWith('.html'))return;
  var cat=(document.querySelector('meta[name="dg-category"]')||{}).content||'';
  var map={'상속등기':'inheritance','상속재산분할':'inheritance','상속포기·한정승인':'renunciation','법인등기':'corporate','부동산등기':'realestate','가사':'family'};
  var key=map[cat];if(!key)return;
  var slug=decodeURIComponent(location.pathname.split('/').pop().replace(/\.html$/,''));
  if(!/^[a-z0-9_-]+$/i.test(slug))return;
  var storageKey='dg-blog-visit-'+slug,last=0;
  try{last=Number(sessionStorage.getItem(storageKey)||0)}catch(e){}
  if(Date.now()-last<1800000)return;
  try{sessionStorage.setItem(storageKey,String(Date.now()))}catch(e){}
  function dayKey(){
    var d=new Date(),parts=new Intl.DateTimeFormat('en-US',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(d);
    var v={};parts.forEach(function(p){v[p.type]=p.value});return 'd'+v.year+v.month+v.day;
  }
  var id='project-b08e5f3c-fa49-4ae6-933',api='AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do';
  var path='projects/'+id+'/databases/(default)/documents/blog_views_'+key+'/'+slug;
  var body={writes:[{transform:{document:path,fieldTransforms:[
    {fieldPath:'total',increment:{integerValue:'1'}},
    {fieldPath:dayKey(),increment:{integerValue:'1'}}
  ]}}]};
  fetch('https://firestore.googleapis.com/v1/projects/'+id+'/databases/(default)/documents:commit?key='+encodeURIComponent(api),{
    method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),keepalive:true
  }).then(function(r){if(!r.ok)throw Error('View tracking unavailable')}).catch(function(){
    try{sessionStorage.removeItem(storageKey)}catch(e){}
  });
})();