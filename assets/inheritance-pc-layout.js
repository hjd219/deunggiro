/* INHERITANCE_PC_LAYOUT_V10 */
(function(){
  const overview=document.querySelector('.inheritance-overview>.container');
  const faq=overview&&overview.querySelector('.faq-block');
  const docs=document.getElementById('documents');
  if(!overview||!faq||!docs) return;

  faq.querySelectorAll('details[open]').forEach(d=>d.removeAttribute('open'));

  const faqPh=document.createComment('inheritance-faq-original-position');
  const docsPh=document.createComment('inheritance-docs-original-position');
  faq.parentNode.insertBefore(faqPh,faq);
  docs.parentNode.insertBefore(docsPh,docs);

  const lower=document.createElement('div');
  lower.className='inheritance-pc-lower';
  const mq=window.matchMedia('(min-width:801px)');

  function applyLayout(){
    if(mq.matches){
      if(!lower.isConnected) faqPh.parentNode.insertBefore(lower,faqPh);
      lower.appendChild(docs);
      lower.appendChild(faq);
    }else{
      if(faq.parentNode!==faqPh.parentNode) faqPh.parentNode.insertBefore(faq,faqPh.nextSibling);
      if(docs.parentNode!==docsPh.parentNode) docsPh.parentNode.insertBefore(docs,docsPh.nextSibling);
      if(lower.isConnected) lower.remove();
    }
  }
  applyLayout();
  if(mq.addEventListener) mq.addEventListener('change',applyLayout);
  else mq.addListener(applyLayout);
})();
