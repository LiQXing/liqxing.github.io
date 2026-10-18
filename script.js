(()=>{
  'use strict';
  const $=s=>document.querySelector(s),reduced=matchMedia('(prefers-reduced-motion: reduce)');
  // Older generated pages gain the store entrance without rewriting article files.
  const homeLink=$('.nav-brand'),base=homeLink.getAttribute('href').replace(/index\.html$/,'');
  const mainNav=$('.top-nav>nav'),sideNav=$('#site-menu>nav');
  if(!mainNav.querySelector('a[href$="shop.html"]')){
    const link=document.createElement('a');link.href=base+'shop.html';link.textContent='小店';mainNav.insertBefore(link,$('#theme-toggle'));
  }
  if(!sideNav.querySelector('a[href$="shop.html"]')){
    const link=document.createElement('a');link.href=base+'shop.html';link.append('◇ ');const label=document.createElement('span');label.textContent='我的小店';link.append(label);sideNav.insertBefore(link,sideNav.querySelector('a[href$="about.html"]').nextSibling);
  }
  const menu=$('#site-menu'),toggle=$('#menu-toggle'),backdrop=$('#menu-backdrop');
  function setMenu(open){menu.classList.toggle('open',open);menu.inert=!open;toggle.setAttribute('aria-expanded',String(open));backdrop.hidden=!open;document.body.classList.toggle('menu-open',open);(open?$('#menu-close'):toggle).focus();}
  toggle.addEventListener('click',()=>setMenu(!menu.classList.contains('open')));$('#menu-close').addEventListener('click',()=>setMenu(false));backdrop.addEventListener('click',()=>setMenu(false));
  menu.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const a=[...menu.querySelectorAll('a,button')],first=a[0],last=a.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('open'))setMenu(false);});
  const theme=$('#theme-toggle');function updateTheme(){const dark=document.documentElement.dataset.theme==='dark';theme.textContent=dark?'☀':'◐';theme.setAttribute('aria-label',dark?'切换到日间模式':'切换到夜间模式');theme.setAttribute('aria-pressed',String(dark));}
  theme.addEventListener('click',()=>{const value=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=value;try{localStorage.setItem('liqxing-theme',value);}catch{}updateTheme();});updateTheme();
  let pending=false;function scroll(){pending=false;const d=document.documentElement.scrollHeight-innerHeight;$('#reading-progress').style.width=(d>0?Math.min(100,scrollY/d*100):0)+'%';$('.top-nav').classList.toggle('scrolled',scrollY>80);$('.back-top').classList.toggle('visible',scrollY>500);}
  addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(scroll);}},{passive:true});scroll();
  const cards=[...document.querySelectorAll('.post-card')],search=$('#post-search');
  if(search){
    const records=new Map((window.BLOG_SEARCH||[]).map(p=>[p.id,(p.title+' '+p.text+' '+p.category).toLocaleLowerCase()])),params=new URLSearchParams(location.search),filters=[...document.querySelectorAll('[data-filter]')];
    let category=params.get('category')||'all',page=Math.max(1,Number(params.get('page'))||1);search.value=params.get('q')||'';if(!filters.some(b=>b.dataset.filter===category))category='all';
    function render(){const q=search.value.trim().toLocaleLowerCase(),words=q.split(/\s+/).filter(Boolean),matches=cards.filter(c=>(category==='all'||c.dataset.category===category)&&words.every(w=>(records.get(c.dataset.id)||c.textContent.toLocaleLowerCase()).includes(w))),total=Math.ceil(matches.length/8);page=Math.min(Math.max(1,page),Math.max(1,total));const show=new Set(matches.slice((page-1)*8,page*8));cards.forEach(c=>{c.hidden=!show.has(c);});filters.forEach(b=>{const active=b.dataset.filter===category;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});$('#result-count').textContent=q||category!=='all'?`找到 ${matches.length} 篇文章`:'';$('#empty-state').hidden=matches.length>0;const pagination=$('#pagination');pagination.replaceChildren();if(total>1)for(let n=1;n<=total;n++){const b=document.createElement('button');b.type='button';b.textContent=String(n);b.setAttribute('aria-label',`第 ${n} 页`);if(n===page){b.className='active';b.setAttribute('aria-current','page');}b.addEventListener('click',()=>{page=n;render();$('#posts').scrollIntoView({behavior:reduced.matches?'instant':'smooth'});});pagination.append(b);}const next=new URLSearchParams();if(q)next.set('q',search.value.trim());if(category!=='all')next.set('category',category);if(page>1)next.set('page',String(page));try{history.replaceState(null,'',location.pathname+(next.size?'?'+next:'')+location.hash);}catch{}}
    search.addEventListener('input',()=>{page=1;render();});$('.search-form').addEventListener('submit',e=>e.preventDefault());filters.forEach(b=>b.addEventListener('click',()=>{category=b.dataset.filter;page=1;render();}));$('#clear-search').addEventListener('click',()=>{search.value='';category='all';page=1;render();});document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();search.focus();search.scrollIntoView({block:'center',behavior:reduced.matches?'instant':'smooth'});}});render();
  }
  const article=$('.article-body'),toc=$('#toc');
  if(article){
    const headings=[...article.querySelectorAll('h1,h2,h3,h4')].filter(h=>h.textContent.trim());headings.forEach((h,i)=>{if(!h.id)h.id='section-'+i;const a=document.createElement('a');a.href='#'+encodeURIComponent(h.id);a.textContent=h.textContent;a.className='toc-level-'+h.tagName.slice(1);toc.append(a);});if(!headings.length)toc.textContent='这篇文章没有分节标题。';
    if('IntersectionObserver' in window){const o=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)toc.querySelectorAll('a').forEach(a=>a.classList.toggle('active',a.hash==='#'+encodeURIComponent(e.target.id)));}),{rootMargin:'-5% 0px -70% 0px'});headings.forEach(h=>o.observe(h));}
    article.querySelectorAll('pre').forEach(pre=>{const code=pre.querySelector('code');if(code&&window.hljs)try{hljs.highlightElement(code);}catch{}const tools=document.createElement('div');tools.className='code-toolbar';const label=document.createElement('span');label.className='code-language';label.textContent=code?.className.match(/language-([\w+-]+)/)?.[1]||'CODE';const dots=document.createElement('span');dots.className='mac-dots';dots.setAttribute('aria-hidden','true');const copy=document.createElement('button');copy.type='button';copy.textContent='复制';copy.addEventListener('click',async()=>{const text=code?.textContent||pre.textContent;try{await navigator.clipboard.writeText(text);copy.textContent='已复制';}catch{const t=document.createElement('textarea');t.value=text;t.style.cssText='position:fixed;opacity:0';document.body.append(t);t.select();copy.textContent=document.execCommand('copy')?'已复制':'请手动复制';t.remove();}setTimeout(()=>{copy.textContent='复制';},1800);});tools.append(dots,label,copy);const wrapper=document.createElement('div');wrapper.className='code-block';pre.before(wrapper);wrapper.append(tools,pre);});
    const dialog=$('#image-dialog'),large=dialog.querySelector('img');article.querySelectorAll('img').forEach(img=>{img.tabIndex=0;img.setAttribute('role','button');img.setAttribute('aria-label','放大图片：'+(img.alt||'文章配图'));const open=()=>{large.src=img.src;large.alt=img.alt;dialog.showModal();};img.addEventListener('click',open);img.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();open();}});});dialog.querySelector('button').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  }
  const phrases=['用我三生烟火，换你一世迷离','长街长，烟花繁，你挑灯回看','似此星辰非昨夜，为谁风露立中宵','如花美眷，似水流年','寄君一曲，不问曲终人聚散'];let phrase=0;
  document.addEventListener('click',e=>{if(reduced.matches||e.target.closest('a,button,input,textarea,pre,.aplayer,dialog'))return;const item=document.createElement('span');item.className='click-poem';item.textContent=phrases[phrase++%phrases.length];item.style.left=Math.min(e.clientX,innerWidth-260)+'px';item.style.top=e.clientY+'px';document.body.append(item);setTimeout(()=>item.remove(),1600);for(let n=0;n<7;n++){const p=document.createElement('i');p.className='click-particle';p.style.cssText=`left:${e.clientX}px;top:${e.clientY}px;--dx:${Math.cos(n/7*Math.PI*2)*48}px;--dy:${Math.sin(n/7*Math.PI*2)*48}px;--tone:${210+n*15}`;document.body.append(p);setTimeout(()=>p.remove(),800);}});
  const originalTitle=document.title;let titleTimer;document.addEventListener('visibilitychange',()=>{clearTimeout(titleTimer);if(document.hidden)titleTimer=setTimeout(()=>{document.title='下次再见～';},500);else{document.title='欢迎回来～';titleTimer=setTimeout(()=>{document.title=originalTitle;},1000);}});
  setTimeout(async()=>{
    if(window.aplayers?.length||!window.APlayer)return;
    try{
      const response=await fetch('https://api.i-meto.com/meting/api?server=netease&type=playlist&id=7002443469',{signal:AbortSignal.timeout(12000)});
      if(!response.ok)return;const tracks=await response.json();if(!Array.isArray(tracks)||!tracks.length||window.aplayers?.length)return;
      const audio=tracks.map(t=>({name:t.name||t.title||'未命名歌曲',artist:t.artist||t.author||'',url:t.url,cover:t.cover||t.pic,lrc:t.lrc}));
      const player=new APlayer({container:$('#aplayer'),audio,fixed:true,autoplay:true,order:'random',volume:0.6,listFolded:true,lrcType:audio[0].lrc?3:0,theme:'#807dd4'});
      (window.aplayers||=[]).push(player);
    }catch{/* The permanent NetEase playlist link remains available. */}
  },6000);
})();
