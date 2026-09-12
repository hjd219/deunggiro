import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const posts=JSON.parse(fs.readFileSync(path.join(root,'data','posts.json'),'utf8'));

const CORE={
  inheritance:{href:'/posts/inheritance-registration-acquisition-tax-incheon-procedure-doc-v9aban.html',label:'인천 상속등기 절차·필요서류·취득세 총정리'},
  missing:{href:'/inheritance-missing-heir.html',label:'연락두절 상속인이 있는 상속등기 안내'},
  minor:{href:'/inheritance-minor-heir.html',label:'미성년 상속인 상속등기 안내'},
  overseas:{href:'/inheritance-overseas-heir.html',label:'해외 거주·외국인 상속인 상속등기 안내'},
  substitute:{href:'/inheritance-substitute-succession.html',label:'대습상속 상속등기 안내'},
  division:{href:'/inheritance-division.html',label:'상속재산분할 안내'},
  renunciation:{href:'/posts/inheritance-renunciation-incheon-procedure-documents-1ifftk.html',label:'인천 상속포기 절차·기간·필요서류 총정리'},
  renunciationAll:{href:'/posts/inheritance-renunciation-limited-acceptance-incheon-procedure-1podzk.html',label:'상속포기·한정승인 3개월 기한과 절차 총정리'},
  corporate:{href:'/posts/naver-224258524096.html',label:'1인 법인 설립 절차·비용·필요서류 총정리'},
  realestate:{href:'/realestate.html',label:'부동산등기 주요 절차 안내'},
  family:{href:'/family.html',label:'가사사건 주요 절차 안내'}
};

function pickCore(p){
  const text=`${p.title||''} ${p.keywords||''} ${p.summary||''}`;
  if(p.category==='상속등기'||p.category==='상속재산분할'){
    if(/연락두절|행방불명|실종선고|실종자/.test(text)) return CORE.missing;
    if(/미성년|특별대리인/.test(text)) return CORE.minor;
    if(/미국|일본|캐나다|호주|해외|외국|시민권|영주권|재외국민|아포스티유|영사관/.test(text)) return CORE.overseas;
    if(/대습상속|대습상속인/.test(text)) return CORE.substitute;
    if(p.category==='상속재산분할'||/상속재산분할심판|기여분|특별수익/.test(text)) return CORE.division;
    return CORE.inheritance;
  }
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
