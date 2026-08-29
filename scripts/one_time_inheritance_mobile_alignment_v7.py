from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_MOBILE_ALIGNMENT_V7 */'
if marker in s:
    print('already applied'); raise SystemExit(0)
css='''\n<style>\n/* INHERITANCE_MOBILE_ALIGNMENT_V7 */\n@media(max-width:700px){\n  .inheritance-flow .flow-step{\n    display:grid!important;\n    grid-template-columns:132px minmax(0,1fr) auto!important;\n    grid-template-rows:auto auto!important;\n    column-gap:14px!important;\n    row-gap:4px!important;\n    align-items:center!important;\n    text-align:left!important;\n    width:100%!important;\n    padding:18px 0!important;\n  }\n  .inheritance-flow .flow-step .flow-icon{\n    grid-column:1!important;\n    grid-row:1 / span 2!important;\n    width:60px!important;\n    height:60px!important;\n    margin-left:0!important;\n    justify-self:start!important;\n  }\n  .inheritance-flow .flow-step h3{\n    grid-column:2!important;\n    grid-row:1!important;\n    margin:0!important;\n    line-height:1.28!important;\n    white-space:normal!important;\n  }\n  .inheritance-flow .flow-step p{\n    grid-column:2!important;\n    grid-row:2!important;\n    margin:0!important;\n    padding:0!important;\n    line-height:1.45!important;\n    white-space:normal!important;\n  }\n  .inheritance-flow .flow-step .deadline{\n    grid-column:3!important;\n    grid-row:1 / span 2!important;\n    justify-self:end!important;\n    align-self:center!important;\n    margin:0!important;\n    white-space:nowrap!important;\n  }\n  .inheritance-flow .flow-arrow{\n    width:60px!important;\n    margin-left:0!important;\n    text-align:center!important;\n  }\n}\n</style>\n'''
if '</body>' not in s: raise SystemExit('body close not found')
s=s.replace('</body>',css+'</body>',1)
p.write_text(s,encoding='utf-8')
print('inheritance mobile alignment v7 applied')
