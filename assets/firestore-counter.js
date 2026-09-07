/* DG_FIREBASE_COUNTER_V2 */
(async()=>{
  const firebaseConfig = {
    apiKey: "AIzaSyAlXYOrj7V-XtDrK13Cbxw6hWzbfhGf_do",
    authDomain: "project-b08e5f3c-fa49-4ae6-933.firebaseapp.com",
    projectId: "project-b08e5f3c-fa49-4ae6-933",
    storageBucket: "project-b08e5f3c-fa49-4ae6-933.firebasestorage.app",
    messagingSenderId: "209298170572",
    appId: "1:209298170572:web:2c47a3779cf4a331039869",
    measurementId: "G-PGFPK2SJLK"
  };

  try{
    const [{ initializeApp }, firestore] = await Promise.all([
      import("https://www.gstatic.com/firebasejs/12.18.0/firebase-app.js"),
      import("https://www.gstatic.com/firebasejs/12.18.0/firebase-firestore.js")
    ]);
    const { getFirestore, doc, getDoc, updateDoc, increment } = firestore;
    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    const ref = doc(db,"counters","calculator");

    async function render(){
      const el=document.getElementById('dg-calculator-usage');
      if(!el) return;
      try{
        const snap=await getDoc(ref);
        if(!snap.exists()) return;
        const n=Number(snap.data().count||0);
        const num=el.querySelector('[data-count]');
        if(num) num.textContent=n.toLocaleString('ko-KR')+'회';
        el.hidden=false;
      }catch(e){}
    }

    window.DGCounter={
      countOnce:async function(kind){
        const key='dg-counter-counted-'+String(kind||'calculator');
        try{
          if(sessionStorage.getItem(key)==='1') return;
          await updateDoc(ref,{count:increment(1)});
          sessionStorage.setItem(key,'1');
        }catch(e){}
      },
      refresh:render
    };

    if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',render);
    else render();
  }catch(e){}
})();