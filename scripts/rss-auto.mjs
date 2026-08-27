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

const posts=raw
  .filter(p=>p && p.slug && p.title && /^\d{4}-\d{2}-\d{2}$/.test(String(p.date||'')))
  .sort((a,b)=>String(b.date).localeCompare(String(a.date)))
  .slice(0,30);

if(!posts.length) throw new Error('RSS에 넣을 게시글이 없습니다.');

const items=posts.map(p=>{
  const link=`${BASE}/posts/${encodeURIComponent(String(p.slug))}.html`;
  const desc=clean(p.summary)||`${clean(p.title)} 관련 법률정보입니다.`;
  return `  <item>\n    <title>${xml(p.title)}</title>\n    <link>${xml(link)}</link>\n    <guid isPermaLink="true">${xml(link)}</guid>\n    <pubDate>${rfc822(p.date)}</pubDate>\n    <category>${xml(p.category||'법률정보')}</category>\n    <description>${xml(desc)}</description>\n  </item>`;
}).join('\n');

const rss=`<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n<channel>\n  <title>등기로 | 현재두 법무사 사무소 법률정보</title>\n  <link>${BASE}/</link>\n  <description>상속등기·상속포기·한정승인·법인등기·부동산등기 관련 최신 법률정보</description>\n  <language>ko-KR</language>\n  <atom:link href="${BASE}/rss.xml" rel="self" type="application/rss+xml"/>\n  <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>\n${items}\n</channel>\n</rss>\n`;

fs.writeFileSync(path.join(root,'rss.xml'),rss,'utf8');
console.log(`RSS 자동 생성 완료: 최근 ${posts.length}개 글`);
