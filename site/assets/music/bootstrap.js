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
   const sync=()=>{try{document.title=frame.contentDocument.title;}catch(e){}};frame.addEventListener('load',sync);sync();window.dispatchEvent(new Event('juju:reading-ready'));
  }catch(e){style.remove();for(const link of styles)link.disabled=false;document.body.replaceChildren(...original);}
 })().catch(()=>{});
})();
