import fs from 'node:fs';
const p='index.html';
let s=fs.readFileSync(p,'utf8');
const old="document.querySelectorAll('#calculator .calculator-icon text:first-of-type')";
const next="document.querySelectorAll('#calculator .calculator-icon > text:first-of-type')";
if((s.split(old).length-1)!==1) throw new Error('display selector target mismatch');
s=s.replace(old,next);
fs.writeFileSync(p,s);
console.log('calculator animation now targets display text only');