/* SERVICE_LEAD_V1 - 5개 업무페이지 상단 설명문 전용 */
(function(){
  const copyByPath={
    '/inheritance.html':'상속등기 절차 · 비용 · 필요서류부터 협의분할, 연락두절 · 해외거주 · 미성년자 등 복잡한 상속까지 실제 처리사례를 바탕으로 안내합니다.',
    '/renunciation.html':'상속포기 · 한정승인 절차 · 비용 · 필요서류부터 특별한정승인, 후순위 상속인, 미성년자, 상속재산파산까지 실제 처리사례를 바탕으로 안내합니다.',
    '/corporate.html':'법인등기 절차 · 비용 · 필요서류부터 법인설립, 임원변경, 본점이전, 상호 · 목적변경, 자본금증자, 해산 · 청산까지 안내합니다.',
    '/realestate.html':'부동산등기 절차 · 비용 · 필요서류부터 매매, 증여, 상속, 재산분할, 근저당 설정 · 말소, 신탁등기까지 안내합니다.',
    '/family.html':'가사사건 절차 · 비용 · 필요서류부터 협의이혼, 재산분할, 미성년자 특별대리인, 성년후견, 개명 · 가족관계등록까지 안내합니다.'
  };
  const copy=copyByPath[location.pathname];
  if(!copy) return;
  const target=document.querySelector('.subhero .subhero-copy > p, .subhero p');
  if(target) target.textContent=copy;
})();
