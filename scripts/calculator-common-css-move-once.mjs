import fs from 'node:fs';
const core='assets/site-shell-core.css';
const pages=['acquisition-calculator.html','corporate-calculator.html'];
let c=fs.readFileSync(core,'utf8');
const block='/* CALCULATOR_ENGLISH_LABELS_OFF_V1 */\nbody:has(.wrap) .hero>b,body:has(.wrap) .step{display:none!important}\nbody:has(.wrap) .hero h1{margin-top:0!important}\n';
if((c.split(block).length-1)!==1) throw new Error('calculator common block mismatch');
c=c.replace(block,'');
fs.writeFileSync(core,c);
const link='<link rel="stylesheet" href="/assets/calculator-common.css?v=20260913">';
for(const page of pages){let p=fs.readFileSync(page,'utf8');if(p.includes(link)) throw new Error(page+' already linked');const anchor='<link rel="stylesheet" href="/assets/site-shell.css?v=20260910-2135">';if((p.split(anchor).length-1)!==1) throw new Error(page+' shell link mismatch');p=p.replace(anchor,anchor+'\n'+link);fs.writeFileSync(page,p);}
console.log('moved calculator-only shared CSS out of site shell core');
