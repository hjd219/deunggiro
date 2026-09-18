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
  const seen=new Set(),valid=[];
  raw.forEach(p=>{
    if(!p||typeof p!=='object') return;
    const item={...p,title:clean(p.title),category:clean(p.category),date:clean(p.date),slug:clean(p.slug),keywords:clean(p.keywords),summary:clean(p.summary),thumbnail:clean(p.thumbnail)};
    if(!item.title||!item.category||!item.date||!item.slug)return;
    if(!/^\d{4}-\d{2}-\d{2}$/.test(item.date))return;
    if(!/^[a-z0-9][a-z0-9-]*$/i.test(item.slug))return;
    if(seen.has(item.slug))throw new Error(`중복 slug가 있습니다: ${item.slug}`);
    seen.add(item.slug);valid.push(item);
  });
  return valid;
}
const posts=loadPosts();
if(!posts.length)throw new Error('유효한 게시글이 없습니다.');

function replaceMarked(html,name,block,before){
  const start=`<!-- ${name}_START -->`,end=`<!-- ${name}_END -->`;
  const re=new RegExp(`${start}[\\s\\S]*?${end}`,'m');
  const marked=`${start}\n${block}\n${end}`;
  if(re.test(html))return html.replace(re,marked);
  const idx=html.indexOf(before);if(idx<0)return html;
  return html.slice(0,idx)+marked+'\n'+html.slice(idx);
}

/* 과거 후처리에서 HTML 주석 기호가 사라지며 SEO_* 마커가 본문에 글자로 노출된 경우를 정리한다.
   게시글마다 기존 자동 생성 breadcrumb/구조화데이터를 제거한 뒤 아래에서 정확히 한 번만 다시 삽입한다. */
function sanitizeSeoArtifacts(html){
  for(const name of ['SEO_STRUCTURED_DATA','SEO_BREADCRUMB']){
    const start=`<!-- ${name}_START -->`,end=`<!-- ${name}_END -->`;
    const marked=new RegExp(`${start}[\\s\\S]*?${end}`,'g');
    html=html.replace(marked,'');
  }
  html=html.replace(/(?:<!--\s*)?SEO_(?:STRUCTURED_DATA|BREADCRUMB)_(?:START|END)(?:\s*-->)?/g,'');
  html=html.replace(/<nav\b[^>]*aria-label=["']breadcrumb["'][^>]*>[\s\S]*?<\/nav>\s*/gi,'');
  html=html.replace(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>[\s\S]*?<\/script>\s*/gi,'');
  return html;
}

/* 업무 허브(index/inheritance/renunciation/corporate/realestate/family)는
   seo-auto가 본문/최신글 영역을 생성·수정하지 않는다.
   허브 구조는 수동 관리하며, 이 자동화는 개별 posts SEO만 처리한다. */

const audit=[];
for(const p of posts){
  const relFile=`posts/${p.slug}.html`,file=path.join(root,relFile);
  if(!fs.existsSync(file)){audit.push({slug:p.slug,status:'warning',issues:['HTML 파일 없음']});continue}
  let html=sanitizeSeoArtifacts(fs.readFileSync(file,'utf8'));
  const url=`${BASE}/posts/${p.slug}.html`,image=abs(p.thumbnail),modified=gitModifiedDate(relFile,p.date||todayKST()),description=optimizedDescription(p,html);
  html=replaceMeta(html,'description',description);html=replaceOg(html,'og:description',description);html=enhanceImages(html,p);
  const articleLd={'@context':'https://schema.org','@type':'Article',headline:p.title,description,datePublished:p.date,dateModified:modified,mainEntityOfPage:{'@type':'WebPage','@id':url},author:{'@type':'Person',name:'현재두'},publisher:{'@type':'Organization',name:'현재두 법무사 사무소',url:BASE},...(image?{image:[image]}:{})};
  const breadcrumbLd={'@context':'https://schema.org','@type':'BreadcrumbList',itemListElement:[{'@type':'ListItem',position:1,name:'홈',item:BASE+'/'},{'@type':'ListItem',position:2,name:'법률정보',item:BASE+'/posts.html'},{'@type':'ListItem',position:3,name:p.category,item:BASE+'/posts.html'},{'@type':'ListItem',position:4,name:p.title,item:url}]};
  const ldBlock=`<script type="application/ld+json">${JSON.stringify(articleLd).replace(/<\//g,'<\\/')}</script>\n<script type="application/ld+json">${JSON.stringify(breadcrumbLd).replace(/<\//g,'<\\/')}</script>`;
  html=replaceMarked(html,'SEO_STRUCTURED_DATA',ldBlock,'\n</head>');
  const crumb=`<nav aria-label="breadcrumb" style="max-width:850px;margin:0 auto 12px;padding:0 4px;font-size:13px;color:#68717d"><a href="/">홈</a> &gt; <a href="/posts.html">법률정보</a> &gt; <span>${esc(p.category)}</span></nav>`;
  html=replaceMarked(html,'SEO_BREADCRUMB',crumb,'<article class="article">');
  const rel=relatedPosts(p),relatedBlock=rel.length?`<section aria-labelledby="related-posts-title" style="margin-top:34px;padding-top:24px;border-top:1px solid #e5e7eb"><h2 id="related-posts-title" style="font-size:22px;margin:0 0 14px">같이 보면 좋은 글</h2><div style="display:grid;gap:9px">${rel.map(x=>`<a href="/posts/${esc(x.slug)}.html" style="display:block;padding:12px 14px;border:1px solid #d9e0ea;border-radius:9px;text-decoration:none"><small style="color:#36a9e1;font-weight:800">${esc(x.category)}</small><strong style="display:block;margin-top:3px;color:#20242b;line-height:1.45">${esc(x.title)}</strong></a>`).join('')}</div></section>`:'';
  html=replaceMarked(html,'SEO_RELATED_POSTS',relatedBlock,'<div class="related">');
  const issues=[];
  if(!/<link\b[^>]*rel=["']canonical["']/i.test(html))issues.push('canonical 누락');
  if(!/<meta\s+name=["']description["']/i.test(html))issues.push('description 누락');
  if(/<meta\s+name=["']robots["'][^>]*noindex/i.test(html))issues.push('noindex 발견');
  if(!/"@type":"Article"/.test(html))issues.push('Article 구조화데이터 누락');
  if(!/"@type":"BreadcrumbList"/.test(html))issues.push('Breadcrumb 구조화데이터 누락');
  if(rel.length===0)issues.push('내부 관련글 없음');
  if(/SEO_(?:STRUCTURED_DATA|BREADCRUMB)_(?:START|END)(?!\s*-->)/.test(html))issues.push('SEO 마커 노출 위험');
  writeIfChanged(file,html);updateSitemapLastmod(p,modified);audit.push({slug:p.slug,status:issues.length?'warning':'ok',issues,modified,related:rel.map(x=>x.slug)});
}
const report={generatedAt:new Date().toISOString(),totalPosts:posts.length,ok:audit.filter(x=>x.status==='ok').length,warnings:audit.filter(x=>x.status!=='ok').length,items:audit};
fs.writeFileSync(path.join(root,'data','seo-report.json'),JSON.stringify(report,null,2)+'\n');
console.log(`SEO 자동화 완료: ${posts.length}개 글 / 정상 ${report.ok} / 경고 ${report.warnings}`);
