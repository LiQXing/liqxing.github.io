/* Pause the embedded animation when its section is out of view. */
(()=>{
  const preview=document.querySelector('.project-visual iframe');
  if(!preview||!('IntersectionObserver' in window)) return;
  const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
  let visible=false;
  function sync(){
    try{
      const button=preview.contentDocument?.getElementById('pause');
      if(!button)return;
      const paused=button.getAttribute('aria-pressed')==='true';
      const shouldRun=visible&&!document.hidden&&!reducedMotion.matches;
      if(paused===shouldRun)button.click();
    }catch{/* The full animation remains available through its own link. */}
  }
  new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;sync();},{rootMargin:'100px'}).observe(preview);
  preview.addEventListener('load',sync);
  reducedMotion.addEventListener('change',sync);
  document.addEventListener('visibilitychange',sync);
})();
