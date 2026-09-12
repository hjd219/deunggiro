import fs from 'node:fs';
const core='assets/site-shell-core.css', home='assets/home.css';
let c=fs.readFileSync(core,'utf8'), h=fs.readFileSync(home,'utf8');
const blocks=[
'body.home .hero-written-ghost{opacity:0!important}body.home .hero .copy{min-width:0!important}body.home .hero .buttons .btn{white-space:nowrap!important}',
'@media(max-width:800px){body.home .hero .copy{padding-top:30px!important;padding-bottom:12px!important}body.home .hero h1{margin-bottom:12px!important}body.home .hero .hero-written-phrase{font-size:44px!important;min-height:88px!important;margin-top:24px!important}body.home .hero .copy p{max-width:34em!important;margin-bottom:15px!important}body.home .quick{padding-left:16px!important;padding-right:16px!important}body.home .section .container{padding-left:16px!important;padding-right:16px!important}}',
'@media(max-width:480px){body.home .hero .hero-written-phrase{font-size:40px!important;min-height:80px!important;margin-top:20px!important}body.home .hero .buttons{grid-template-columns:1fr 1fr!important}body.home .hero .buttons .btn-dark{grid-column:1/-1!important}body.home .quick{padding-left:16px!important;padding-right:16px!important}}'
];
for(const b of blocks){if((c.split(b).length-1)!==1)throw new Error('core target mismatch');if(h.includes(b))throw new Error('already in home');c=c.replace(b,'');}
h+='\n\n/* HOME_CORE_OWNERSHIP_MOVE_V1 - 공통 shell에서 메인 전용 규칙 이전 */\n'+blocks.join('\n')+'\n';
fs.writeFileSync(core,c);fs.writeFileSync(home,h);
console.log('moved 3 home-only rule blocks from core to home.css');