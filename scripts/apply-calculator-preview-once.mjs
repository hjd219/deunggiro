import fs from 'node:fs';

const homePath='assets/home.css';
const indexPath='index.html';
let home=fs.readFileSync(homePath,'utf8');
let index=fs.readFileSync(indexPath,'utf8');

const start='/* CALCULATOR */';
const end='/* CONTACT / FOOTER */';
const a=home.indexOf(start), b=home.indexOf(end);
if(a<0||b<0||b<=a) throw new Error('calculator CSS anchors not found');
if(home.indexOf(start,a+1)!==-1) throw new Error('duplicate calculator CSS anchor');

const css=`/* CALCULATOR */
#calculator{padding:72px 0 78px;background:var(--home-sky);margin-top:0;border-top:0;box-shadow:none}
#calculator .calculator-heading{margin-bottom:26px}
#calculator .title{font-size:36px;line-height:1.3;letter-spacing:-1px;margin:0 0 10px;font-weight:900;color:#18283c}
#calculator .title .calculator-brand{color:#159fd9}
#calculator .desc{font-size:16px;line-height:1.6;color:#3e4b58;margin:0 0 20px;word-break:keep-all}
#calculator .desc strong{color:#18283c;font-weight:900}
#calculator .calculator-usage{display:inline-block;background:#fff;border:1px solid #b7e2f5;border-radius:25px;padding:9px 16px;margin:0;font-weight:800;color:#445362;font-size:14px}
#calculator .calculator-usage[hidden]{display:none}
#calculator .calculator-usage strong{color:#199fd9;font-size:18px;margin-left:7px}
#calculator .calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
#calculator .calc-card{min-height:202px;background:#fff;border:1.5px solid #a9ddf3;border-radius:18px;padding:23px;display:grid;grid-template-columns:minmax(0,1fr) 112px;gap:16px;align-items:center;color:#18283c;box-shadow:none;text-decoration:none}
#calculator .calc-copy{min-width:0}
#calculator .calc-card h3{font-size:20px;font-weight:900;margin:0 0 12px;white-space:nowrap;letter-spacing:-.6px;line-height:1.35;color:#18283c}
#calculator .calc-card h3 strong{color:#159fd9}
#calculator .calc-types{font-size:13.5px;line-height:1.55;color:#334250;font-weight:750;margin:0 0 8px;word-break:keep-all}
#calculator .calc-point{font-size:14px;color:#334250;margin:0;line-height:1.5;font-weight:700;word-break:keep-all}
#calculator .calc-point strong{color:#159fd9;font-weight:900}
#calculator .calc-action{border-left:1px solid #d7ecf6;padding-left:15px;text-align:center}
#calculator .calculator-icon{width:88px;height:108px;margin:0 auto 5px;display:block}
#calculator .calculator-icon text{font-family:-apple-system,BlinkMacSystemFont,"Noto Sans KR","Malgun Gothic",sans-serif}
#calculator .calc-action-label{color:#168fc4;font-size:13px;font-weight:900;display:block;white-space:nowrap}
@media(hover:hover) and (pointer:fine){#calculator .calc-card:hover{border-color:#36a9e1}}
@media(max-width:700px){
  #calculator{padding:44px 0 48px}
  #calculator .calculator-heading{margin-bottom:26px}
  #calculator .title{font-size:26px;letter-spacing:-1px}
  #calculator .desc{font-size:14px;color:#2f3e4c;line-height:1.6;margin-bottom:20px}
  #calculator .calc-grid{grid-template-columns:1fr;gap:18px}
  #calculator .calc-card{min-height:175px;padding:18px;grid-template-columns:minmax(0,1fr) 92px;gap:10px;border-radius:18px}
  #calculator .calc-card h3{font-size:17px;letter-spacing:-.8px;margin-bottom:12px}
  #calculator .calc-types{font-size:12.5px;color:#263745;line-height:1.55;margin-bottom:8px}
  #calculator .calc-point{font-size:12.5px;color:#263745;line-height:1.5}
  #calculator .calc-action{padding-left:9px}
  #calculator .calculator-icon{width:76px;height:92px}
  #calculator .calc-action-label{font-size:12px}
}
@media(max-width:370px){
  #calculator .calc-card h3{font-size:15.5px}
  #calculator .calc-card{grid-template-columns:minmax(0,1fr) 82px;padding:15px}
  #calculator .calculator-icon{width:68px;height:84px}
}

`;
home=home.slice(0,a)+css+home.slice(b);

const sectionStart='<section class="section soft" id="calculator">';
const sectionEnd='</section>';
const s=index.indexOf(sectionStart);
if(s<0) throw new Error('calculator section start missing');
const e=index.indexOf(sectionEnd,s);
if(e<0) throw new Error('calculator section end missing');
const old=index.slice(s,e+sectionEnd.length);
if((old.match(/class="calc-card"/g)||[]).length!==2) throw new Error('expected exactly two calculator cards');
const svg1=old.match(/<svg class="calculator-icon"[\s\S]*?<\/svg>/)?.[0];
const svgMatches=[...old.matchAll(/<svg class="calculator-icon"[\s\S]*?<\/svg>/g)].map(m=>m[0]);
if(svgMatches.length!==2) throw new Error('expected two calculator SVGs');
const section=`<section class="section soft" id="calculator">
 <div class="container">
  <div class="calculator-heading">
   <h2 class="title"><span class="calculator-brand">등기로</span> 비용계산기</h2>
   <p class="desc"><strong>공과금과 법무사 보수를 포함한 예상 등기비용</strong>을 바로 확인할 수 있습니다.</p>
   <div class="calculator-usage" id="dg-calculator-usage" hidden>누적 계산기 이용자 <strong data-count>0회</strong></div>
  </div>
  <div class="calc-grid">
   <a class="calc-card" href="/acquisition-calculator.html?v=20260910-accountfix">
    <span class="calc-copy"><h3><strong>부동산 등기비용</strong> 바로 계산</h3><p class="calc-types">상속 · 증여 · 매매 · 이혼 재산분할</p><p class="calc-point"><strong>공과금 + 법무사 보수</strong>까지 한 번에</p></span>
    <span class="calc-action">${svgMatches[0]}<span class="calc-action-label">계산하기</span></span>
   </a>
   <a class="calc-card" href="/corporate-calculator.html?v=20260910-clean">
    <span class="calc-copy"><h3><strong>법인 등기비용</strong> 바로 계산</h3><p class="calc-types">설립 · 임원변경 · 상호/목적변경<br>증자 · 본점이전</p><p class="calc-point"><strong>공과금 + 법무사 보수</strong>까지 한 번에</p></span>
    <span class="calc-action">${svgMatches[1]}<span class="calc-action-label">계산하기</span></span>
   </a>
  </div>
 </div>
</section>`;
index=index.slice(0,s)+section+index.slice(e+sectionEnd.length);
index=index.replace('/assets/home.css?v=20260912-maintenance1','/assets/home.css?v=20260912-calculator-preview-final');
if(!index.includes('/assets/home.css?v=20260912-calculator-preview-final')) throw new Error('home CSS cache version not updated');
fs.writeFileSync(homePath,home);
fs.writeFileSync(indexPath,index);
console.log('calculator preview applied');
