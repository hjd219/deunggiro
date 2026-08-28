from pathlib import Path

p=Path('admin.html')
s=p.read_text(encoding='utf-8')

marker='/* ===== v13 블로그형 편집기 핵심: 선택영역 기억 + 즉시 적용 + 메뉴 자동 닫기 ===== */'
addon=r'''
/* ===== 카테고리 자동분류: 제목 기준, 직접 선택 시 유지 ===== */
let dgCategoryAutoWriting=false;
function dgInferCategory(title){
  const t=String(title||'').replace(/\s+/g,' ');
  const rules=[
    ['상속포기·한정승인',['상속포기','한정승인','특별한정승인','상속채무','사망신고 전 예금','망인 예금','보험금','해지환급금']],
    ['상속재산분할',['상속재산분할심판','상속재산분할청구','상속분쟁','기여분','특별수익','협조거부','연락두절']],
    ['법인등기',['법인','주식회사','유한회사','대표이사','이사','감사','주주','본점이전','자본금','증자','감자','상호변경','목적변경','해산','청산']],
    ['가사',['협의이혼','재판이혼','이혼','개명','성년후견','한정후견','친권','양육비','가사사건']],
    ['부동산등기',['근저당','가압류','등기권리증','등기필증','매매','증여','전세권','소유권이전','부동산','재산분할등기','신탁등기']],
    ['상속등기',['상속등기','대습상속','상속취득세','상속인','상속지분','상속재산','유언','사망 후 상속','부모님 사망']]
  ];
  for(const [category,words] of rules){if(words.some(w=>t.includes(w)))return category}
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
