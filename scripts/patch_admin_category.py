from pathlib import Path

p=Path('admin.html')
s=p.read_text(encoding='utf-8')

marker='/* ===== v13 블로그형 편집기 핵심: 선택영역 기억 + 즉시 적용 + 메뉴 자동 닫기 ===== */'
addon=r'''
/* ===== 카테고리 자동분류: 제목 기준, 직접 선택 시 유지 ===== */
let dgCategoryAutoWriting=false;
function dgInferCategory(title){
  const t=String(title||'').replace(/\s+/g,' ').trim();
  const has=words=>words.some(w=>t.includes(w));
  if(has(['법인등기','법인설립','법인주소','법인 본점','법인 상호','법인 목적','법인 대표','1인 법인','1인법인','주식회사','유한회사','유한책임회사','농업회사법인','영농조합법인','대표이사','주주총회','이사회','본점이전','본점주소','자본금','가수금','증자','감자','회사계속','해산간주','청산종결간주','합명회사','합자회사','법인인감','법인도장','정관']))return '법인등기';
  if(has(['상속재산분할심판','상속재산분할청구','상속재산분할협의서','상속재산분할협의','상속분쟁','기여분','특별수익','유류분','상속회복청구']))return '상속재산분할';
  if(has(['재산분할등기','부동산 이전','부동산이전','공동명의·단독명의 이전','공동명의 단독명의 이전','촉탁등기','소유권이전등기','매매예약가등기','가등기','근저당','전세권','등기권리증','등기필증','신탁등기','부동산 등기부','부동산등기비용','취득세율']))return '부동산등기';
  const death=has(['사망','망인','피상속인']);
  if(death&&has(['예금 인출','예금인출','통장 인출','통장예금 인출','사망보험금','해지환급금','장례비','병원비'])&&has(['주의','위험','단순승인','영향','괜찮을까','가능할까']))return '상속포기·한정승인';
  if(t.includes('상속절차')&&(t.includes('상속등기')||t.includes('해야 할 일')||t.includes('사망신고'))&&has(['예금','은행','보험','자동차','주식','안심상속']))return '상속등기';
  if(death&&t.includes('특별대리인'))return '상속등기';
  if(has(['상속등기','상속절차','상속순위','상속권','대습상속','상속취득세','상속지분','누가 상속인','상속인은 누구','상속받','상속예금'])){
    if(t.includes('상속포기는 어디까지'))return '상속포기·한정승인';
    return '상속등기';
  }
  if(has(['상속포기','한정승인','특별한정승인','상속채무','상속빚','상속 빚','상속재산파산','단순승인'])||(death&&t.includes('3개월')))return '상속포기·한정승인';
  if(has(['협의이혼','재판이혼','재판상이혼','이혼소송','이혼신고','숙려기간','친권','양육권','양육비','면접교섭','상간남','상간녀','위자료','개명','성본변경','성·본변경','성본창설','성년후견','한정후견','미성년후견']))return '가사';
  if(has(['부동산','임차권등기','임차인','임대인','임대차','전세보증금','보증금','계약갱신거절','신탁','공매','경매','매매','증여','취득세']))return '부동산등기';
  if(has(['가압류 해방공탁','제3채무자 공탁','채권압류','공시최고','제권판결','개인회생','파산지원센터']))return '기타';
  if(has(['상속인','상속재산','유언','부모님 사망','부모 사망','배우자 사망','남편 사망','아내 사망','형제 사망','자녀 사망']))return '상속등기';
  return '';
}
function dgAutoCategory(force=false){
  if(typeof editingOriginalSlug!=='undefined' && editingOriginalSlug)return;
  const el=$('category'),title=$('title')?.value||'';
  if(!el||el.dataset.dgManualCategory==='1')return;
  if(!force && el.value && el.value!=='기타' && el.dataset.dgAutoCategory!=='1')return;
  const next=dgInferCategory(title);if(!next)return;
  const option=[...el.options].find(o=>o.value===next||o.textContent===next);if(!option)return;
  dgCategoryAutoWriting=true;el.value=option.value;el.dataset.dgAutoCategory='1';el.dispatchEvent(new Event('change'));dgCategoryAutoWriting=false;
}
$('category')?.addEventListener('change',e=>{if(!dgCategoryAutoWriting&&e.isTrusted){e.currentTarget.dataset.dgManualCategory='1';e.currentTarget.dataset.dgAutoCategory='0'}});
$('title')?.addEventListener('input',()=>{dgAutoCategory();setTimeout(()=>{if(typeof autoGenerateSeoFields==='function')autoGenerateSeoFields()},0)});
$('publishBtn')?.addEventListener('click',()=>dgAutoCategory(true),true);
$('writeTab')?.addEventListener('click',()=>setTimeout(()=>{const el=$('category');if(el){delete el.dataset.dgManualCategory;delete el.dataset.dgAutoCategory}dgAutoCategory()},0));
setTimeout(()=>dgAutoCategory(),0);

'''

if '카테고리 자동분류: 제목 기준' not in s:
    if marker not in s:
        raise SystemExit('admin category insertion marker not found')
    s=s.replace(marker,addon+marker,1)

# 화면에서도 자동분류임을 알 수 있게 표시
s=s.replace('<div class="form-group"><label>카테고리</label><select id="category">','<div class="form-group"><label>카테고리 <span style="color:#2457a6;font-size:12px">자동분류</span></label><select id="category">',1)

p.write_text(s,encoding='utf-8')
print('admin category auto-classification patched')
