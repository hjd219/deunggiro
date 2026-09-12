import fs from 'node:fs';

const p='assets/site-shell-core.css';
let css=fs.readFileSync(p,'utf8');
const before=css;

// 1) 뒤의 DETAIL_CATEGORY_BADGE_SOFT_V1이 동일 selector/importance로 덮는 구형 진한 배지 블록 제거.
const badge=/\/\* RELATED_BADGE_PRIMARY_BG_V1[\s\S]*?(?=\/\* DETAIL_CATEGORY_BADGE_SOFT_V1)/;
if(!badge.test(css)) throw new Error('RELATED_BADGE_PRIMARY_BG_V1 block not found');
css=css.replace(badge,'');

// 2) 현재 한 줄 형태의 모바일 공통 16px 여백 선언은 유지한다.
// 과거 스크립트가 줄바꿈 형태만 가정해 실패했으므로, 검증 가능한 죽은 규칙만 제거한다.
if(css===before) throw new Error('No changes');
fs.writeFileSync(p,css);
console.log('phase2 structure cleanup complete: obsolete related badge block removed');
