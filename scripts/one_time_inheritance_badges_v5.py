from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<span class="deadline">1개월</span>','<span class="deadline">1개월 이내</span>',1)
s=s.replace('<span class="deadline muted-deadline">재산조회</span>','<span class="deadline">조회 약 20일</span>',1)
s=s.replace('<span class="deadline">3개월</span>','<span class="deadline">3개월 이내</span>',1)
old='<div class="flow-step flow-purple"><div class="flow-icon"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="19" r="10" class="purple"/><circle cx="15" cy="27" r="8" fill="#b790e5"/><circle cx="49" cy="27" r="8" fill="#b790e5"/><path d="M16 55c1-14 7-22 16-22s15 8 16 22" fill="#9162ce"/><path d="M2 55c1-11 5-17 13-17 4 0 7 2 9 5-2 4-3 8-3 12zM62 55c-1-11-5-17-13-17-4 0-7 2-9 5 2 4 3 8 3 12z" fill="#c6a9e9"/></svg></div><h3>상속인 협의</h3><p>분할방법 협의</p></div>'
new=old[:-6]+'<span class="deadline">전원 합의</span></div>'
if old not in s: raise SystemExit('target inheritance agreement step not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('inheritance badges v5 applied')
