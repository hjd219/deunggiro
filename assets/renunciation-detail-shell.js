(()=>{
const PATH=location.pathname;
const detailPaths=['/renunciation-after.html','/limited-acceptance-liquidation.html'];
if(!detailPaths.includes(PATH))return;
const labels={'/renunciation-after.html':'상속포기 후 절차','/limited-acceptance-liquidation.html':'한정승인 후 청산절차'};


const actions=document.querySelector('.hero .actions');
if(actions&&!actions.querySelector('.dg-detail-home')) actions.insertAdjacentHTML('afterbegin',`<a class="btn dg-detail-home" href="/renunciation.html" aria-label="상속포기·한정승인 메인으로 이동" title="상속포기·한정승인 메인으로 이동"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 11.2 12 4l9 7.2M5.5 9.6V20h13V9.6M9.2 20v-6.5h5.6V20" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg></a>`);

/* 상속 상세페이지(detail-shell.js)와 같은 기본 폼 스타일 */
const style=document.createElement('style');
style.id='dg-renunciation-detail-unified';
style.textContent=`
:root{--dg-detail-line:#9fd3ec;--dg-detail-line-strong:#8fcbea}
body .hero{padding:78px 0 64px!important}
body .hero .breadcrumb{margin:0 0 18px!important;padding:0!important;font-size:13px!important;line-height:1.5!important;color:#5b7185!important}
body .dg-detail-home{width:48px!important;padding:0!important;background:#fff!important;color:#1599d7!important;border:1px solid #84c9ed!important}
body .dg-detail-home svg{width:20px!important;height:20px!important;display:block!important}
body .dg-detail-home:hover,body .dg-detail-home:focus-visible{background:#f5fbfe!important;color:#168dca!important}
body .hero h1{font-size:clamp(34px,4.4vw,49px)!important;line-height:1.16!important;letter-spacing:-2.8px!important;font-weight:900!important}
body .hero-line{width:min(430px,100%)!important;height:3px!important;margin:12px 0 20px!important;background:#6bc5eb!important}
body .hero-desc,body .summary p,body .section p{color:#4f6275!important}
body .summary{border-color:var(--dg-detail-line)!important;border-radius:18px!important}
body .key{border-color:var(--dg-detail-line)!important;border-radius:14px!important}
body .section{border-bottom-color:var(--dg-detail-line)!important}
body .process-box{border:1px solid var(--dg-detail-line-strong)!important;border-radius:20px!important;background:#fff!important;overflow:hidden!important}
body .proc-icon{width:62px!important;height:62px!important;border:1px solid var(--dg-detail-line-strong)!important;border-radius:16px!important;background:#fff!important;font-size:0!important;box-shadow:none!important}
body .proc-icon svg{width:35px!important;height:35px!important}
body .proc b{font-size:14px!important;margin-bottom:8px!important}
body .proc small{display:block!important;color:#465b6e!important;font-size:11px!important;line-height:1.5!important;min-height:34px!important}
body .badge{display:inline-block!important;margin-top:9px!important;padding:5px 9px!important;border-radius:999px!important;background:#edf8fe!important;border:1px solid var(--dg-detail-line)!important;color:#168dca!important;font-size:10px!important;font-weight:900!important}
body .arrow{color:#9daebe!important;padding-top:27px!important}
body .case-card{border-color:var(--dg-detail-line)!important;border-radius:18px!important}
body .side-card{padding:0!important;border:1px solid var(--dg-detail-line-strong)!important;border-radius:14px!important;background:#fff!important;box-shadow:none!important;overflow:hidden!important}
body .side-title{height:38px!important;display:flex!important;align-items:center!important;margin:0!important;padding:0 11px!important;background:#eef8fd!important;color:#0789ca!important;font-size:13px!important;font-weight:900!important;border-bottom:1px solid var(--dg-detail-line-strong)!important}
body .side-link{min-height:52px!important;display:flex!important;align-items:center!important;justify-content:space-between!important;padding:0 11px!important;border-bottom:1px solid var(--dg-detail-line)!important;background:#fff!important;color:#40566a!important;font-size:13px!important;font-weight:800!important}
body .side-link>span{display:none!important}body .side-link::after{content:'›';color:#008fd2;font-size:22px;font-weight:700;line-height:1}
body .side-phone{margin:0!important;padding:12px!important;border:0!important;background:#fff!important}
body .side-call-btn{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;width:100%!important;height:54px!important;padding:0 10px!important;border-radius:10px!important;background:#279ed7!important;color:#fff!important;font-size:13px!important;font-weight:900!important;line-height:1.15!important;white-space:nowrap!important}
body .side-call-btn small{display:block!important;margin-top:4px!important;font-size:10px!important;font-weight:700!important;color:#fff!important}
body .faq{display:block!important;margin-top:12px!important}body .faq-table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;font-size:13px;table-layout:fixed;border:1px solid var(--dg-detail-line);border-radius:14px;overflow:hidden}body .faq-table th,body .faq-table td{padding:9px 11px;text-align:left;vertical-align:middle;line-height:1.4;border-bottom:1px solid var(--dg-detail-line)}body .faq-table tr:last-child th,body .faq-table tr:last-child td{border-bottom:0}body .faq-table th{width:43%;background:#eef8fd;color:#17304a;font-weight:900;white-space:nowrap;border-right:1px solid var(--dg-detail-line)}body .faq-table td{color:#29445d;background:#fff}body .faq-kicker{display:inline-block;font-size:10px;color:#168dca;font-weight:900;margin:0 7px 0 0}
.dg-renunciation-side-spacer{height:156px;background:#fff;border-bottom:1px solid var(--dg-detail-line)}
body .dg-shell-contact{display:none!important}
@media(min-width:769px){.layout{align-items:stretch!important;overflow:visible!important}.layout>.sidebar{display:block!important;position:relative!important;align-self:stretch!important;height:auto!important;min-height:100%!important;overflow:visible!important}.layout>.sidebar>.side-card{position:sticky!important;top:96px!important;width:100%!important;height:max-content!important}}
@media(max-width:900px){body .hero{padding:70px 0 66px!important}body .proc small{min-height:auto!important}}
@media(max-width:800px){body .hero h1{font-size:clamp(18px,4.8vw,22px)!important;letter-spacing:-1.45px!important;white-space:nowrap!important;word-break:keep-all!important;overflow-wrap:normal!important;line-height:1.15!important}@media(max-width:700px){.dg-renunciation-side-spacer{display:none}body .faq-table{display:block!important;width:100%!important;border:0!important;border-radius:0!important;background:transparent!important;font-size:13px!important;overflow:visible!important}body .faq-table tbody{display:block!important;width:100%!important}body .faq-table tr{display:block!important;width:100%!important;margin:0 0 12px!important;border:1px solid var(--dg-detail-line)!important;border-radius:14px!important;background:#fff!important;overflow:hidden!important}body .faq-table th,body .faq-table td{display:block!important;width:100%!important;border:0!important;text-align:left!important}body .faq-table th{padding:13px 14px!important;background:#eef8fd!important;color:#17304a!important;font-size:13px!important;line-height:1.45!important;white-space:normal!important;word-break:keep-all!important;border-bottom:1px solid var(--dg-detail-line)!important}body .faq-table td{padding:13px 14px 15px!important;background:#fff!important;color:#29445d!important;font-size:13px!important;line-height:1.65!important;word-break:keep-all!important}}
`;
document.head.appendChild(style);

const icons=[`<svg viewBox="0 0 48 48"><path d="M13 7h19v28H13zM18 13h9M18 19h9M18 25h6" fill="none" stroke="#2d8df0" stroke-width="3" stroke-linecap="round"/><circle cx="31" cy="31" r="6" fill="none" stroke="#2d8df0" stroke-width="3"/><path d="M28 31l2 2 4-5" fill="none" stroke="#2d8df0" stroke-width="2.5"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M12 8h20v25H12zM17 14h10M17 20h8" fill="none" stroke="#22b8a5" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="29" r="7" fill="none" stroke="#22b8a5" stroke-width="3"/><path d="M37 34l5 5" stroke="#22b8a5" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M24 8v27M13 14h22M15 15l-6 11h12zM33 15l-6 11h12zM18 38h12" fill="none" stroke="#e0a424" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><circle cx="18" cy="18" r="6" fill="#9965df"/><circle cx="30" cy="17" r="5" fill="#b47cec"/><circle cx="25" cy="29" r="7" fill="#8f5ed6"/><path d="M9 38c1-7 6-11 12-11M39 38c-1-7-5-11-11-11" fill="none" stroke="#9b68df" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M8 24l16-12 16 12M12 22v18h24V22M20 40V29h8v11" fill="none" stroke="#45b86b" stroke-width="3"/><path d="M32 11l3 3 6-7" fill="none" stroke="#45b86b" stroke-width="3"/></svg>`];
const processData={
'/renunciation-after.html':[['심판 수리','상속포기 심판문<br>확보','심판 수리'],['소송 대응','채권자 소송 시<br>답변서 제출','답변서 제출'],['후순위 확인','다음 순위 상속인<br>확인','후순위 확인'],['서류 제공','심판문·망인서류<br>등 제공','서류 제공'],['후속절차','후순위 포기 또는<br>한정승인','포기·한정승인']],
'/limited-acceptance-liquidation.html':[['심판 수리','한정승인 심판<br>수리','심판 수리'],['신문공고','채권신고를 위한<br>신문공고','신문공고'],['채권신고','채권신고 내용<br>확인·정리','채권 확인'],['방법 결정','재산상태에 따라<br>청산방법 결정','방법 선택'],['청산 진행','임의청산 또는<br>상속재산파산','청산 진행']]};
document.querySelectorAll('.process-row .proc').forEach((proc,i)=>{const d=processData[PATH]?.[i];if(d)proc.innerHTML=`<div class="proc-icon">${icons[i]}</div><b>${d[0]}</b><small>${d[1]}</small><span class="badge">${d[2]}</span>`});

const sideCard=document.querySelector('.sidebar .side-card');
if(sideCard) sideCard.innerHTML=`<div class="side-title">상속포기·한정승인 세부안내</div>${detailPaths.map(p=>`<a class="side-link ${PATH===p?'active':''}" href="${p}">${labels[p]}<span>›</span></a>`).join('')}<div class="dg-renunciation-side-spacer"></div><div class="side-phone"><a class="side-call-btn" href="tel:0324251500"><span>032-425-1500 상담</span><small>현재두 법무사 사무소</small></a></div>`;

const faqData={
'/renunciation-after.html':[['상속포기 심판이 수리되면 채권자에게 따로 알려야 하나요?','채권자가 소송을 제기한 경우에는 상속포기 심판문 등을 첨부하여 답변서를 제출하는 방식으로 대응합니다.'],['상속포기 후 후순위 상속인은 어떻게 확인하나요?','가족관계에 따라 다음 순위 상속인이 있는지 확인하고, 필요한 경우 상속포기 심판문과 망인 관련 서류를 전달합니다.'],['후순위 상속인도 상속포기나 한정승인을 해야 하나요?','선순위 상속포기로 후순위가 상속인이 된 경우에는 후순위 상속인이 자신의 상황에 따라 상속포기 또는 한정승인 절차를 검토합니다.']],
'/limited-acceptance-liquidation.html':[['한정승인 결정만 받으면 절차가 끝나나요?','한정승인 심판 수리 후에는 신문공고와 채권신고 확인, 상속재산 청산 등 후속절차가 남습니다.'],['임의청산은 어떻게 진행하나요?','채권신고 내용을 확인한 뒤 배당표를 작성하고 상속재산 범위에서 채권자에게 배당하는 방식으로 진행합니다.'],['상속재산파산은 언제 검토하나요?','부동산 등 상속재산을 직접 환가하거나 여러 채권자에게 배당하기 곤란한 경우 상속재산파산 절차를 검토할 수 있습니다.']]};
const faq=document.querySelector('.faq');
if(faq) faq.innerHTML='<table class="faq-table"><tbody>'+faqData[PATH].map(([q,a])=>`<tr><th><span class="faq-kicker">Q</span>${q}</th><td>${a}</td></tr>`).join('')+'</tbody></table>';

if(!document.getElementById('dg-ai-panel')&&!document.querySelector('script[data-dg-ai-widget]')){const ai=document.createElement('script');ai.src='/assets/ai-deunggiro-widget.js?v=20260915-4';ai.defer=true;ai.dataset.dgAiWidget='1';document.head.appendChild(ai)}
})();