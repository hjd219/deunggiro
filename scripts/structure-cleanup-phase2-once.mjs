import fs from 'node:fs';

const p='assets/site-shell-core.css';
let css=fs.readFileSync(p,'utf8');
const before=css;

// 1) 뒤의 DETAIL_CATEGORY_BADGE_SOFT_V1이 동일 selector/importance로 완전히 덮는 구형 진한 배지 블록 제거.
const badge=/\/\* RELATED_BADGE_PRIMARY_BG_V1[\s\S]*?(?=\/\* DETAIL_CATEGORY_BADGE_SOFT_V1)/;
const m=css.match(badge);
if(!m) throw new Error('RELATED_BADGE_PRIMARY_BG_V1 block not found');
css=css.replace(badge,'');

// 2) MOBILE_POLISH_20260908_V1에서 동일하게 다시 선언되는 700px 공통 16px padding 중복만 제거.
const dup=`  .container{padding-left:16px!important;padding-right:16px!important}\n  .dg-shell-header .dg-shell-inner{padding-left:16px!important;padding-right:16px!important}\n  .dg-shell-contact .dg-shell-contact-grid,.dg-shell-footer .dg-shell-footer-grid{padding-left:16px!important;padding-right:16px!important}\n`;
const count=css.split(dup).length-1;
if(count!==1) throw new Error('Expected exact duplicate mobile padding group once, got '+count);
if(!css.includes('MOBILE_POLISH_20260908_V1')) throw new Error('canonical mobile polish block missing');
css=css.replace(dup,'');

if(css===before) throw new Error('No changes');
fs.writeFileSync(p,css);
console.log('phase2 structure cleanup complete');
