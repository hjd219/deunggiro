import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const postsPath=path.join(root,'data','posts.json');
const posts=JSON.parse(fs.readFileSync(postsPath,'utf8'));
const BASE='https://www.deunggiro.kr';

const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
const abs=u=>!u?'':(/^https?:\/\//i.test(u)?u:BASE+(u.startsWith('/')?u:'/'+u));
const sortPosts=list=>[...list].sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));

function replaceMarked(html,name,block,before){
  const start=`<!-- ${name}_START -->`;
  const end=`<!-- ${name}_END -->`;
  const re=new RegExp(`${start}[\\s\\S]*?${end}`,'m');
  const marked=`${start}\n${block}\n${end}`;
  if(re.test(html)) return html.replace(re,marked);
  const idx=html.indexOf(before);
  if(idx<0) return html;
  return html.slice(0,idx)+marked+'\n'+html.slice(idx);
}

function removeLegacyLegalInfoSection(html){
  return html.replace(/<section class="section white">[\s\S]*?<h2 class="title">등기로 법률정보<\/h2>[\s\S]*?<\/section>\s*(?=<!-- SEO_LATEST_START -->)/m,'');
}

function latestCards(list,limit=6){
  return sortPosts(list).slice(0,limit).map(p=>`<a href="/posts/${esc(p.slug)}.html" style="display:block;padding:15px 16px;border:1px solid #d9e0ea;border-radius:10px;background:#fff;text-decoration:none;color:#20242b"><small style="display:block;color:#36a9e1;font-weight:800;margin-bottom:5px">${esc(p.category)} · ${esc(p.date)}</small><strong style="display:block;line-height:1.45">${esc(p.title)}</strong></a>`).join('\n');
}

function buildLatestSection(list,title='최신 법률정보'){
  return `<section class="section white" aria-labelledby="seo-latest-title" style="padding-top:34px;padding-bottom:54px"><div class="container"><div class="label">LATEST LEGAL POSTS</div><h2 id="seo-latest-title" class="title" style="font-size:30px">${esc(title)}</h2><p class="desc">최근 작성한 법률정보를 개별 글로 바로 확인할 수 있습니다.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px">${latestCards(list,6)}</div><div style="margin-top:18px"><a class="btn btn-border" href="/posts.html">전체 법률정보 보기</a></div></div></section>`;
}

const indexPath=path.join(root,'index.html');
if(fs.existsSync(indexPath)){
  let html=fs.readFileSync(indexPath,'utf8');
  html=removeLegacyLegalInfoSection(html);
  html=replaceMarked(html,'SEO_LATEST',buildLatestSection(posts),'\n<section class="contact"');
  fs.writeFileSync(indexPath,html);
}

const categoryPages=[
  ['inheritance.html',['상속등기','상속재산분할'],'상속 관련 최신 글'],
  ['renunciation.html',['상속포기·한정승인'],'상속포기·한정승인 관련 최신 글'],
  ['corporate.html',['법인등기'],'법인등기 관련 최신 글'],
  ['realestate.html',['부동산등기'],'부동산등기 관련 최신 글'],
  ['family.html',['가사'],'가사 관련 최신 글']
];
for(const [file,cats,title] of categoryPages){
  const p=path.join(root,file);
  if(!fs.existsSync(p)) continue;
  const related=posts.filter(x=>cats.includes(x.category));
  let html=fs.readFileSync(p,'utf8');
  html=replaceMarked(html,'SEO_CATEGORY_LINKS',buildLatestSection(related,title),'\n<footer');
  fs.writeFileSync(p,html);
}

for(const p of posts){
  const file=path.join(root,'posts',`${p.slug}.html`);
  if(!fs.existsSync(file)) continue;
  let html=fs.readFileSync(file,'utf8');
  const url=`${BASE}/posts/${p.slug}.html`;
  const image=abs(p.thumbnail);
  const articleLd={
    '@context':'https://schema.org',
    '@type':'Article',
    headline:p.title,
    description:p.summary||p.title,
    datePublished:p.date,
    dateModified:p.date,
    mainEntityOfPage:{'@type':'WebPage','@id':url},
    author:{'@type':'Person',name:'현재두'},
    publisher:{'@type':'Organization',name:'현재두 법무사 사무소',url:BASE},
    ...(image?{image:[image]}:{})
  };
  const breadcrumbLd={
    '@context':'https://schema.org',
    '@type':'BreadcrumbList',
    itemListElement:[
      {'@type':'ListItem',position:1,name:'홈',item:BASE+'/'},
      {'@type':'ListItem',position:2,name:'법률정보',item:BASE+'/posts.html'},
      {'@type':'ListItem',position:3,name:p.category,item:BASE+'/posts.html'},
      {'@type':'ListItem',position:4,name:p.title,item:url}
    ]
  };
  const ldBlock=`<script type="application/ld+json">${JSON.stringify(articleLd).replace(/<\//g,'<\\/')}</script>\n<script type="application/ld+json">${JSON.stringify(breadcrumbLd).replace(/<\//g,'<\\/')}</script>`;
  html=replaceMarked(html,'SEO_STRUCTURED_DATA',ldBlock,'\n</head>');

  const crumb=`<nav aria-label="breadcrumb" style="max-width:850px;margin:0 auto 12px;padding:0 4px;font-size:13px;color:#68717d"><a href="/">홈</a> &gt; <a href="/posts.html">법률정보</a> &gt; <span>${esc(p.category)}</span></nav>`;
  html=replaceMarked(html,'SEO_BREADCRUMB',crumb,'<article class="article">');

  const rel=sortPosts(posts.filter(x=>x.slug!==p.slug && x.category===p.category)).slice(0,4);
  const relatedBlock=rel.length?`<section aria-labelledby="related-posts-title" style="margin-top:34px;padding-top:24px;border-top:1px solid #e5e7eb"><h2 id="related-posts-title" style="font-size:22px;margin:0 0 14px">같이 보면 좋은 글</h2><div style="display:grid;gap:9px">${rel.map(x=>`<a href="/posts/${esc(x.slug)}.html" style="display:block;padding:12px 14px;border:1px solid #d9e0ea;border-radius:9px;text-decoration:none"><small style="color:#36a9e1;font-weight:800">${esc(x.category)}</small><strong style="display:block;margin-top:3px;color:#20242b;line-height:1.45">${esc(x.title)}</strong></a>`).join('')}</div></section>`:'';
  html=replaceMarked(html,'SEO_RELATED_POSTS',relatedBlock,'<div class="related">');

  fs.writeFileSync(file,html);
}

console.log(`SEO automation complete: ${posts.length} posts processed.`);
