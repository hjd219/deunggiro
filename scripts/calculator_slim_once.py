from pathlib import Path

p=Path('assets/home.css')
s=p.read_text(encoding='utf-8')
repls={
'font-size:14px}':'font-size:12.5px}',
'#calculator .calculator-usage strong{color:#199fd9;font-size:18px;margin-left:7px}':'#calculator .calculator-usage strong{color:#199fd9;font-size:16px;margin-left:6px}',
'#calculator .calculator-icon{width:88px;height:108px;margin:0 auto 5px;display:block}':'#calculator .calculator-icon{width:59px;height:108px;margin:0 auto 5px;display:block}',
'  #calculator .calculator-icon{width:60px;height:92px}':'  #calculator .calculator-icon{width:40px;height:92px}',
'  #calculator .calculator-icon{width:60px;height:84px}':'  #calculator .calculator-icon{width:40px;height:84px}'
}
for old,new in repls.items():
    if old not in s: raise SystemExit('missing CSS pattern: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

p=Path('assets/icons/calculator.svg')
s=p.read_text(encoding='utf-8')
old='<text x="126" y="41" text-anchor="end" font-size="22" font-weight="900" fill="#1f5f7d">9,999</text>'
new='''<g transform="translate(25 0) scale(.6667 1)"><text x="126" y="41" text-anchor="end" font-size="22" font-weight="900" fill="#1f5f7d">9,999</text></g>'''
if old not in s: raise SystemExit('missing calculator display')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
