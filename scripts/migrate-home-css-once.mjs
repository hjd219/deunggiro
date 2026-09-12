import fs from 'node:fs';

const shellPath='assets/site-shell.css';
const homePath='assets/home.css';
let shell=fs.readFileSync(shellPath,'utf8');
let home=fs.readFileSync(homePath,'utf8');

const blocks=[
`/* HOME_MOBILE_HERO_BUTTON_TEXT_V1 - 메인 상단 3개 버튼 글자 크기 통일 */
@media (max-width:800px){
  body.home .hero .buttons .btn{
    font-size:16px!important;
    font-weight:900!important;
    line-height:1!important;
  }
  body.home .hero .buttons .btn span,
  body.home .hero .buttons .btn small{
    font-size:16px!important;
    font-weight:900!important;
    line-height:1!important;
  }
}

`,
`/* HOME_SERVICE_TITLE_V1 - 메인 업무카드 위에는 제목만 간결하게 표시 */
body.home #services .quick-grid{
  position:relative!important;
  padding-top:52px!important;
}
body.home #services .quick-grid::before{
  content:"업무안내";
  position:absolute;
  top:0;
  left:0;
  display:block;
  color:#20242b;
  font-size:28px;
  font-weight:900;
  line-height:1.3;
  letter-spacing:-.8px;
}
@media(max-width:800px){
  body.home #services .quick-grid{
    padding-top:44px!important;
  }
  body.home #services .quick-grid::before{
    font-size:23px;
    letter-spacing:-.6px;
  }
}

`,
`/* HOME_SERVICE_ALIGNMENT_V2 - 업무안내/카드/비용계산기 좌우 기준선 통일 */
body.home #services{
  width:100%!important;
  max-width:1180px!important;
  margin-left:auto!important;
  margin-right:auto!important;
  padding-left:22px!important;
  padding-right:22px!important;
  box-sizing:border-box!important;
}
body.home #services .quick-grid{
  width:100%!important;
  max-width:100%!important;
  margin:0!important;
  grid-template-columns:repeat(5,minmax(0,1fr))!important;
  gap:14px!important;
  padding-top:90px!important;
  box-sizing:border-box!important;
}
body.home #services .quick-grid::before{
  left:0!important;
  font-size:36px!important;
  line-height:1.25!important;
  letter-spacing:-1.5px!important;
}
body.home #services .quick-item.quick-rich{
  min-width:0!important;
  width:100%!important;
  max-width:100%!important;
  box-sizing:border-box!important;
}
@media(max-width:1000px){
  body.home #services{
    padding-left:22px!important;
    padding-right:22px!important;
  }
  body.home #services .quick-grid{
    grid-template-columns:repeat(2,minmax(0,1fr))!important;
  }
}
@media(max-width:800px){
  body.home #services{
    padding-left:18px!important;
    padding-right:18px!important;
  }
  body.home #services .quick-grid{
    grid-template-columns:1fr!important;
    gap:14px!important;
    padding-top:62px!important;
  }
  body.home #services .quick-grid::before{
    font-size:30px!important;
    letter-spacing:-1.2px!important;
  }
}
@media(max-width:480px){
  body.home #services{
    padding-left:14px!important;
    padding-right:14px!important;
  }
  body.home #services .quick-grid::before{
    font-size:27px!important;
  }
}

`,
`/* HOME_INTRO_DIRECT_REVIEW_V1 - 등기로 소개 팝업 직접 상담·검토 문구 */
body.home .dg-intro-copy::after{
  content:"상속등기 · 상속포기 · 한정승인 · 법인등기 사건은 직접 상담하고 검토합니다.";
  display:block;
  margin-top:10px;
  color:#27313d;
  font-size:17px;
  font-weight:800;
  line-height:1.9;
  word-break:keep-all;
}
@media(max-width:700px){
  body.home .dg-intro-copy::after{
    font-size:15px;
    line-height:1.8;
  }
}

`
];

for(const block of blocks){
  const count=shell.split(block).length-1;
  if(count!==1) throw new Error(`Expected shell block exactly once, got ${count}: ${block.slice(0,60)}`);
  shell=shell.replace(block,'');
}

const heroAnchor='/* PHOTO SOCIAL */';
if(!home.includes(heroAnchor)) throw new Error('hero anchor missing');
if(!home.includes('HOME_MOBILE_HERO_BUTTON_TEXT_V1')) home=home.replace(heroAnchor,blocks[0]+heroAnchor);

const serviceAnchor='/* SERVICE CARDS */';
if(!home.includes(serviceAnchor)) throw new Error('service anchor missing');
if(!home.includes('HOME_SERVICE_TITLE_V1')) home=home.replace(serviceAnchor,serviceAnchor+'\n'+blocks[1]+blocks[2]);

const introAnchor='/* INTRO MODAL */';
if(!home.includes(introAnchor)) throw new Error('intro anchor missing');
if(!home.includes('HOME_INTRO_DIRECT_REVIEW_V1')) home=home.replace(introAnchor,introAnchor+'\n'+blocks[3]);

fs.writeFileSync(shellPath,shell);
fs.writeFileSync(homePath,home);

console.log('CSS migration complete');
