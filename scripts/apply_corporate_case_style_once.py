from pathlib import Path

p = Path('corporate.html')
s = p.read_text(encoding='utf-8')
start = '<!-- CORPORATE_CASE_LINK_HUB_V1 -->'
end = '<section class="contact" id="contact">'
if start not in s:
    raise SystemExit('corporate case hub marker not found')
if end not in s:
    raise SystemExit('contact marker not found')
pre, rest = s.split(start, 1)
old_block, post = rest.split(end, 1)

block = '''<!-- CORPORATE_CASE_LINK_HUB_V2 -->
<section class="section white dg-corporate-casehub" aria-labelledby="corporate-casehub-title">
  <div class="container">
    <h2 class="title" id="corporate-casehub-title">법인등기 이런 경우도 확인하세요</h2>
    <p class="desc">법인등기 진행 시 자주 발생하는 특수한 상황에 대한 처리사례를 확인할 수 있습니다.</p>
    <nav class="dg-corporate-casehub-grid" aria-label="법인등기 처리사례 바로가기">
      <a href="/posts/naver-224411175706.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>1인 법인 설립</strong></div><span>주식 없는 임원을 조사보고인으로 선임한 경우</span></a>
      <a href="/posts/naver-224411086807.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>대표이사 사망 후 변경</strong></div><span>1인 이사인 대표이사 사망 후 배우자를 대표이사로 변경한 경우</span></a>
      <a href="/posts/naver-224411143025.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>감사 중임·의결권 3%</strong></div><span>감사 중임 시 주식 의결권 3% 제한을 확인한 사례</span></a>
      <a href="/posts/naver-224411109357.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>본점 관외이전</strong></div><span>이전 관할 내 동일상호를 확인하고 관외이전등기를 진행한 경우</span></a>
      <a href="/posts/naver-224411074752.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>회사계속·부활등기</strong></div><span>해산간주 회사의 회사계속 및 청산종결간주 후 부활등기</span></a>
    </nav>
  </div>
</section>
<style>
.dg-corporate-casehub{padding-top:48px!important;padding-bottom:48px!important;background:#eef6fb!important}
.dg-corporate-casehub .title{margin:0 0 10px!important;color:#102c48!important;font-size:36px!important;line-height:1.2!important;letter-spacing:-1.8px!important;font-weight:900!important}
.dg-corporate-casehub .desc{margin:0 0 20px!important;color:#587080!important;font-size:15px!important;line-height:1.5!important}
.dg-corporate-casehub-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.dg-corporate-casehub-grid a{display:flex;min-height:118px;flex-direction:column;justify-content:flex-start;padding:18px 16px;border:1px solid #62bcf0;border-radius:15px;background:#fff;transition:.18s;text-decoration:none!important}
.dg-corporate-casehub-grid a:hover{border-color:#36a9e1;transform:translateY(-2px);box-shadow:0 8px 22px rgba(25,41,68,.06)}
.dg-case-head{display:flex;align-items:center;gap:7px;margin-bottom:10px}
.dg-case-badge{display:inline-flex;align-items:center;justify-content:center;min-width:37px;height:23px;padding:0 8px;border-radius:999px;background:#36a9e1;color:#fff!important;font-size:11px!important;line-height:1;font-weight:900;flex:0 0 auto}
.dg-corporate-casehub-grid strong{display:block;color:#102c48;font-size:15px;line-height:1.25;letter-spacing:-.3px;font-weight:900}
.dg-corporate-casehub-grid a>span{display:block;margin-top:0;color:#2d4052;font-size:12px;line-height:1.55}
@media(max-width:1000px){.dg-corporate-casehub-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.dg-corporate-casehub{padding-top:36px!important;padding-bottom:36px!important}.dg-corporate-casehub .title{font-size:29px!important}.dg-corporate-casehub .desc{font-size:13px!important}.dg-corporate-casehub-grid{grid-template-columns:1fr 1fr;gap:8px}.dg-corporate-casehub-grid a{min-height:104px;padding:14px 12px}.dg-corporate-casehub-grid strong{font-size:13px}.dg-corporate-casehub-grid a>span{font-size:10.5px}.dg-case-badge{min-width:34px;height:21px;font-size:10px!important;padding:0 7px}}
</style>
'''

s2 = pre + block + end + post
if s2.count('CORPORATE_CASE_LINK_HUB_V2') != 1:
    raise SystemExit('new case hub marker invalid')
for slug in ['224411175706','224411086807','224411143025','224411109357','224411074752']:
    if s2.count(slug) < 1:
        raise SystemExit('missing case link '+slug)
p.write_text(s2, encoding='utf-8')
