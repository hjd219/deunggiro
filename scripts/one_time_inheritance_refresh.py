from pathlib import Path
import re

p = Path('inheritance.html')
s = p.read_text(encoding='utf-8')

# Remove current main-services block only.
s, n1 = re.subn(r'<section class="section white"><div class="container"><div class="label">MAIN SERVICES</div><h2 class="title">주요 업무</h2>.*?</section>\n', '', s, count=1, flags=re.S)
if n1 != 1:
    raise SystemExit(f'MAIN SERVICES replacement count={n1}')

new_mid = '''<section class="section inheritance-overview"><div class="container">
<div class="label">INHERITANCE PROCESS</div><h2 class="title">상속절차 한눈에 보기</h2><p class="desc">사망 후 확인해야 할 주요 절차와 기한을 순서대로 확인하세요.</p>
<div class="inheritance-flow">
  <div class="flow-step flow-blue"><div class="flow-icon">申</div><h3>사망신고</h3><p>사망 사실 신고</p><span class="deadline">1개월</span></div><div class="flow-arrow">→</div>
  <div class="flow-step flow-teal"><div class="flow-icon">⌕</div><h3>재산·채무조회</h3><p>안심상속 등으로 확인</p><span class="deadline muted-deadline">재산조회</span></div><div class="flow-arrow">→</div>
  <div class="flow-step flow-gold"><div class="flow-icon">⚖</div><h3>상속방법 결정</h3><p>포기·한정승인 판단</p><span class="deadline">3개월</span></div><div class="flow-arrow">→</div>
  <div class="flow-step flow-purple"><div class="flow-icon">協</div><h3>상속인 협의</h3><p>분할방법 협의</p></div><div class="flow-arrow">→</div>
  <div class="flow-step flow-green"><div class="flow-icon">登</div><h3>취득세·상속등기</h3><p>세금 신고·명의변경</p><span class="deadline">취득세 6개월</span></div>
</div>
<div class="inheritance-note">※ 상속등기 자체에는 신청기한이 없지만, 취득세는 원칙적으로 상속개시일이 속하는 달의 말일부터 6개월 이내 신고·납부해야 합니다.</div>
<div class="faq-block"><div class="label">FAQ</div><h2 class="title faq-title">자주 묻는 질문</h2>
  <details class="faq-acc"><summary><span>Q</span>상속등기는 언제까지 해야 하나요?</summary><p><b>A.</b> 상속등기 자체에는 신청기한이 없습니다. 다만 취득세는 원칙적으로 <strong>상속개시일이 속하는 달의 말일부터 6개월 이내</strong> 신고·납부해야 하며, 넘기면 가산세가 부과될 수 있습니다.</p></details>
  <details class="faq-acc"><summary><span>Q</span>상속인이 연락이 안 되거나 협조하지 않으면?</summary><p><b>A.</b> 한 명이라도 협의가 안 되면 협의분할등기는 어렵습니다. <strong>법정지분 상속등기 또는 상속재산분할심판</strong>을 검토할 수 있습니다.</p></details>
  <details class="faq-acc"><summary><span>Q</span>빚이 있는지 정확히 모르면?</summary><p><b>A.</b> 재산·채무를 먼저 확인해야 합니다. 채무가 걱정된다면 원칙적으로 <strong>상속 사실을 안 날부터 3개월 이내</strong> 상속포기·한정승인을 검토해야 합니다.</p></details>
  <details class="faq-acc"><summary><span>Q</span>상속포기 예정인데 예금을 인출해도 되나요?</summary><p><b>A.</b> 주의해야 합니다. 상속재산을 임의로 처분하면 <strong>법정단순승인으로 판단될 수 있으므로</strong> 먼저 상속포기·한정승인 여부를 검토하는 것이 좋습니다.</p></details>
</div></div></section>'''

# Replace the old process + FAQ block.
s, n2 = re.subn(r'<section class="section soft"><div class="container feature-grid">.*?</section>', new_mid, s, count=1, flags=re.S)
if n2 != 1:
    raise SystemExit(f'PROCESS/FAQ replacement count={n2}')

css = '''
<style>
/* INHERITANCE_INFOGRAPHIC_V1 */
.inheritance-overview{background:#fff!important}
.inheritance-flow{display:grid;grid-template-columns:1fr 34px 1fr 34px 1fr 34px 1fr 34px 1fr;align-items:center;margin-top:30px;padding:34px 28px;border:1px solid #e4e9ef;border-radius:20px;background:#fff;box-shadow:0 14px 40px rgba(28,48,72,.06)}
.flow-step{text-align:center;min-width:0}.flow-icon{width:64px;height:64px;margin:0 auto 14px;border-radius:19px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:950;color:#fff;box-shadow:0 8px 18px rgba(0,0,0,.10)}
.flow-blue .flow-icon{background:#368ee8}.flow-teal .flow-icon{background:#20a6a1}.flow-gold .flow-icon{background:#d8a52d}.flow-purple .flow-icon{background:#8a67d5}.flow-green .flow-icon{background:#42a76c}
.flow-step h3{font-size:17px;letter-spacing:-.6px;margin:0 0 4px}.flow-step p{font-size:12px;color:#727b87;margin:0 0 10px;white-space:nowrap}.flow-arrow{text-align:center;color:#b7c0ca;font-size:25px;font-weight:900}.deadline{display:inline-flex;align-items:center;justify-content:center;min-height:28px;padding:3px 10px;border-radius:999px;background:#eaf7fd;color:#168dca;border:1px solid #bfe5f7;font-size:11px;font-weight:900}.muted-deadline{background:#f4f6f8;color:#687482;border-color:#e1e5ea}.inheritance-note{margin-top:16px;padding:13px 16px;border-radius:10px;background:#f6fbfe;color:#52606d;font-size:12px;border:1px solid #dceef7}.faq-block{max-width:900px;margin:58px auto 0}.faq-title{font-size:30px!important;margin-bottom:20px}.faq-acc{background:#fff;border:1px solid #dfe5ec;border-radius:12px;margin:10px 0;overflow:hidden}.faq-acc summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:11px;padding:17px 19px;font-size:15px;font-weight:900;color:#26313d}.faq-acc summary::-webkit-details-marker{display:none}.faq-acc summary span{display:inline-flex;flex:0 0 29px;width:29px;height:29px;align-items:center;justify-content:center;border-radius:50%;background:#eaf7fd;color:#168dca;font-size:13px}.faq-acc summary:after{content:'+';margin-left:auto;color:#8793a0;font-size:21px}.faq-acc[open] summary:after{content:'−'}.faq-acc p{margin:0;padding:0 19px 18px 59px;color:#596572;font-size:13px;line-height:1.75}.faq-acc strong{color:#273746}
@media(max-width:900px){.inheritance-flow{grid-template-columns:1fr;padding:24px 18px}.flow-step{padding:7px 0}.flow-arrow{transform:rotate(90deg);height:28px;line-height:28px}.flow-step p{white-space:normal}.faq-block{margin-top:42px}}
@media(max-width:600px){.inheritance-overview .title{font-size:29px}.flow-icon{width:58px;height:58px;border-radius:17px}.faq-acc summary{padding:15px 14px;font-size:14px}.faq-acc p{padding:0 15px 16px 54px;font-size:12px}.inheritance-note{font-size:11px}}
</style>
'''
if 'INHERITANCE_INFOGRAPHIC_V1' not in s:
    s = s.replace('</head>', css + '</head>', 1)

p.write_text(s, encoding='utf-8')
print('inheritance.html updated')
