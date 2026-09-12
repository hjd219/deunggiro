import fs from 'node:fs';

const cssPath='assets/home.css';
const htmlPath='index.html';
let css=fs.readFileSync(cssPath,'utf8');
let html=fs.readFileSync(htmlPath,'utf8');

const oldMobile=`  #calculator .calc-card h3{font-size:17px;letter-spacing:-.8px;margin-bottom:12px}\n  #calculator .calc-types{font-size:12.5px;color:#263745;line-height:1.55;margin-bottom:8px}\n  #calculator .calc-point{font-size:12.5px;color:#263745;line-height:1.5}\n  #calculator .calc-action{padding-left:9px;align-self:start}\n  #calculator .calculator-icon{width:64px;height:92px}`;
const newMobile=`  #calculator .calc-card h3{font-size:17px;letter-spacing:-.8px;margin-bottom:12px;transform:translateY(-2px)}\n  #calculator .calc-types{font-size:12.5px;color:#263745;line-height:1.55;margin-bottom:8px}\n  #calculator .calc-point{font-size:12.5px;color:#263745;line-height:1.5}\n  #calculator .calc-action{padding-left:9px;align-self:start}\n  #calculator .calculator-icon{width:60px;height:92px}`;
if(!css.includes(oldMobile)) throw new Error('mobile calculator target not found');
css=css.replace(oldMobile,newMobile);

const oldTiny='  #calculator .calculator-icon{width:64px;height:84px}';
const newTiny='  #calculator .calculator-icon{width:60px;height:84px}';
if((css.match(new RegExp(oldTiny.replace(/[.*+?^${}()|[\\]\\]/g,'\\$&'),'g'))||[]).length!==1) throw new Error('tiny icon target count mismatch');
css=css.replace(oldTiny,newTiny);

const marker='</body>';
if(!html.includes(marker)) throw new Error('body close not found');
if(html.includes('CALCULATOR_DISPLAY_ROLL_V1')) throw new Error('calculator animation already exists');
const js=`\n<script>\n/* CALCULATOR_DISPLAY_ROLL_V1 */\n(()=>{\n  const displays=[...document.querySelectorAll('#calculator .calculator-icon text:first-of-type')];\n  if(!displays.length) return;\n  const reduce=window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;\n  const finish=()=>displays.forEach(el=>el.textContent='9,999');\n  if(reduce){finish();return;}\n  let started=false;\n  const run=()=>{\n    if(started) return; started=true;\n    const start=performance.now(), duration=1400, target=9999;\n    const tick=now=>{\n      const p=Math.min(1,(now-start)/duration);\n      const eased=1-Math.pow(1-p,3);\n      const value=Math.round(target*eased).toLocaleString('ko-KR');\n      displays.forEach(el=>el.textContent=value);\n      if(p<1) requestAnimationFrame(tick); else finish();\n    };\n    requestAnimationFrame(tick);\n  };\n  const section=document.getElementById('calculator');\n  if(!section){finish();return;}\n  if('IntersectionObserver' in window){\n    const io=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){io.disconnect();run();}},{threshold:.25});\n    io.observe(section);\n  }else run();\n})();\n</script>\n`;
html=html.replace(marker,js+marker);

fs.writeFileSync(cssPath,css);
fs.writeFileSync(htmlPath,html);
console.log('calculator visual 3-fix applied');