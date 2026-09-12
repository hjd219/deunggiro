import fs from 'node:fs';

const cssPath='assets/home.css';
let css=fs.readFileSync(cssPath,'utf8');

const oldRule='  #calculator .calc-card h3{font-size:17px;letter-spacing:-.8px;margin-bottom:12px;transform:translateY(-2px)}';
const newRule='  #calculator .calc-card h3{font-size:17px;letter-spacing:-.8px;margin-bottom:12px;transform:translateY(6px)}';
if((css.split(oldRule).length-1)!==1) throw new Error('mobile calculator title target mismatch');
css=css.replace(oldRule,newRule);

fs.writeFileSync(cssPath,css);
console.log('calculator title moved down 8px from current position');