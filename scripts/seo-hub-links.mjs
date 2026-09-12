import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const posts=JSON.parse(fs.readFileSync(path.join(root,'data','posts.json'),'utf8'));

const CORE={
  inheritance:{href:'/posts/inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban.html',label:'인천 상속등기 절차·필요서류·취득세 총정리'},
  renunciation:{href:'/posts/inheritance-renunciation-incheon-procedure-documents-1ifftk.html',label:'인천 상속포기 절차·기간·필요서류 총정리'},
  renunciationAll:{href:'/posts/inheritance-renunciation-limited-acceptance-incheon-procedure-1podzk.html',label:'상속포기·한정승인 3개월 기한과 절차 총정리'},
  corporate:{href:'/posts/naver-224258524096.html',label:'1인 법인 설립 절차·비용·필요서류 총정리'},
  realestate:{href:'/realestate.html',label:'부동산등기 주요 절차 안내'},
  family:{href:'/family.html',label:'가사사건 주요 절차 안내'}
};

function pickCore(p){
  const text=`${p.title||''} ${p.keywords||''} ${p.summary||''}`;
  if(p.category==='상속등기'||p.category==='상속재산분할') return CORE.inheritance;
  if(p.category==='상속포기·한정승인'){
    if(/한정승인|특별한정승인/.test(text) && !/상속포기/.test(text)) return CORE.renunciationAll;
    return CORE.renunciation;
  }
  if(p.category==='법인등기') return CORE.corporate;
  if(p.category==='부동산등기') return CORE.realestate;
  if(p.category==='가사') return CORE.family;
  return null;
}

function esc(s){return String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
function replaceMarked(html,block){
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
  const block=core.href===self?'':`<aside aria-label="핵심 안내" style="margin:28px 0 4px;padding:16px 18px;background:#f4f9fd;border:1px solid #cfe9f7;border-radius:9px"><strong style="display:block;margin-bottom:6px;color:#20242b">핵심 안내</strong><a href="${esc(core.href)}" style="color:#1677a8;font-weight:800;text-decoration:underline">${esc(core.label)} →</a></aside>`;
  const next=replaceMarked(html,block);
  if(next!==html){fs.writeFileSync(file,next);changed++;}
}
console.log(`SEO core links: changed=${changed}, skipped=${skipped}`);
