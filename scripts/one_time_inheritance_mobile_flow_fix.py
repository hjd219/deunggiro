from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_MOBILE_FLOW_FIX_V3 */'
css='''
<style>
/* INHERITANCE_MOBILE_FLOW_FIX_V3 */
@media(max-width:700px){
  .inheritance-flow{display:block!important;padding:18px 16px!important}
  .inheritance-flow .flow-step{display:grid!important;grid-template-columns:66px minmax(0,1fr)!important;grid-template-rows:auto auto auto!important;column-gap:14px!important;row-gap:3px!important;align-items:center!important;text-align:left!important;padding:17px 0!important;position:relative!important;min-width:0!important}
  .inheritance-flow .flow-step .flow-icon{grid-column:1!important;grid-row:1 / span 3!important;width:60px!important;height:60px!important;margin:0!important;align-self:center!important;justify-self:start!important;flex:none!important}
  .inheritance-flow .flow-step h3{grid-column:2!important;grid-row:1!important;margin:0!important;padding:0!important;font-size:18px!important;line-height:1.3!important;letter-spacing:-.6px!important;white-space:normal!important;word-break:keep-all!important;overflow-wrap:normal!important;min-width:0!important;max-width:100%!important}
  .inheritance-flow .flow-step p{grid-column:2!important;grid-row:2!important;margin:2px 0 0!important;padding:0!important;font-size:13px!important;line-height:1.45!important;color:#727b87!important;white-space:normal!important;word-break:keep-all!important;overflow-wrap:normal!important;min-width:0!important;max-width:100%!important}
  .inheritance-flow .flow-step .deadline{grid-column:2!important;grid-row:3!important;position:static!important;justify-self:start!important;align-self:start!important;margin:7px 0 0!important;white-space:nowrap!important;min-width:0!important;width:auto!important;max-width:100%!important;padding:4px 10px!important;font-size:12px!important;line-height:1.2!important}
  .inheritance-flow .flow-arrow{display:block!important;height:24px!important;line-height:24px!important;transform:none!important;font-size:0!important;text-align:left!important;margin:0 0 0 18px!important;padding:0!important;position:relative!important}
  .inheritance-flow .flow-arrow:before{content:'↓'!important;font-size:28px!important;line-height:24px!important;color:#b7c0ca!important;font-weight:900!important}
  .inheritance-note{margin-top:14px!important}
}
</style>
'''
if marker not in s:
    s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding='utf-8')
print('mobile inheritance flow v3 fixed')
