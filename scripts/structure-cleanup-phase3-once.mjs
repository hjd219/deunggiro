import fs from 'node:fs';

const p='assets/site-shell-core.css';
let css=fs.readFileSync(p,'utf8');
const before=css;

// 700px 이하에서 뒤의 16px !important 규칙이 완전히 덮는 구형 14px contact/footer 여백만 제거.
const old='@media(max-width:700px){.dg-shell-contact{padding:38px 0!important}.dg-shell-contact .dg-shell-contact-grid,.dg-shell-footer .dg-shell-footer-grid{padding-left:14px;padding-right:14px}.dg-shell-contact h2{font-size:25px;line-height:1.4}';
const next='@media(max-width:700px){.dg-shell-contact{padding:38px 0!important}.dg-shell-contact h2{font-size:25px;line-height:1.4}';
if((css.split(old).length-1)!==1) throw new Error('legacy 14px mobile padding target mismatch');
css=css.replace(old,next);

// 최종 16px 공통 규칙은 반드시 유지되어야 한다.
const finalRule='.dg-shell-contact .dg-shell-contact-grid,.dg-shell-footer .dg-shell-footer-grid{padding-left:16px!important;padding-right:16px!important}';
if((css.split(finalRule).length-1)!==1) throw new Error('final 16px mobile padding rule missing or duplicated');

if(css===before) throw new Error('No changes');
fs.writeFileSync(p,css);
console.log('phase3 structure cleanup complete: superseded 14px mobile padding removed');