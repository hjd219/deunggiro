import fs from 'node:fs';
const p='assets/home.css';
let s=fs.readFileSync(p,'utf8');
const changes=[
['  #calculator .calc-card{min-height:175px;padding:18px;grid-template-columns:minmax(0,1fr) 92px;gap:10px;border-radius:18px}','  #calculator .calc-card{min-height:175px;padding:18px;grid-template-columns:minmax(0,1fr) 92px;gap:10px;border-radius:18px;align-items:start}'],
['  #calculator .calc-action{padding-left:9px}','  #calculator .calc-action{padding-left:9px;align-self:start}'],
['  #calculator .calculator-icon{width:76px;height:92px}','  #calculator .calculator-icon{width:64px;height:92px}'],
['  #calculator .calculator-icon{width:68px;height:84px}','  #calculator .calculator-icon{width:64px;height:84px}']
];
for(const [a,b] of changes){const n=s.split(a).length-1;if(n!==1)throw new Error(`target count ${n}: ${a}`);s=s.replace(a,b)}
fs.writeFileSync(p,s);
