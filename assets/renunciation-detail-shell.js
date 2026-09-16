(()=>{
const PATH=location.pathname;
const detailPaths=['/renunciation-after.html','/limited-acceptance-liquidation.html'];
if(!detailPaths.includes(PATH))return;
const labels={'/renunciation-after.html':'상속포기 후 절차','/limited-acceptance-liquidation.html':'한정승인 후 청산절차'};

/* 제목 아이콘: 상속포기·한정승인 대표페이지와 같은 기존 아이콘만 사용 */
const mainIcon=document.querySelector('.main-icon');
if(mainIcon) mainIcon.innerHTML='<img src="/assets/icons/service-renunciation.svg" alt="">';

/* 상속 상세페이지 기본 폼에서 필요한 내용만 채움 */
const icons=[`<svg viewBox="0 0 48 48"><path d="M13 7h19v28H13zM18 13h9M18 19h9M18 25h6" fill="none" stroke="#2d8df0" stroke-width="3" stroke-linecap="round"/><circle cx="31" cy="31" r="6" fill="none" stroke="#2d8df0" stroke-width="3"/><path d="M28 31l2 2 4-5" fill="none" stroke="#2d8df0" stroke-width="2.5"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M12 8h20v25H12zM17 14h10M17 20h8" fill="none" stroke="#22b8a5" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="29" r="7" fill="none" stroke="#22b8a5" stroke-width="3"/><path d="M37 34l5 5" stroke="#22b8a5" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M24 8v27M13 14h22M15 15l-6 11h12zM33 15l-6 11h12zM18 38h12" fill="none" stroke="#e0a424" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><circle cx="18" cy="18" r="6" fill="#9965df"/><circle cx="30" cy="17" r="5" fill="#b47cec"/><circle cx="25" cy="29" r="7" fill="#8f5ed6"/><path d="M9 38c1-7 6-11 12-11M39 38c-1-7-5-11-11-11" fill="none" stroke="#9b68df" stroke-width="3"/></svg>`,`<svg viewBox="0 0 48 48"><path d="M8 24l16-12 16 12M12 22v18h24V22M20 40V29h8v11" fill="none" stroke="#45b86b" stroke-width="3"/><path d="M32 11l3 3 6-7" fill="none" stroke="#45b86b" stroke-width="3"/></svg>`];
const processData={
'/renunciation-after.html':[['심판 수리','상속포기 심판문<br>확보','심판 수리'],['소송 대응','채권자 소송 시<br>답변서 제출','답변서 제출'],['후순위 확인','다음 순위 상속인<br>확인','후순위 확인'],['서류 제공','심판문·망인서류<br>등 제공','서류 제공'],['후속절차','후순위 포기 또는<br>한정승인','포기·한정승인']],
'/limited-acceptance-liquidation.html':[['심판 수리','한정승인 심판<br>수리','심판 수리'],['신문공고','채권신고를 위한<br>신문공고','신문공고'],['채권신고','채권신고 내용<br>확인·정리','채권 확인'],['방법 결정','재산상태에 따라<br>청산방법 결정','방법 선택'],['청산 진행','임의청산 또는<br>상속재산파산','청산 진행']]};
document.querySelectorAll('.process-row .proc').forEach((proc,i)=>{const d=processData[PATH]?.[i];if(d)proc.innerHTML=`<div class="proc-icon">${icons[i]}</div><b>${d[0]}</b><small>${d[1]}</small><span class="badge">${d[2]}</span>`});

/* 우측 세부안내: 기존 상속 상세페이지 클래스/동작을 그대로 사용, 2개 아래만 빈 공간 */
const sideCard=document.querySelector('.sidebar .side-card');
if(sideCard) sideCard.innerHTML=`<div class="side-title">상속포기·한정승인 세부안내</div>${detailPaths.map(p=>`<a class="side-link ${PATH===p?'active':''}" href="${p}">${labels[p]}<span>›</span></a>`).join('')}<div class="dg-renunciation-side-spacer"></div><div class="side-phone"><a class="side-call-btn" href="tel:0324251500"><span>032-425-1500 상담</span><small>현재두 법무사 사무소</small></a></div>`;

const faqData={
'/renunciation-after.html':[['상속포기 심판이 수리되면 채권자에게 따로 알려야 하나요?','채권자가 소송을 제기한 경우에는 상속포기 심판문 등을 첨부하여 답변서를 제출하는 방식으로 대응합니다.'],['상속포기 후 후순위 상속인은 어떻게 확인하나요?','가족관계에 따라 다음 순위 상속인이 있는지 확인하고, 필요한 경우 상속포기 심판문과 망인 관련 서류를 전달합니다.'],['후순위 상속인도 상속포기나 한정승인을 해야 하나요?','선순위 상속포기로 후순위가 상속인이 된 경우에는 후순위 상속인이 자신의 상황에 따라 상속포기 또는 한정승인 절차를 검토합니다.']],
'/limited-acceptance-liquidation.html':[['한정승인 결정만 받으면 절차가 끝나나요?','한정승인 심판 수리 후에는 신문공고와 채권신고 확인, 상속재산 청산 등 후속절차가 남습니다.'],['임의청산은 어떻게 진행하나요?','채권신고 내용을 확인한 뒤 배당표를 작성하고 상속재산 범위에서 채권자에게 배당하는 방식으로 진행합니다.'],['상속재산파산은 언제 검토하나요?','부동산 등 상속재산을 직접 환가하거나 여러 채권자에게 배당하기 곤란한 경우 상속재산파산 절차를 검토할 수 있습니다.']]};
const faq=document.querySelector('.faq');
if(faq) faq.innerHTML='<table class="faq-table"><tbody>'+faqData[PATH].map(([q,a])=>`<tr><th><span class="faq-kicker">Q</span>${q}</th><td>${a}</td></tr>`).join('')+'</tbody></table>';

/* 상단 세부안내: 기존 사이트의 native select와 같은 실제 select */
const actions=document.querySelector('.hero .actions,.subhero .actions,.hero .buttons,.subhero .buttons');
if(actions){
  const old=[...actions.querySelectorAll('a,button,select')].find(el=>el.textContent.includes('상속포기·한정승인 세부안내'));
  if(old) old.remove();
  const wrap=document.createElement('label'); wrap.className='dg-native-detail-select-wrap';
  const select=document.createElement('select'); select.className='dg-native-detail-select'; select.setAttribute('aria-label','상속포기·한정승인 세부안내');
  select.innerHTML=`<option value="" selected>상속포기·한정승인 세부안내</option><option value="/renunciation-after.html">상속포기 후 절차</option><option value="/limited-acceptance-liquidation.html">한정승인 후 청산절차</option>`;
  select.addEventListener('change',()=>{if(select.value)location.href=select.value;else select.selectedIndex=0});
  wrap.appendChild(select); actions.appendChild(wrap);
}

/* 기존 native select와 동일한 스타일 + 기본 폼의 sticky/빈칸만 보완 */
const style=document.createElement('style');
style.id='dg-renunciation-detail-minimal';
style.textContent=`
.dg-native-detail-select-wrap{position:relative;display:inline-flex;min-width:210px;min-height:48px}
.dg-native-detail-select{width:100%;min-height:48px;padding:0 38px 0 16px;border:1px solid #84c9ed;border-radius:8px;background:#fff;color:#20242b;font:inherit;font-size:15px;font-weight:900;box-shadow:0 8px 18px rgba(54,169,225,.20);appearance:auto;-webkit-appearance:menulist;cursor:pointer}
.dg-renunciation-side-spacer{height:156px;background:#fff;border-bottom:1px solid #9fd3ec}
@media(min-width:769px){.layout{align-items:stretch!important;overflow:visible!important}.layout>.sidebar{display:block!important;position:relative!important;align-self:stretch!important;height:auto!important;min-height:100%!important;overflow:visible!important}.layout>.sidebar>.side-card{position:sticky!important;top:96px!important;width:100%!important;height:max-content!important}}
@media(max-width:700px){.dg-native-detail-select-wrap{flex:1 1 210px;min-width:0}.dg-native-detail-select{font-size:15px}.dg-renunciation-side-spacer{display:none}}
`;
document.head.appendChild(style);

if(!document.getElementById('dg-ai-panel')&&!document.querySelector('script[data-dg-ai-widget]')){const ai=document.createElement('script');ai.src='/assets/ai-deunggiro-widget.js?v=20260915-4';ai.defer=true;ai.dataset.dgAiWidget='1';document.head.appendChild(ai)}
})();