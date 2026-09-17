from pathlib import Path
import re
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
s=re.sub(r'\s*<!-- INHERITANCE_INTERNAL_LINK_HUB_V1 -->\s*<section class="section white dg-inheritance-linkhub"[\s\S]*?</section>\s*<style>[\s\S]*?\.dg-inheritance-linkhub[\s\S]*?</style>\s*','\n',s,count=1)
if 'INHERITANCE_CASE_CARDS_RESTORED_V1' not in s:
    block='''\n<!-- INHERITANCE_CASE_CARDS_RESTORED_V1 -->
<section class="section white dg-inheritance-casecards"><div class="container"><div class="label">실제 처리사례</div><h2 class="title">상속등기 이런 경우도 처리합니다</h2><p class="desc">상속인 상황에 따라 달라지는 실제 처리 유형을 확인하세요.</p><nav class="dg-inheritance-casecards-grid"><a href="/inheritance-missing-heir.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>연락두절</strong></div><span>연락이 되지 않는 상속인이 있는 경우</span></a><a href="/inheritance-overseas-heir.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>해외·외국국적</strong></div><span>해외거주·외국인 상속인이 있는 경우</span></a><a href="/inheritance-minor-heir.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>미성년자</strong></div><span>미성년 상속인이 있는 경우</span></a><a href="/inheritance-substitute-succession.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>대습상속</strong></div><span>대습상속이 문제되는 경우</span></a><a href="/inheritance-division.html"><div class="dg-case-head"><span class="dg-case-badge">사례</span><strong>상속재산분할</strong></div><span>협의가 되지 않거나 분할이 필요한 경우</span></a></nav></div></section>
<style>.dg-inheritance-casecards{padding:48px 0!important;background:#eef6fb!important}.dg-inheritance-casecards .desc{margin-bottom:18px!important}.dg-inheritance-casecards-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}.dg-inheritance-casecards-grid a{min-height:118px;padding:18px 16px;display:flex;flex-direction:column;background:#fff;border:1.5px solid #69b8ee;border-radius:14px}.dg-inheritance-casecards .dg-case-head{display:flex;align-items:center;gap:7px;white-space:nowrap}.dg-inheritance-casecards .dg-case-badge{display:inline-flex;align-items:center;height:21px;padding:0 8px;border-radius:999px;background:#2fa6ef;color:#fff;font-size:11px;font-weight:800}.dg-inheritance-casecards-grid strong{color:#24384f;font-size:15px}.dg-inheritance-casecards-grid a>span{margin-top:12px;color:#3f4f63;font-size:12px;font-weight:700}@media(max-width:1000px){.dg-inheritance-casecards-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:700px){.dg-inheritance-casecards-grid{grid-template-columns:1fr 1fr;gap:8px}.dg-inheritance-casecards-grid a{min-height:108px;padding:14px 12px}.dg-inheritance-casecards-grid strong{font-size:13px}.dg-inheritance-casecards-grid a>span{font-size:10.5px}}</style>
'''
    marker='<section class="contact" id="contact">'
    if marker not in s: raise SystemExit('contact marker missing')
    s=s.replace(marker,block+marker,1)
p.write_text(s,encoding='utf-8')
assert 'INHERITANCE_INTERNAL_LINK_HUB_V1' not in s
assert s.count('INHERITANCE_CASE_CARDS_RESTORED_V1')==1
# trigger
