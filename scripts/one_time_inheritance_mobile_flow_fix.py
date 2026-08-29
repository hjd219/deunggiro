from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_MOBILE_FLOW_FIX_V2 */'
css='''
<style>
/* INHERITANCE_MOBILE_FLOW_FIX_V2 */
@media(max-width:700px){
  .inheritance-flow{display:block!important;padding:18px 16px!important}
  .flow-step{display:grid!important;grid-template-columns:72px minmax(0,1fr)!important;grid-template-rows:auto auto!important;column-gap:14px!important;row-gap:4px!important;align-items:center!important;text-align:left!important;padding:18px 0!important;position:relative!important}
  .flow-step .flow-icon{grid-column:1!important;grid-row:1 / span 2!important;width:64px!important;height:64px!important;margin:0!important;align-self:center!important}
  .flow-step h3{grid-column:2!important;grid-row:1!important;margin:0!important;font-size:20px!important;line-height:1.35!important;letter-spacing:-.7px!important;white-space:normal!important;word-break:keep-all!important;overflow-wrap:normal!important}
  .flow-step p{grid-column:2!important;grid-row:2!important;margin:0!important;font-size:13px!important;line-height:1.5!important;color:#727b87!important;white-space:normal!important;word-break:keep-all!important;overflow-wrap:normal!important;padding-right:0!important}
  .flow-step .deadline{grid-column:2!important;grid-row:3!important;justify-self:start!important;margin-top:7px!important;white-space:nowrap!important;min-width:0!important;width:auto!important;padding:4px 11px!important;font-size:12px!important;line-height:1.2!important}
  .flow-arrow{height:26px!important;line-height:26px!important;transform:none!important;font-size:0!important;text-align:left!important;margin-left:23px!important;position:relative!important}
  .flow-arrow:before{content:'↓';font-size:30px!important;line-height:26px!important;color:#b7c0ca!important;font-weight:900!important}
  .inheritance-note{margin-top:14px!important}
}
</style>
'''
if marker not in s:
    s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding='utf-8')
print('mobile inheritance flow fixed')
