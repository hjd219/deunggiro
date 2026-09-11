/* CORPORATE_EXTRA_V1 - 법인등기 페이지 전용 기능. 공통 shell과 분리 */
(function(){
  if(location.pathname!=='/corporate.html') return;

  const cards=document.querySelector('.corp-cards');
  if(cards&&!document.getElementById('service-4')){
    cards.insertAdjacentHTML('beforeend',`<article class="corp-card" id="service-4"><div class="corp-card-top"><div class="corp-icon"><svg viewBox="0 0 64 64"><path d="M21 29v-6c0-8 5-13 12-13 5 0 9 3 11 7" fill="none" stroke="#d85b7d" stroke-width="3.8" stroke-linecap="round"/><rect x="16" y="28" width="34" height="25" rx="6" fill="none" stroke="#d85b7d" stroke-width="3.8"/><path d="M33 36v8" fill="none" stroke="#d85b7d" stroke-width="3.8" stroke-linecap="round"/><circle cx="33" cy="36" r="2.5" fill="#d85b7d"/><path d="M23 48h20" fill="none" stroke="#d85b7d" stroke-width="3" stroke-linecap="round"/></svg></div><div><h3>회사계속등기</h3></div></div><div class="corp-tags"><span>해산간주</span><span>회사계속</span><span>임원선임</span></div><div class="corp-row"><b>임원</b><span>인감도장 · 인감증명서 2통 · 주민등록초본 1통</span></div><div class="corp-row"><b>임원 아닌 주주</b><span>인감도장 · 인감증명서 1통</span></div><div class="corp-row"><b>법인</b><span>법인 인감도장 · 정관 2통 · 주주명부 1통 · 법인 인감카드</span></div><div class="corp-note"><strong>회사계속등기 확인사항</strong><br>현재 법인등기부상 해산간주 상태인지 먼저 확인하고, 회사계속 결의와 임원선임을 함께 진행합니다.</div><a class="corp-cost" href="tel:0324251500">회사계속등기 상담하기 <span>→</span></a></article>`);
    const style=document.createElement('style');
    style.textContent='@media(min-width:901px){.corp-cards{grid-template-columns:repeat(4,minmax(0,1fr))!important}.corp-card{padding:20px 17px!important}.corp-row{grid-template-columns:82px minmax(0,1fr)!important;gap:8px!important}.corp-card h3{font-size:24px!important}}';
    document.head.appendChild(style);
    const intro=document.querySelector('.corp-head p');
    if(intro) intro.textContent='법인설립·변경등기·자본금증자·회사계속등기에 필요한 핵심서류를 업무별로 확인하세요.';
  }

  const faqLayout=document.querySelector('.corp-faq-layout'),authCard=document.querySelector('.corp-auth-card'),faq=document.querySelector('.corp-faq');
  if(faqLayout&&authCard&&faq&&!document.querySelector('.corp-penalty-card')){
    const faqInner=faqLayout.parentElement,outerKicker=faqInner?.querySelector('.corp-faq-kicker'),outerTitle=faqInner?.querySelector(':scope > h2');
    if(outerTitle) faq.insertBefore(outerTitle,faq.firstChild);
    if(outerKicker) faq.insertBefore(outerKicker,faq.firstChild);
    const authIcon=authCard.querySelector('.corp-auth-icon'),authTitle=authCard.querySelector('h3');
    if(authIcon&&authTitle&&!authCard.querySelector('.corp-auth-head')){
      const head=document.createElement('div');head.className='corp-auth-head';authCard.insertBefore(head,authCard.firstChild);head.appendChild(authIcon);head.appendChild(authTitle);
    }
    const penalty=document.createElement('section');
    penalty.className='corp-penalty-card';
    penalty.innerHTML=`<div class="corp-penalty-kicker">PENALTY GUIDE</div><h3>과태료 예상기준표</h3><p class="corp-penalty-desc">임원변경등기 지연 시 참고할 수 있는 실무상 예상기준입니다.</p><table class="corp-penalty-table"><thead><tr><th>등기 지연기간</th><th>예상기준</th></tr></thead><tbody><tr><td>1일 ~ 1개월</td><td>약 10만원 이내</td></tr><tr><td>1개월 ~ 2개월</td><td>약 20만원 이내</td></tr><tr><td>2개월 ~ 6개월</td><td>약 30만원 이내</td></tr><tr><td>6개월 ~ 1년</td><td>약 50만원 이내</td></tr><tr><td>1년 이상</td><td>사건별 상이</td></tr></tbody></table><div class="corp-penalty-note">※ 법원의 공식 과태료 산정표가 아닌 실무상 예상기준입니다. 실제 과태료는 지연기간, 등기사항, 위반 내용 및 법원의 판단에 따라 달라질 수 있습니다.</div>`;
    faqLayout.appendChild(authCard);faqLayout.appendChild(penalty);faqLayout.appendChild(faq);
    const items=[...faq.querySelectorAll('.corp-faq-item')].slice(0,4),qa=[['임원 임기가 만료되면 과태료가 나오나요?','임기만료 후 임원을 선임한 경우 <strong>주주총회 선임일 또는 취임승낙일부터 2주 이내</strong> 변경등기를 해야 하며, 기간을 넘기면 과태료가 부과될 수 있습니다.'],['해산간주된 법인을 다시 운영할 수 있나요?','<strong>해산간주 상태라면 회사계속등기가 가능합니다.</strong> 다만 청산종결간주된 법인은 회사계속이 불가능하며 청산사무 수행을 위한 부활등기만 가능합니다.'],['1인 법인·1인 주주도 주주총회를 꼭 해야 하나요?','<strong>1인 주주 법인은 주주전원 서면결의로 주주총회를 갈음할 수 있습니다.</strong>'],['대표이사의 주소가 변경되면 변경등기를 해야 하나요?','네. 대표이사의 주소가 변경된 경우 <strong>주소변경일로부터 2주 이내에 대표이사 주소변경등기</strong>를 해야 합니다.']];
    items.forEach((item,i)=>{const q=item.querySelector('.corp-faq-q'),a=item.querySelector('.corp-faq-a');if(q){const mark=q.querySelector('.corp-qmark'),plus=q.querySelector('.corp-plus');q.innerHTML='';if(mark)q.appendChild(mark);const span=document.createElement('span');span.textContent=qa[i][0];q.appendChild(span);if(plus)q.appendChild(plus)}if(a)a.innerHTML=qa[i][1]});
    const faqStyle=document.createElement('style');
    faqStyle.textContent=`
      .corp-faq-inner{max-width:1180px!important}
      .corp-faq-layout{display:grid!important;grid-template-columns:.82fr 1fr 1.35fr!important;gap:18px!important;align-items:stretch!important}
      .corp-faq-layout>.corp-auth-card{grid-column:1!important;grid-row:1!important}
      .corp-faq-layout>.corp-penalty-card{grid-column:2!important;grid-row:1!important}
      .corp-faq-layout>.corp-faq{grid-column:3!important;grid-row:1!important}
      .corp-faq-layout>.corp-auth-card,.corp-faq-layout>.corp-penalty-card,.corp-faq-layout>.corp-faq{background:#fff!important;border:1px solid #d7e1e8!important;border-radius:22px!important;padding:25px 22px!important;min-width:0!important;box-shadow:0 6px 20px rgba(31,41,55,.035)!important}
      .corp-auth-head{display:flex!important;align-items:center!important;gap:13px!important;margin:0 0 15px!important}.corp-auth-head .corp-auth-icon{margin:0!important;flex:0 0 60px!important}.corp-auth-head h3{margin:0!important;font-size:24px!important;line-height:1.25!important;letter-spacing:-1px!important}
      .corp-faq{display:block!important}
      .corp-faq .corp-faq-kicker{display:block!important;color:#168dca!important;font-size:11px!important;font-weight:900!important;letter-spacing:.13em!important;margin:0 0 7px!important}
      .corp-faq>h2{font-size:27px!important;line-height:1.22!important;letter-spacing:-1.4px!important;margin:0 0 18px!important;color:#111827!important}
      .corp-faq-layout .corp-faq-item{background:#fff!important;border:1px solid #c9dbe8!important;border-radius:13px!important;margin:9px 0!important;overflow:hidden!important;box-shadow:none!important}
      .corp-faq-layout .corp-faq-q{display:grid!important;grid-template-columns:28px minmax(0,1fr) 24px!important;align-items:center!important;gap:9px!important;padding:13px 12px!important;min-height:57px!important;font-size:12.5px!important;font-weight:900!important;line-height:1.45!important;color:#111827!important;background:#fff!important;border:0!important}
      .corp-faq-layout .corp-qmark{display:flex!important;align-items:center!important;justify-content:center!important;width:27px!important;height:27px!important;border-radius:50%!important;background:#eaf7fd!important;color:#168dca!important;font-size:12px!important;font-weight:900!important}
      .corp-faq-layout .corp-plus{color:#8ca0b2!important;font-size:21px!important;font-weight:300!important;text-align:center!important}
      .corp-faq-layout .corp-faq-a{padding:0 13px 14px 49px!important;font-size:11.5px!important;line-height:1.7!important;color:#596572!important;background:#fff!important}
      .corp-faq-layout .corp-faq-a strong{color:#168dca!important}
      .corp-penalty-kicker{font-size:11px;font-weight:900;letter-spacing:.13em;color:#168dca;margin-bottom:7px}.corp-penalty-card h3{font-size:27px;line-height:1.22;letter-spacing:-1.4px;margin:0 0 16px;color:#20242b}.corp-penalty-desc{font-size:12.5px;color:#6b7680;line-height:1.6;margin:0 0 15px}.corp-penalty-table{width:100%;border-collapse:separate;border-spacing:0;font-size:11.5px;border:1px solid #dfe7ee;border-radius:11px;overflow:hidden}.corp-penalty-table th,.corp-penalty-table td{padding:8px 7px;text-align:center;border-bottom:1px solid #e5ebef}.corp-penalty-table tr:last-child td{border-bottom:0}.corp-penalty-table th{background:#f3f9fc;color:#365a70;font-weight:900}.corp-penalty-table td:first-child{font-weight:800;color:#4b5965}.corp-penalty-table td:last-child{font-weight:900;color:#168dca}.corp-penalty-note{margin-top:11px;padding:9px 10px;background:#f6fbfe;border:1px solid #dceef7;border-radius:10px;color:#687680;font-size:9.8px;line-height:1.55}
      @media(max-width:950px){.corp-faq-layout{grid-template-columns:1fr 1fr!important}.corp-faq-layout>.corp-auth-card{grid-column:1!important;grid-row:1!important}.corp-faq-layout>.corp-penalty-card{grid-column:2!important;grid-row:1!important}.corp-faq-layout>.corp-faq{grid-column:1/-1!important;grid-row:2!important}}
      @media(max-width:650px){.corp-faq-layout{grid-template-columns:1fr!important}.corp-faq-layout>.corp-auth-card{grid-column:1!important;grid-row:1!important}.corp-faq-layout>.corp-penalty-card{grid-column:1!important;grid-row:2!important}.corp-faq-layout>.corp-faq{grid-column:1!important;grid-row:3!important}.corp-faq-layout>.corp-auth-card,.corp-faq-layout>.corp-penalty-card,.corp-faq-layout>.corp-faq{padding:22px 18px!important}.corp-auth-head .corp-auth-icon{flex-basis:52px!important;width:52px!important;height:52px!important}.corp-auth-head h3{font-size:21px!important}}
    `;
    document.head.appendChild(faqStyle);
  }
})();
