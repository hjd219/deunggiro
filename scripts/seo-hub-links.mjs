import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const posts=JSON.parse(fs.readFileSync(path.join(root,'data','posts.json'),'utf8'));

const CATEGORY_HUBS={
  '상속등기':{href:'/inheritance.html',label:'상속등기 핵심안내'},
  '상속재산분할':{href:'/inheritance.html',label:'상속등기 핵심안내'},
  '상속포기·한정승인':{href:'/renunciation.html',label:'상속포기·한정승인 핵심안내'},
  '법인등기':{href:'/corporate.html',label:'법인등기 핵심안내'},
  '부동산등기':{href:'/realestate.html',label:'부동산등기 핵심안내'},
  '가사':{href:'/family.html',label:'가사 핵심안내'}
};

function pickCore(p){
  return CATEGORY_HUBS[String(p.category||'').trim()]||null;
}

function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
function removeLegacyHub(html){
  // 구형 SEO_HUB_LINK는 현재 SEO_CORE_LINK와 같은 업무 허브를 중복 연결하므로 제거한다.
  return html.replace(/<!-- SEO_HUB_LINK_START -->[\\s\\S]*?<!-- SEO_HUB_LINK_END -->\\s*/gm,'');
}
function replaceMarked(html,block){
  html=removeLegacyHub(html);
  const start='<!-- SEO_CORE_LINK_START -->',end='<!-- SEO_CORE_LINK_END -->';
  const marked=`${start}\n${block}\n${end}`;
  const re=new RegExp(`${start}[\\s\\S]*?${end}`,'m');
  if(re.test(html)) return html.replace(re,marked);
  const marker='<!-- SEO_RELATED_POSTS_START -->';
  const idx=html.indexOf(marker);
  if(idx<0) return html;
  return html.slice(0,idx)+marked+'\n'+html.slice(idx);
}

let changed=0,skipped=0;
for(const p of posts){
  const core=pickCore(p); if(!core){skipped++;continue;}
  const rel=`posts/${p.slug}.html`,file=path.join(root,rel);
  if(!fs.existsSync(file)){skipped++;continue;}
  let html=fs.readFileSync(file,'utf8');
  const self=`/posts/${p.slug}.html`;
  const target=core;
  const block=`<aside class="seo-core-link" aria-label="핵심 안내"><div class="seo-link-kicker">핵심 안내</div><a href="${esc(target.href)}">${esc(target.label)} <span aria-hidden="true">→</span></a></aside>`;
  const next=replaceMarked(html,block);
  if(next!==html){fs.writeFileSync(file,next);changed++;}
}
console.log(`SEO core links: changed=${changed}, skipped=${skipped}`);
