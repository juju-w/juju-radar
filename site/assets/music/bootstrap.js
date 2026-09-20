/* Preserve server-rendered pages, then keep a persistent player around navigation. */
(() => {
 if(window.self!==window.top)return;
 const base=new URL('.',document.currentScript.src).href;
 const get=async name=>{const response=await fetch(base+name);if(!response.ok)throw Error('Music resource unavailable');return response.text();};
 const script=name=>new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=base+name;s.onload=resolve;s.onerror=reject;document.body.append(s);});
 (async()=>{
  // Fail quietly without replacing the article if optional music files are unavailable.
  const media=await fetch('/juju-radar/music-v1/playlist.json');if(!media.ok)return;
  const [markup,css]=await Promise.all([get('shell.html'),get('music.css')]);
  const frame=document.createElement('iframe');frame.id='site';frame.allow='clipboard-write';
  const policy=document.permissionsPolicy||document.featurePolicy;
  if(!policy?.features || policy.features().includes('web-share'))frame.allow+='; web-share';frame.title='Juju Radar reading area';frame.hidden=true;
  const loaded=new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('Reading frame timed out')),15000);frame.addEventListener('load',()=>{clearTimeout(timer);resolve();},{once:true});});
  frame.src=location.href;document.body.append(frame);
  try{await loaded;}catch(e){frame.remove();return;}
  const original=[...document.body.childNodes].filter(n=>n!==frame),styles=[...document.querySelectorAll('link[rel="stylesheet"]')];
  const template=document.createElement('template');template.innerHTML=markup;
  const style=document.createElement('style');style.textContent=css;
  try{
   for(const node of original)node.remove();
   for(const link of styles)link.disabled=true;
   document.head.append(style);frame.hidden=false;
   document.body.append(template.content);
   await script('liquid-glass.js');await script('player.js');
   const sync=()=>{
    try{
     const doc=frame.contentDocument,url=new URL(frame.contentWindow.location.href);
     if(url.origin!==location.origin||!url.pathname.startsWith('/juju-radar/'))return;
     // The iframe owns navigation history; mirror its current entry without adding a second entry.
     history.replaceState(history.state,'',url.pathname+url.search+url.hash);
     document.title=doc.title;
     for(const selector of ['link[rel="canonical"]','meta[name="description"]','meta[property="og:title"]','meta[property="og:description"]','meta[property="og:url"]']){
      const source=doc.querySelector(selector),target=document.querySelector(selector);
      if(source&&target){if(source.tagName==='LINK')target.href=source.href;else target.content=source.content;}
     }
     window.dispatchEvent(new Event('juju:reading-ready'));
    }catch(e){}
   };
   const bind=()=>{
    const win=frame.contentWindow;
    for(const name of ['pushState','replaceState']){
     const original=win.history[name].bind(win.history);
     win.history[name]=function(...args){const result=original(...args);sync();return result;};
    }
    win.addEventListener('popstate',sync);win.addEventListener('hashchange',sync);sync();
   };
   frame.addEventListener('load',bind);bind();
  }catch(e){style.remove();for(const link of styles)link.disabled=false;document.body.replaceChildren(...original);}
 })().catch(()=>{});
})();
