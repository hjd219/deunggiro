from pathlib import Path
p=Path('inheritance.html')
s=p.read_text(encoding='utf-8')
marker='/* INHERITANCE_MOBILE_FLOW_FIX_V4 */'
css='''
<style>
/* INHERITANCE_MOBILE_FLOW_FIX_V4 */
@media(max-width:700px){
  .inheritance-flow{
    display:block!important;
    padding:18px 16px!important;
  }
  .inheritance-flow .flow-step{
    display:grid!important;
    grid-template-columns:64px minmax(0,1fr)!important;
    grid-template-rows:auto auto auto!important;
    column-gap:14px!important;
    row-gap:5px!important;
    align-items:start!important;
    text-align:left!important;
    padding:18px 0!important;
    position:relative!important;
    min-width:0!important;
    width:100%!important;
    height:auto!important;
  }
  .inheritance-flow .flow-step > *{
    position:static!important;
    float:none!important;
    transform:none!important;
    min-width:0!important;
    max-width:100%!important;
  }
  .inheritance-flow .flow-step .flow-icon{
    grid-column:1!important;
    grid-row:1 / span 3!important;
    width:58px!important;
    height:58px!important;
    margin:0!important;
    align-self:start!important;
    justify-self:start!important;
    flex:none!important;
  }
  .inheritance-flow .flow-step h3{
    grid-column:2!important;
    grid-row:1!important;
    display:block!important;
    margin:0!important;
    padding:0!important;
    font-size:18px!important;
    line-height:1.35!important;
    letter-spacing:-.6px!important;
    white-space:normal!important;
    word-break:keep-all!important;
    overflow-wrap:break-word!important;
    width:auto!important;
  }
  .inheritance-flow .flow-step p{
    grid-column:2!important;
    grid-row:2!important;
    display:block!important;
    margin:0!important;
    padding:0!important;
    font-size:13px!important;
    line-height:1.5!important;
    color:#727b87!important;
    white-space:normal!important;
    word-break:keep-all!important;
    overflow-wrap:break-word!important;
    width:auto!important;
  }
  .inheritance-flow .flow-step .deadline{
    grid-column:2!important;
    grid-row:3!important;
    display:inline-flex!important;
    justify-self:start!important;
    align-self:start!important;
    margin:3px 0 0!important;
    white-space:nowrap!important;
    width:auto!important;
    min-width:auto!important;
    max-width:none!important;
    padding:4px 10px!important;
    font-size:12px!important;
    line-height:1.2!important;
    inset:auto!important;
  }
  .inheritance-flow .flow-arrow{
    display:block!important;
    width:58px!important;
    height:28px!important;
    line-height:28px!important;
    margin:0!important;
    padding:0!important;
    text-align:center!important;
    font-size:0!important;
    position:relative!important;
  }
  .inheritance-flow .flow-arrow:before{
    content:'↓'!important;
    display:block!important;
    font-size:28px!important;
    line-height:28px!important;
    color:#b7c0ca!important;
    font-weight:900!important;
  }
  .inheritance-note{margin-top:14px!important}
}
</style>
'''
if marker not in s:
    s=s.replace('</head>',css+'</head>',1)
p.write_text(s,encoding='utf-8')
print('mobile inheritance flow v4 fixed')
