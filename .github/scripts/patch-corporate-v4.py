from pathlib import Path
p = Path('corporate.html')
s = p.read_text(encoding='utf-8')
marker = 'CORPORATE_HERO_SKY_V4'
css = '''<style>
/* CORPORATE_HERO_SKY_V4 */
.subhero{background:#eef6fb!important}
.subhero::before,.subhero::after{background:transparent!important}
.corp-card-top{background:transparent!important;padding:0!important;margin:0 0 15px!important;border-radius:0!important}
.corp-card{display:flex!important;flex-direction:column!important}
.corp-card .corp-cost{margin-top:auto!important}
@media(min-width:901px){.corp-guide .corp-head,.corp-guide .corp-kicker,.corp-guide .corp-head h2,.corp-guide .corp-head p{text-align:left!important}}
</style>'''
if marker not in s:
    s = s.replace('</head>', css + '</head>', 1)
s = s.replace('상호 · 목적 · 자본금 · 1주의 금액', '상호 · 본점주소 · 목적 · 자본금 · 1주의 금액')
p.write_text(s, encoding='utf-8')
