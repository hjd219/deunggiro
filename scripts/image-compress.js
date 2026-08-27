/* 등기로 CMS 이미지 자동압축 v1
 * admin.html에서 readImageAsDataURL(file)을 호출할 때 자동 적용할 수 있는 안전 모듈.
 * GIF/SVG는 원본 유지, 일반 사진은 최대 크기 축소 + WebP/JPEG 압축.
 */
(function(){
  'use strict';
  const DEFAULTS={maxWidth:1600,maxHeight:1600,quality:0.82,skipBytes:350*1024};

  function readRaw(file){
    return new Promise((resolve,reject)=>{
      const r=new FileReader();
      r.onload=()=>resolve(r.result);
      r.onerror=()=>reject(new Error('이미지를 읽지 못했습니다.'));
      r.readAsDataURL(file);
    });
  }

  function loadImage(dataUrl){
    return new Promise((resolve,reject)=>{
      const img=new Image();
      img.onload=()=>resolve(img);
      img.onerror=()=>reject(new Error('이미지를 불러오지 못했습니다.'));
      img.src=dataUrl;
    });
  }

  async function compressImageFile(file,opts={}){
    if(!file || !file.type || !file.type.startsWith('image/')) throw new Error('이미지 파일만 첨부할 수 있습니다.');
    const cfg={...DEFAULTS,...opts};
    const type=(file.type||'').toLowerCase();
    if(type==='image/gif' || type==='image/svg+xml' || file.size<=cfg.skipBytes) return readRaw(file);

    const original=await readRaw(file);
    const img=await loadImage(original);
    const scale=Math.min(1,cfg.maxWidth/img.naturalWidth,cfg.maxHeight/img.naturalHeight);
    const w=Math.max(1,Math.round(img.naturalWidth*scale));
    const h=Math.max(1,Math.round(img.naturalHeight*scale));
    const canvas=document.createElement('canvas');
    canvas.width=w; canvas.height=h;
    const ctx=canvas.getContext('2d',{alpha:type==='image/png'});
    if(!ctx) return original;
    ctx.drawImage(img,0,0,w,h);

    let out='';
    try{ out=canvas.toDataURL('image/webp',cfg.quality); }catch(e){}
    if(!out || !/^data:image\/webp/i.test(out)){
      try{ out=canvas.toDataURL(type==='image/png'?'image/png':'image/jpeg',cfg.quality); }catch(e){ out=original; }
    }
    // 압축 결과가 오히려 커지면 원본 유지
    return out.length < original.length ? out : original;
  }

  window.DeunggiroImageCompression={
    compressImageFile,
    thumbnail:file=>compressImageFile(file,{maxWidth:1200,maxHeight:1200,quality:0.80,skipBytes:250*1024}),
    body:file=>compressImageFile(file,{maxWidth:1600,maxHeight:1600,quality:0.82,skipBytes:350*1024})
  };
})();
