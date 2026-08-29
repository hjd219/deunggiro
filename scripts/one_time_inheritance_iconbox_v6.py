from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_ICON_BOX_V6 */'
if marker in s:
    print('already applied'); raise SystemExit(0)
css='''\n<style>\n/* INHERITANCE_ICON_BOX_V6 */\n.inheritance-flow .flow-icon{background:#fff!important;border:1px solid #dfe7ee!important;box-shadow:0 5px 14px rgba(31,41,55,.055)!important;border-radius:18px!important;padding:10px!important;color:inherit!important}\n.inheritance-flow .flow-icon svg{width:100%!important;height:100%!important;display:block!important}\n@media(max-width:700px){\n .inheritance-flow .flow-step .flow-icon{width:60px!important;height:60px!important;border-radius:17px!important;background:#fff!important;border:1px solid #dfe7ee!important;box-shadow:0 5px 14px rgba(31,41,55,.055)!important;padding:9px!important}\n}\n</style>\n'''
if '</head>' not in s: raise SystemExit('head close not found')
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding='utf-8')
print('inheritance icon box v6 applied')
