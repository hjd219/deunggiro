document.addEventListener('DOMContentLoaded',function(){
  const video=document.getElementById('dg-hero-video');
  if(video){
    video.src='/assets/deunggiro-hero-video.mp4.mp4';
    video.poster='/images/og-home.jpg';
    video.load();
    const p=video.play();
    if(p&&typeof p.catch==='function')p.catch(()=>{});
  }
  const photo=document.getElementById('dg-profile-photo');
  if(photo) photo.src='/assets/deunggiro-profile.png';
});
