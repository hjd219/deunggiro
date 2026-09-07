/* DG_FIREBASE_COUNTER_V5 */
(()=>{
  const pending=[];
  let ready=false, doCount=null, doRender=null;
  const DEBUG=new URLSearchParams(location.search).get('counterdebug')==='1';

  function status(msg){
    if(!DEBUG) return;
    let el=document.getElementById('dg-counter-debug');
    if(!el){
      el=document.createElement('div');
      el.id='dg-counter-debug';
      el.style.cssText='position:fixed;left:10px;right:10px;bottom:10px;z-index:99999;padding:10px 12px;background:#111;color:#fff;border-radius:8px;font:12px/1.45 monospace;word-break:break-all';
      document.body.appendChild(el);
    }
    el.textContent='COUNTER: '+msg;
  }

  window.DGCounter={
    countOnce:function(kind){
      status('click received');
      if(ready && doCount) return doCount(kind);
      pending.push(String(kind||'calculator'));
      status('queued until Firebase ready');
    },
    refresh:function(){ if(ready&&doRender) return doRender(); }
  };

  (async()=>{
    const firebaseConfig={
      apiKey:"AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do",
      authDomain:"project-b08e5f3c-fa49-4ae6-933.firebaseapp.com",
      projectId:"project-b08e5f3c-fa49-4ae6-933",
      storageBucket:"project-b08e5f3c-fa49-4ae6-933.firebasestorage.app",
      messagingSenderId:"209298170572",
      appId:"1:209298170572:web:2c47a3779cf4a331039869"
    };
    try{
      status('loading Firebase SDK');
      const [{initializeApp},fs]=await Promise.all([
        import("https://www.gstatic.com/firebasejs/12.18.0/firebase-app.js"),
        import("https://www.gstatic.com/firebasejs/12.18.0/firebase-firestore.js")
      ]);
      const {initializeFirestore,doc,getDoc,updateDoc,increment}=fs;
      const app=initializeApp(firebaseConfig);
      const db=initializeFirestore(app,{},"default");
      const ref=doc(db,"counters","calculator");

      doRender=async()=>{
        const el=document.getElementById('dg-calculator-usage');
        try{
          const snap=await getDoc(ref);
          status('read ok: '+(snap.exists()?JSON.stringify(snap.data()):'document missing'));
          if(!el||!snap.exists()) return;
          const n=Number(snap.data().count||0);
          const num=el.querySelector('[data-count]');
          if(num) num.textContent=n.toLocaleString('ko-KR')+'회';
          el.hidden=false;
        }catch(e){status('READ ERROR '+(e.code||'')+' '+e.message);}
      };

      doCount=async(kind)=>{
        const key='dg-counter-counted-'+String(kind||'calculator');
        try{
          if(sessionStorage.getItem(key)==='1'){status('already counted this session');return;}
          status('writing to database "default"');
          await updateDoc(ref,{count:increment(1)});
          sessionStorage.setItem(key,'1');
          status('WRITE OK');
          await doRender();
        }catch(e){status('WRITE ERROR '+(e.code||'')+' '+e.message);}
      };

      ready=true;
      status('Firebase ready');
      while(pending.length) await doCount(pending.shift());
      if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',doRender);
      else doRender();
    }catch(e){status('INIT ERROR '+(e.code||'')+' '+e.message);}
  })();
})();