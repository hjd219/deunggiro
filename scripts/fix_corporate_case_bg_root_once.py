from pathlib import Path
p=Path('corporate.html')
s=p.read_text(encoding='utf-8')
old='<section class="section white dg-corporate-casehub" aria-labelledby="corporate-casehub-title">'
new='<section class="section dg-corporate-casehub" aria-labelledby="corporate-casehub-title">'
if old not in s:
    raise SystemExit('target section class not found')
s=s.replace(old,new,1)
old_css='.section.white.dg-corporate-casehub{padding-top:48px!important;padding-bottom:48px!important;background:var(--detail-sky,#eef6fb)!important}'
new_css='.dg-corporate-casehub{padding-top:48px!important;padding-bottom:48px!important}'
if old_css not in s:
    raise SystemExit('temporary specificity override not found')
s=s.replace(old_css,new_css,1)
p.write_text(s,encoding='utf-8')
