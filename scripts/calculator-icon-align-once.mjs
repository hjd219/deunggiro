import fs from 'node:fs';
const p='assets/home.css';
let s=fs.readFileSync(p,'utf8');
const old1='  #calculator .calc-card{min-height:175px;padding:18px;grid-template-columns:minmax(0,1fr) 92px;gap:10px;border-radius:18px}';
const new1='  #calculator .calc-card{min-height:175px;padding:18px;grid-template-columns:minmax(0,1fr) 92px;gap:10px;border-radius:18px;align-items:start}';
const old2='  #calculator .calc-action{padding-left:9px}';
const new2='  #calculator .calc-action{padding-left:9px;align-self:start}';
const old3='  #calculator .calculator-icon{width:76px;height:92px}';
const new3='  #calculator .calculator-icon{width:64px;height:92px}';
for(const [a,b] of [[old1,new1],[old2,new2],[old3,new3]]){
  if((s.split(a).length-1)!==1) throw new Error('target not unique: '+a);
  s=s.replace(a,b);
}
fs.writeFileSync(p,s);
console.log('calculator mobile alignment/icon updated');
