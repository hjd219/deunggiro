import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root=process.cwd();
const postsPath=path.join(root,'data','posts.json');
const BASE='https://www.deunggiro.kr';

const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
const clean=s=>String(s??'').trim();
const abs=u=>!u?'':(/^https?:\/\//i.test(u)?u:BASE+(u.startsWith('/')?u:'/'+u));
const sortPosts=list=>[...list].sort((a,b)=>String(b.date||'').localeCompare(String(a.date||'')));
const todayKST=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());

function loadPosts(){
  if(!fs.existsSync(postsPath)) throw new Error('data/posts.json 파일이 없습니다.');
  let raw;
  try{ raw=JSON.parse(fs.readFileSync(postsPath,'utf8')); }
  catch{ throw new Error('data/posts.json JSON 형식이 깨져 있습니다.'); }
  if(!Array.isArray(raw)) throw new Error('data/posts.json은 배열 형식이어야 합니다.');

  const seen=new Set();
  const valid=[];
  raw.forEach((p,i)=>{
    if(!p || typeof p!=='object') return console.warn(`SEO 경고: ${i+1}번째 글 데이터가 객체가 아닙니다.`);
    const item={...p,
      title:clean(p.title), category:clean(p.category), date:clean(p.date), slug:clean(p.slug),
      keywords:clean(p.keywords), summary:clean(p.summary), thumbnail:clean(p.thumbnail)
    };
    if(!item.title || !item.category || !item.date || !item.slug){
      console.warn(`SEO 경고: 필수값 누락으로 건너뜀 - ${item.title||item.slug||i+1}`); return;
    }
    if(!/^\d{4}-\d{2}-\d{2}$/.test(item.date)){
      console.warn(`SEO 경고: 날짜 형식 오류로 건너뜀 - ${item.slug}`); return;
    }
    if(!/^[a-z0-9][a-z0-9-]*$/i.test(item.slug)){
      console.warn(`SEO 경고: URL 형식 오류로 건너뜀 - ${item.slug}`); return;
    }
    if(seen.has(item.slug)) throw new Error(`중복 slug가 있습니다: ${item.slug}`);
    seen.add(item.slug); valid.push(item);
  });
  return valid;
}

const posts=loadPosts();
if(!posts.length) throw new Error('유효한 게시글이 하나도 없습니다. 자동 SEO 작업을 중단합니다.');

function replaceMarked(html,name,block,before){
  const start=`<!-- ${name}_START -->`;
  const end=`<!-- ${name}_END -->`;
  const re=new RegExp(`${start}[\\s\\S]*?${end}`,'m');
  const marked=`${start}\n${block}\n${end}`;
  if(re.test(html)) return html.replace(re,marked);
  const idx=html.indexOf(before);
  if(idx<0){ console.warn(`SEO 경고: ${name} 삽입 위치를 찾지 못했습니다.`); return html; }
  return html.slice(0,idx)+marked+'\n'+html.slice(idx);
}

function removeLegacyLegalInfoSection(html){
  return html.replace(/<section class="section white">[\s\S]*?<h2 class="title">등기로 법률정보<\/h2>[\s\S]*?<\/section>\s*(?=<!-- SEO_LATEST_START -->)/m,'');
}

function latestCards(list,limit=6){
  return sortPosts(list).slice(0,limit).map(p=>`<a href="/posts/${esc(p.slug)}.html" style="display:block;padding:15px 16px;border:1px solid #d9e0ea;border-radius:10px;background:#fff;text-decoration:none;color:#20242b"><small style="display:block;color:#36a9e1;font-weight:800;margin-bottom:5px">${esc(p.category)} · ${esc(p.date)}</small><strong style="display:block;line-height:1.45">${esc(p.title)}</strong></a>`).join('\n');
}

function buildLatestSection(list,title='최신 법률정보'){
  if(!list.length) return '';
  return `<section class="section white" aria-labelledby="seo-latest-title" style="padding-top:34px;padding-bottom:54px"><div class="container"><div class="label">LATEST LEGAL POSTS</div><h2 id="seo-latest-title" class="title" style="font-size:30px">${esc(title)}</h2><p class="desc">최근 작성한 법률정보를 개별 글로 바로 확인할 수 있습니다.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px">${latestCards(list,6)}</div><div style="margin-top:18px"><a class="btn btn-border" href="/posts.html">전체 법률정보 보기</a></div></div></section>`;
}

function tokens(p){
  return new Set(`${p.title} ${p.keywords} ${p.summary}`.toLowerCase().replace(/[^0-9a-z가-힣]+/g,' ').split(/\s+/).filter(x=>x.length>=2));
}

function relatedPosts(p){
  const a=tokens(p);
  const scored=posts.filter(x=>x.slug!==p.slug).map(x=>{
    const b=tokens(x); let score=x.category===p.category?20:0;
    for(const t of a) if(b.has(t)) score+=1;
    return {post:x,score};
  }).sort((x,y)=>y.score-x.score || String(y.post.date).localeCompare(String(x.post.date)));
  const selected=scored.filter(x=>x.score>0).slice(0,4).map(x=>x.post);
  if(selected.length<4){
    for(const p2 of sortPosts(posts.filter(x=>x.slug!==p.slug))){
      if(!selected.some(x=>x.slug===p2.slug)) selected.push(p2);
      if(selected.length===4) break;
    }
  }
  return selected.slice(0,4);
}

function gitModifiedDate(relPath,fallback){
  try{
    const out=execFileSync('git',['log','-1','--format=%cs','--',relPath],{cwd:root,encoding:'utf8'}).trim();
    return /^\d{4}-\d{2}-\d{2}$/.test(out)?out:fallback;
  }catch{return fallback;}
}

function plainTextFromArticle(html){
  const m=html.match(/<div class="article-body">([\s\S]*?)<\/div>\s*<!-- SEO_RELATED_POSTS_START -->/i)
    || html.match(/<div class="article-body">([\s\S]*?)<\/div>\s*<div class="related">/i);
  if(!m) return '';
  return m[1].replace(/<script[\s\S]*?<\/script>/gi,' ').replace(/<style[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/gi,' ').replace(/&amp;/gi,'&').replace(/\s+/g,' ').trim();
}

function optimizedDescription(p,html){
  const summary=clean(p.summary);
  if(summary.length>=50 && summary.length<=165) return summary;
  const text=plainTextFromArticle(html);
  const source=text || summary || p.title;
  const out=source.slice(0,160).trim();
  return out.length<30 ? `${p.title} 관련 절차와 핵심 내용을 정리한 등기로 법률정보입니다.`.slice(0,160) : out;
}

function replaceMeta(html,name,value){
  const safe=esc(value);
  const re=new RegExp(`<meta\\s+name=["']${name}["']\\s+content=["'][^"']*["']\\s*\\/?>(?![^<]*<meta)`,'i');
  if(re.test(html)) return html.replace(re,`<meta name="${name}" content="${safe}">`);
  return html.replace('</head>',`<meta name="${name}" content="${safe}">\n</head>`);
}

function replaceOg(html,prop,value){
  const safe=esc(value);
  const re=new RegExp(`<meta\\s+property=["']${prop}["']\\s+content=["'][^"']*["']\\s*\\/?>(?![^<]*<meta)`,'i');
  if(re.test(html)) return html.replace(re,`<meta property="${prop}" content="${safe}">`);
  return html.replace('</head>',`<meta property="${prop}" content="${safe}">\n</head>`);
}

function enhanceImages(html,p){
  return html.replace(/<img\b([^>]*?)>/gi,(full,attrs)=>{
    if(/class=["'][^"']*social/i.test(attrs)) return full;
    let a=attrs;
    if(!/\balt\s*=/i.test(a)) a+=` alt="${esc(p.title)} 관련 이미지"`;
    else a=a.replace(/\balt\s*=\s*["']\s*["']/i,`alt="${esc(p.title)} 관련 이미지"`);
    if(!/\bloading\s*=/i.test(a)) a+=' loading="lazy"';
    if(!/\bdecoding\s*=/i.test(a)) a+=' decoding="async"';
    return `<img${a}>`;
  });
}

function updateSitemapLastmod(p,modified){
  const sitemap=path.join(root,'sitemap.xml');
  if(!fs.existsSync(sitemap)) return;
  let xml=fs.readFileSync(sitemap,'utf8');
  const url=`${BASE}/posts/${p.slug}.html`;
  const escaped=url.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  const re=new RegExp(`(<loc>${escaped}<\\/loc>\\s*<lastmod>)[^<]+(<\\/lastmod>)`);
  if(re.test(xml)){
    xml=xml.replace(re,`$1${modified}$2`);
    fs.writeFileSync(sitemap,xml);
  }
}

function writeIfChanged(file,next){
  const current=fs.readFileSync(file,'utf8');
  if(current!==next) fs.writeFileSync(file,next);
}

const indexPath=path.join(root,'index.html');
if(fs.existsSync(indexPath)){
  let html=fs.readFileSync(indexPath,'utf8');
  html=removeLegacyLegalInfoSection(html);
  html=replaceMarked(html,'SEO_LATEST',buildLatestSection(posts),'\n<section class="contact"');
  writeIfChanged(indexPath,html);
}

const categoryPages=[
  ['inheritance.html',['상속등기','상속재산분할'],'상속 관련 최신 글'],
  ['renunciation.html',['상속포기·한정승인'],'상속포기·한정승인 관련 최신 글'],
  ['corporate.html',['법인등기'],'법인등기 관련 최신 글'],
  ['realestate.html',['부동산등기'],'부동산등기 관련 최신 글'],
  ['family.html',['가사'],'가사 관련 최신 글']
];

for(const [file,cats,title] of categoryPages){
  const full=path.join(root,file);
  if(!fs.existsSync(full)) continue;
  const related=posts.filter(x=>cats.includes(x.category));
  let html=fs.readFileSync(full,'utf8');
  html=replaceMarked(html,'SEO_CATEGORY_LINKS',buildLatestSection(related,title),'\n<footer');
  writeIfChanged(full,html);
}

const audit=[];
for(const p of posts){
  const relFile=`posts/${p.slug}.html`;
  const file=path.join(root,relFile);
  if(!fs.existsSync(file)){
    audit.push({slug:p.slug,status:'warning',issues:['HTML 파일 없음']});
    continue;
  }

  let html=fs.readFileSync(file,'utf8');
  const url=`${BASE}/posts/${p.slug}.html`;
  const image=abs(p.thumbnail);
  const modified=gitModifiedDate(relFile,p.date||todayKST());
  const description=optimizedDescription(p,html);

  html=replaceMeta(html,'description',description);
  html=replaceOg(html,'og:description',description);
  html=enhanceImages(html,p);

  const articleLd={
    '@context':'https://schema.org','@type':'Article',headline:p.title,description,
    datePublished:p.date,dateModified:modified,
    mainEntityOfPage:{'@type':'WebPage','@id':url},
    author:{'@type':'Person',name:'현재두'},
    publisher:{'@type':'Organization',name:'현재두 법무사 사무소',url:BASE},
    ...(image?{image:[image]}:{})
  };
  const breadcrumbLd={
    '@context':'https://schema.org','@type':'BreadcrumbList',
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

  const rel=relatedPosts(p);
  const relatedBlock=rel.length?`<section aria-labelledby="related-posts-title" style="margin-top:34px;padding-top:24px;border-top:1px solid #e5e7eb"><h2 id="related-posts-title" style="font-size:22px;margin:0 0 14px">같이 보면 좋은 글</h2><div style="display:grid;gap:9px">${rel.map(x=>`<a href="/posts/${esc(x.slug)}.html" style="display:block;padding:12px 14px;border:1px solid #d9e0ea;border-radius:9px;text-decoration:none"><small style="color:#36a9e1;font-weight:800">${esc(x.category)}</small><strong style="display:block;margin-top:3px;color:#20242b;line-height:1.45">${esc(x.title)}</strong></a>`).join('')}</div></section>`:'';
  html=replaceMarked(html,'SEO_RELATED_POSTS',relatedBlock,'<div class="related">');

  const issues=[];
  if(!/<link\s+rel=["']canonical["']/i.test(html)) issues.push('canonical 누락');
  if(!/<meta\s+name=["']description["']/i.test(html)) issues.push('description 누락');
  if(/<meta\s+name=["']robots["'][^>]*noindex/i.test(html)) issues.push('noindex 발견');
  if(!/"@type":"Article"/.test(html)) issues.push('Article 구조화데이터 누락');
  if(!/"@type":"BreadcrumbList"/.test(html)) issues.push('Breadcrumb 구조화데이터 누락');
  if(rel.length===0) issues.push('내부 관련글 없음');

  writeIfChanged(file,html);
  updateSitemapLastmod(p,modified);
  audit.push({slug:p.slug,status:issues.length?'warning':'ok',issues,modified,related:rel.map(x=>x.slug)});
}

const report={generatedAt:new Date().toISOString(),totalPosts:posts.length,ok:audit.filter(x=>x.status==='ok').length,warnings:audit.filter(x=>x.status!=='ok').length,items:audit};
fs.writeFileSync(path.join(root,'data','seo-report.json'),JSON.stringify(report,null,2)+'\n');

console.log(`SEO 자동화 완료: ${posts.length}개 글 / 정상 ${report.ok} / 경고 ${report.warnings}`);
