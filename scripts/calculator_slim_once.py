from pathlib import Path

p=Path('assets/home.css')
s=p.read_text(encoding='utf-8')
repls={
'#calculator .calculator-usage{display:inline-block;background:#fff;border:1px solid #b7e2f5;border-radius:25px;padding:9px 16px;margin:0;font-weight:800;color:#445362;font-size:14px}':'#calculator .calculator-usage{display:inline-block;background:#fff;border:1px solid #b7e2f5;border-radius:25px;padding:8px 14px;margin:0;font-weight:800;color:#445362;font-size:12.5px}',
'#calculator .calculator-usage strong{color:#199fd9;font-size:18px;margin-left:7px}':'#calculator .calculator-usage strong{color:#199fd9;font-size:16px;margin-left:6px}',
'#calculator .calculator-icon{width:88px;height:108px;margin:0 auto 5px;display:block}':'#calculator .calculator-icon{width:59px;height:108px;margin:0 auto 5px;display:block}',
'  #calculator .calculator-icon{width:60px;height:92px}':'  #calculator .calculator-icon{width:40px;height:92px}',
'  #calculator .calculator-icon{width:60px;height:84px}':'  #calculator .calculator-icon{width:40px;height:84px}'
}
for old,new in repls.items():
    if s.count(old)!=1:
        raise SystemExit(f'CSS pattern mismatch: {old[:55]} count={s.count(old)}')
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 168">
<g transform="translate(25 0) scale(.6667 1)">
<rect x="5" y="3" width="140" height="162" rx="20" fill="#69c5ed"/>
<rect x="16" y="15" width="118" height="38" rx="8" fill="#eaf8fe"/>
<g text-anchor="end" font-size="22" font-weight="900" fill="#1f5f7d">
<text x="126" y="41">0<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.98;1" dur="0.25s" begin="0s" fill="freeze"/></text>
<text x="126" y="41" opacity="0">2,350<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" dur="0.25s" begin="0.25s" fill="freeze"/></text>
<text x="126" y="41" opacity="0">5,000<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" dur="0.25s" begin="0.5s" fill="freeze"/></text>
<text x="126" y="41" opacity="0">7,500<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" dur="0.25s" begin="0.75s" fill="freeze"/></text>
<text x="126" y="41" opacity="0">9,999<animate attributeName="opacity" values="0;1" dur="0.01s" begin="1s" fill="freeze"/></text>
</g>
<g fill="#fff"><rect x="17" y="65" width="25" height="22" rx="5"/><rect x="47" y="65" width="25" height="22" rx="5"/><rect x="77" y="65" width="25" height="22" rx="5"/><rect x="17" y="92" width="25" height="22" rx="5"/><rect x="47" y="92" width="25" height="22" rx="5"/><rect x="77" y="92" width="25" height="22" rx="5"/><rect x="17" y="119" width="25" height="22" rx="5"/><rect x="47" y="119" width="25" height="22" rx="5"/><rect x="77" y="119" width="25" height="22" rx="5"/></g>
<rect x="108" y="65" width="25" height="22" rx="5" fill="#cceeff"/><rect x="108" y="92" width="25" height="22" rx="5" fill="#cceeff"/><rect x="108" y="119" width="25" height="22" rx="5" fill="#ff8f7d"/>
<g text-anchor="middle" font-size="16" font-weight="900" fill="#3482a7"><text x="29.5" y="81">7</text><text x="59.5" y="81">8</text><text x="89.5" y="81">9</text><text x="29.5" y="108">4</text><text x="59.5" y="108">5</text><text x="89.5" y="108">6</text><text x="29.5" y="135">1</text><text x="59.5" y="135">2</text><text x="89.5" y="135">3</text><text x="120.5" y="81">+</text><text x="120.5" y="108">−</text></g>
<text x="120.5" y="136" text-anchor="middle" font-size="17" font-weight="900" fill="#fff">=</text>
</g>
</svg>'''
Path('assets/icons/calculator.svg').write_text(svg,encoding='utf-8')

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='/assets/icons/calculator.svg" alt="계산기"'
if s.count(old)!=2:
    raise SystemExit(f'calculator refs count={s.count(old)}')
s=s.replace(old,'/assets/icons/calculator.svg?v=20260913-slim-count" alt="계산기"')
oldcss='/assets/home.css?v=20260913-mobile-recovery-1'
if s.count(oldcss)!=1:
    raise SystemExit(f'home css ref count={s.count(oldcss)}')
s=s.replace(oldcss,'/assets/home.css?v=20260913-calculator-slim')
p.write_text(s,encoding='utf-8')
