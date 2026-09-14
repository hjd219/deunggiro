from pathlib import Path
p=Path('corporate.html')
s=p.read_text(encoding='utf-8')
old='.dg-corporate-casehub{padding-top:48px!important;padding-bottom:48px!important;background:#eef6fb!important}'
new='.section.white.dg-corporate-casehub{padding-top:48px!important;padding-bottom:48px!important;background:var(--detail-sky,#eef6fb)!important}'
if s.count(old)!=1:
    raise SystemExit(f'expected 1 target, found {s.count(old)}')
p.write_text(s.replace(old,new,1),encoding='utf-8')
