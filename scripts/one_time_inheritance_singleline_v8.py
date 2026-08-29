from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_MOBILE_SINGLELINE_V8 */'
if marker not in s:
    css='''\n<style>\n/* INHERITANCE_MOBILE_SINGLELINE_V8 */\n@media(max-width:700px){\n .inheritance-flow .flow-step{grid-template-columns:132px minmax(0,1fr) auto!important;column-gap:10px!important}\n .inheritance-flow .flow-step h3{font-size:16px!important;letter-spacing:-.8px!important;white-space:nowrap!important;word-break:keep-all!important;overflow-wrap:normal!important;max-width:none!important}\n .inheritance-flow .flow-step p{font-size:12px!important;letter-spacing:-.45px!important;white-space:nowrap!important;word-break:keep-all!important;overflow-wrap:normal!important;max-width:none!important}\n .inheritance-flow .flow-step .deadline{font-size:11px!important;padding:4px 8px!important}\n}\n</style>\n'''
    s=s.replace('</body></html>',css+'</body></html>')
    p.write_text(s,encoding='utf-8')
