import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const BASE='https://www.deunggiro.kr';
const postsPath=path.join(root,'data','posts.json');

const xml=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&apos;');
const clean=s=>String(s??'').replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
const rfc822=d=>{
  const m=String(d||'').match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if(!m) return new Date().toUTCString();
  return new Date(`${m[1]}-${m[2]}-${m[3]}T00:00:00+09:00`).toUTCString();
};

if(!fs.existsSync(postsPath)) throw new Error('data/posts.json 파일이 없습니다.');
const raw=JSON.parse(fs.readFileSync(postsPath,'utf8'));
if(!Array.isArray(raw)) throw new Error('data/posts.json 형식이 올바르지 않습니다.');


const decodeEntities = text => String(text||'').replace(/&(#x[0-9a-f]+|#\d+|[a-z][a-z0-9]+);/gi,(full,entity)=>{
  if(entity.startsWith('#')){
    const code=entity.slice(1).toLowerCase().startsWith('x')?parseInt(entity.slice(2),16):parseInt(entity.slice(1),10);
    return code>0 && code<=0x10ffff && !(code>=0xd800 && code<=0xdfff)?String.fromCodePoint(code):'';
  }
  const named={amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' ',hellip:'…',mdash:'—',ndash:'–',bull:'•',lsquo:'‘',rsquo:'’',ldquo:'“',rdquo:'”',copy:'©'};
  return named[entity.toLowerCase()]??full;
});

let fullTextCount=0;
let summaryFallbackCount=0;
// Read only the published article body; never modify the article HTML.
function articleText(slug,summary){
  const fallback=clean(summary)||'관련 법률정보입니다.';
  const safe=String(slug||'');
  if(!/^[a-zA-Z0-9_-]+$/.test(safe)){summaryFallbackCount++;return fallback;}
  const filename=path.join(root,'posts',safe+'.html');
  if(!fs.existsSync(filename)){summaryFallbackCount++;return fallback;}
  try{
    const html=fs.readFileSync(filename,'utf8');
    const opening=/<div\b[^>]*\bclass\s*=\s*["'][^"']*\barticle-body\b[^"']*["'][^>]*>/i.exec(html);
    if(!opening){summaryFallbackCount++;return fallback;}
    const start=opening.index+opening[0].length;
    const divTags=/<\/?div\b[^>]*>/gi;
    divTags.lastIndex=start;
    let depth=1, end=-1,match;
    while((match=divTags.exec(html))){
      if(/^<\/div\b/i.test(match[0]))depth--;
      else if(!/\/>$/.test(match[0]))depth++;
      if(depth===0){end=match.index;break;}
    }
    if(end<start){summaryFallbackCount++;return fallback;}
    const body=html.slice(start,end)
      .replace(/<!--[\s\S]*?-->/g,'')
      .replace(/<(script|style|noscript|template|svg|iframe)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,'')
      .replace(/<(?:br|hr)\b[^>]*\/?>/gi,'\n')
      .replace(/<\/(?:p|div|li|h[1-6]|ul|ol|blockquote|tr|table|section|article)>/gi,'\n')
      .replace(/<[^>]*>/g,' ');
    const text=decodeEntities(body)
      .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\uFFFE\uFFFF]/g,'')
      .replace(/[^\S\n]+/g,' ')
      .replace(/ *\n */g,'\n')
      .replace(/\n{3,}/g,'\n\n')
      .trim();
    if(text.length<30){summaryFallbackCount++;return fallback;}
    fullTextCount++;
    return text;
  }catch(error){
    console.warn('RSS body extraction failed for',safe,error.message);
    summaryFallbackCount++;
    return fallback;
  }
}

const posts=raw
  .filter(p=>p && p.slug && p.title && /^\d{4}-\d{2}-\d{2}$/.test(String(p.date||'')))
  .sort((a,b)=>String(b.date).localeCompare(String(a.date)))
  .slice(0,100);

if(!posts.length) throw new Error('RSS에 넣을 게시글이 없습니다.');

const items=posts.map(p=>{
  const link=`${BASE}/posts/${encodeURIComponent(String(p.slug))}.html`;
  const desc=articleText(p.slug,p.summary);
  return `  <item>\n    <title>${xml(p.title)}</title>\n    <link>${xml(link)}</link>\n    <guid isPermaLink="true">${xml(link)}</guid>\n    <pubDate>${rfc822(p.date)}</pubDate>\n    <category>${xml(p.category||'법률정보')}</category>\n    <description>${xml(desc)}</description>\n  </item>`;
}).join('\n');

const rss=`<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n  <title>등기로 | 현재두 법무사 사무소 법률정보</title>\n  <link>${BASE}/</link>\n  <description>상속등기·상속포기·한정승인·법인등기·부동산등기 관련 최신 법률정보</description>\n  <language>ko-KR</language>\n  <atom:link href="${BASE}/rss.xml" rel="self" type="application/rss+xml"/>\n  <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>\n${items}\n</channel>\n</rss>\n`;

const output=path.join(root,'rss.xml');
const old=fs.existsSync(output)?fs.readFileSync(output,'utf8'):'';
const ignoreBuildDate=text=>text.replace(/<lastBuildDate>[^<]*<\/lastBuildDate>/,'<lastBuildDate>UNCHANGED</lastBuildDate>');
if(old && ignoreBuildDate(old)===ignoreBuildDate(rss)){
  console.log('RSS 내용 변동 없음: 기존 생성일과 파일 유지');
}else{
  const bytes=Buffer.byteLength(rss,'utf8');
  if(bytes>=10*1024*1024)throw new Error('RSS 10MB 제한 초과: 기존 RSS 파일 유지 ('+bytes+' bytes)');
  fs.writeFileSync(output,rss,'utf8');
  console.log('RSS 갱신: '+posts.length+'개 글, '+bytes+' bytes');
}
console.log('RSS 본문 추출 '+fullTextCount+'개 / 요약 대체 '+summaryFallbackCount+'개');
