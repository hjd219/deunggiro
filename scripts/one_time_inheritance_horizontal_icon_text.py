from pathlib import Path

p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_ICON_TEXT_SIDE_V1 */'
css=r'''
/* INHERITANCE_ICON_TEXT_SIDE_V1 */
.inheritance-flow .flow-step,.inheritance-process .flow-step,.flow-wrap .flow-step{display:flex!important;align-items:center!important;text-align:left!important;gap:14px!important}
.inheritance-flow .flow-icon,.inheritance-process .flow-icon,.flow-wrap .flow-icon{flex:0 0 62px!important;width:62px!important;height:62px!important;margin:0!important}
.inheritance-flow .flow-content,.inheritance-process .flow-content,.flow-wrap .flow-content{flex:1!important;min-width:0!important}
.inheritance-flow .flow-step h3,.inheritance-process .flow-step h3,.flow-wrap .flow-step h3{margin:0 0 3px!important}
.inheritance-flow .flow-step p,.inheritance-process .flow-step p,.flow-wrap .flow-step p{margin:0!important}
.inheritance-flow .deadline,.inheritance-process .deadline,.flow-wrap .deadline{display:inline-flex!important;margin-top:6px!important}
@media(max-width:800px){
 .inheritance-flow .flow-step,.inheritance-process .flow-step,.flow-wrap .flow-step{display:flex!important;align-items:center!important;text-align:left!important;gap:13px!important}
 .inheritance-flow .flow-icon,.inheritance-process .flow-icon,.flow-wrap .flow-icon{flex-basis:56px!important;width:56px!important;height:56px!important}
}
'''
if marker in s:
    raise SystemExit('already applied')
# Discover the actual flow-step rule and make the layout generic too.
css += r'''
.flow-step{display:flex!important;align-items:center!important;text-align:left!important;gap:14px!important}
.flow-step>.flow-icon{flex:0 0 62px!important;width:62px!important;height:62px!important;margin:0!important}
.flow-step>.flow-icon+*{min-width:0}
@media(max-width:800px){.flow-step{display:flex!important;align-items:center!important;text-align:left!important}.flow-step>.flow-icon{flex:0 0 56px!important;width:56px!important;height:56px!important}}
'''
idx=s.rfind('</style>')
if idx<0: raise SystemExit('style close not found')
s=s[:idx]+css+s[idx:]
p.write_text(s,encoding='utf-8')
print('side layout applied')
