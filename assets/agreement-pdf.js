/* Shared client-side agreement PDF export (no personal form data sent to a server). */
(()=>{
  'use strict';
  let loader=null;
  const sources=[
    'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/html2pdf.js@0.10.1/dist/html2pdf.bundle.min.js'
  ];
  function importOne(url){
    return new Promise((resolve,reject)=>{
      const script=document.createElement('script');
      script.src=url;
      script.async=true;
      script.onload=()=>window.html2pdf?resolve():reject(new Error('PDF library unavailable'));
      script.onerror=()=>{script.remove();reject(new Error('PDF library load failed'))};
      document.head.appendChild(script);
    });
  }
  function load(){
    if(window.html2pdf)return Promise.resolve();
    if(!loader)loader=(async()=>{
      let lastError;
      for(const url of sources){
        try{await importOne(url);return}catch(e){lastError=e}
      }
      throw lastError||new Error('PDF 기능을 불러오지 못했습니다.');
    })().catch(e=>{loader=null;throw e});
    return loader;
  }
  async function save(source,filename){
    if(!source)throw new Error('PDF 내용을 찾지 못했습니다.');
    await load();
    if(document.fonts&&document.fonts.ready)await document.fonts.ready;
    const copy=source.cloneNode(true);
    copy.style.boxSizing='border-box';
    copy.style.width='180mm';
    copy.style.maxWidth='180mm';
    copy.style.padding='0';
    copy.style.margin='0';
    copy.style.background='#fff';
    copy.style.color='#222';
    copy.style.fontFamily="'Malgun Gothic','Apple SD Gothic Neo',sans-serif";
    copy.style.fontSize='13px';
    copy.style.lineHeight='1.8';
    copy.style.overflow='visible';
    const options={
      margin:[15,15,15,15], filename,
      image:{type:'jpeg',quality:0.97},
      html2canvas:{scale:window.innerWidth<600?1.35:1.7,useCORS:true,backgroundColor:'#fff',logging:false,scrollY:0},
      jsPDF:{unit:'mm',format:'a4',orientation:'portrait'},
      pagebreak:{mode:['css','legacy'],avoid:['p']}
    };
    await window.html2pdf().set(options).from(copy).save();
  }
  window.DGAgreementPDF={save};
})();
