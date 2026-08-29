from pathlib import Path

p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
repls={
'<div class="flow-icon">申</div>':'<div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="14" y="8" width="36" height="48" rx="6" class="white"/><rect x="14" y="8" width="36" height="48" rx="6" fill="none" stroke="#438fe5" stroke-width="3"/><rect x="21" y="20" width="22" height="4" rx="2" class="bluefill"/><rect x="21" y="29" width="18" height="4" rx="2" class="bluefill"/><circle cx="44" cy="46" r="10" class="bluefill"/><path d="M39 46l3 3 6-7" fill="none" stroke="white" stroke-width="3"/></svg></div>',
'<div class="flow-icon">⌕</div>':'<div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="9" y="9" width="35" height="44" rx="6" class="white" stroke="#2eb59a" stroke-width="3"/><rect x="16" y="20" width="19" height="4" rx="2" class="teal"/><rect x="16" y="29" width="14" height="4" rx="2" class="teal"/><circle cx="43" cy="42" r="11" fill="#d7f5ee" stroke="#2eb59a" stroke-width="4"/><path d="M51 50l8 8" stroke="#2eb59a" stroke-width="5" stroke-linecap="round"/></svg></div>',
'<div class="flow-icon">⚖</div>':'<div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><rect x="29" y="10" width="6" height="42" rx="3" class="dark"/><rect x="11" y="17" width="42" height="5" rx="2.5" class="gold"/><path d="M17 22l-9 18h18zM47 22l-9 18h18z" class="gold"/><rect x="21" y="51" width="22" height="6" rx="3" class="dark"/></svg></div>',
'<div class="flow-icon">協</div>':'<div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="19" r="10" class="purple"/><circle cx="15" cy="27" r="8" fill="#b790e5"/><circle cx="49" cy="27" r="8" fill="#b790e5"/><path d="M16 55c1-14 7-22 16-22s15 8 16 22" fill="#9162ce"/><path d="M2 55c1-11 5-17 13-17 4 0 7 2 9 5-2 4-3 8-3 12zM62 55c-1-11-5-17-13-17-4 0-7 2-9 5 2 4 3 8 3 12z" fill="#c6a9e9"/></svg></div>',
'<div class="flow-icon">登</div>':'<div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M7 30L32 9l25 21-5 5-20-17-20 17z" class="green"/><rect x="13" y="30" width="38" height="27" rx="3" class="white" stroke="#43a965" stroke-width="3"/><rect x="27" y="39" width="11" height="18" rx="2" fill="#bce6c9"/><circle cx="49" cy="16" r="10" class="green"/><path d="M44 16l3 3 7-8" fill="none" stroke="white" stroke-width="3"/></svg></div>'
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit(f'missing icon marker: {a}')
    s=s.replace(a,b,1)
css='''.flow-icon{background:#fff!important;border:1px solid #e5eaf0;box-shadow:0 8px 18px rgba(20,40,65,.08)!important;padding:10px}.flow-icon svg{width:100%;height:100%;display:block}.flow-icon .white{fill:#fff}.flow-icon .bluefill{fill:#438fe5}.flow-icon .teal{fill:#2eb59a}.flow-icon .dark{fill:#4d5664}.flow-icon .gold{fill:#d9a72e}.flow-icon .purple{fill:#9162ce}.flow-icon .green{fill:#43a965}'''
marker='/* INHERITANCE_COLOR_ICON_FIX_V1 */'
if marker not in s:
    s=s.replace('</style>\n</head>',f'\n{marker}\n{css}\n</style>\n</head>',1)
p.write_text(s,encoding='utf-8')
print('icons fixed')
