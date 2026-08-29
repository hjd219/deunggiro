from pathlib import Path
p=Path('corporate.html')
s=p.read_text(encoding='utf-8')
if 'CORPORATE_ELECTRONIC_SIGNATURE_CARD_V1' in s:
    raise SystemExit(0)
css='''<style>\n/* CORPORATE_ELECTRONIC_SIGNATURE_CARD_V1 */\n.corp-faq-inner{max-width:1180px!important}\n.corp-faq-layout{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.65fr);gap:22px;align-items:stretch}\n.corp-auth-card{background:#fff;border:1px solid #dfe7ee;border-radius:18px;box-shadow:0 7px 20px rgba(31,41,55,.05);padding:27px;display:flex;flex-direction:column}\n.corp-auth-icon{width:60px;height:60px;border:1px solid #dfe7ee;border-radius:18px;display:flex;align-items:center;justify-content:center;margin-bottom:15px;box-shadow:0 5px 14px rgba(31,41,55,.055);background:#fff}\n.corp-auth-icon svg{width:36px;height:36px}.corp-auth-card h3{font-size:24px;margin:0 0 7px;letter-spacing:-1px}.corp-auth-desc{font-size:13px;color:#6b7680;margin:0 0 17px;line-height:1.55}\n.corp-auth-row{background:#f8fbfd;border:1px solid #e5edf2;border-radius:13px;padding:14px 15px;margin-bottom:10px}.corp-auth-label{font-size:12px;color:#168dca;font-weight:900;margin-bottom:5px}.corp-auth-main{font-size:15px;font-weight:900}.corp-auth-sub{font-size:12px;color:#707b85;margin-top:4px}\n.corp-auth-link{margin-top:auto;display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:10px;background:#36a9e1;color:#fff!important;font-size:14px;font-weight:900}.corp-auth-note{text-align:center;font-size:11px;color:#8b949e;margin-top:9px}\n@media(max-width:800px){.corp-faq-layout{grid-template-columns:1fr}.corp-auth-card{padding:23px}}\n</style>'''
s=s.replace('</head>',css+'</head>',1)
old='<div class="corp-faq">'
new='''<div class="corp-faq-layout"><div class="corp-faq">'''
s=s.replace(old,new,1)
needle='</div></div></section><script>document.addEventListener(\'click\',function(e){const b=e.target.closest(\'.corp-faq-q\');'
card='''</div><aside class="corp-auth-card"><div class="corp-auth-icon"><svg viewBox="0 0 48 48" fill="none"><path d="M24 5 38 10v11c0 10-6 17-14 22C16 38 10 31 10 21V10L24 5Z" stroke="#36a9e1" stroke-width="3"/><path d="m17 24 5 5 10-11" stroke="#8b5cf6" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div><h3>전자서명·인증</h3><p class="corp-auth-desc">법인 전자등기 진행 시 필요한 인증수단을 확인하세요.</p><div class="corp-auth-row"><div class="corp-auth-label">개인</div><div class="corp-auth-main">공동인증서 · 금융인증서</div><div class="corp-auth-sub">주주·임원 등 개인 전자서명</div></div><div class="corp-auth-row"><div class="corp-auth-label">법인</div><div class="corp-auth-main">법인 전자증명서</div><div class="corp-auth-sub">법인의 전자서명·인증</div></div><a class="corp-auth-link" href="https://www.iros.go.kr/" target="_blank" rel="noopener">인터넷등기소 전자서명 바로가기 →</a><div class="corp-auth-note">대한민국 법원 인터넷등기소로 이동합니다.</div></aside></div></div></section><script>document.addEventListener('click',function(e){const b=e.target.closest('.corp-faq-q');'''
if needle not in s:
    raise SystemExit('FAQ closing marker not found')
s=s.replace(needle,card,1)
p.write_text(s,encoding='utf-8')
