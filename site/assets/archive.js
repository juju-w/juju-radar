(() => {
 const groups=[...document.querySelectorAll('.archive-group[data-date]')];if(groups.length<2)return;
 const rail=document.createElement('nav');rail.className='archive-rail';rail.setAttribute('aria-label','往期日期导航');
 const track=document.createElement('div');track.className='date-track';track.tabIndex=0;track.setAttribute('role','slider');track.setAttribute('aria-label','快速跳转日期');track.setAttribute('aria-orientation','vertical');track.setAttribute('aria-valuemin','0');track.setAttribute('aria-valuemax',String(groups.length-1));
 const preview=document.createElement('div');preview.className='date-preview';preview.hidden=true;preview.id='date-preview';track.setAttribute('aria-controls',preview.id);
 const count=Math.min(groups.length,50);track.style.height=Math.min(360,Math.max(64,(count-1)*12))+'px';
 const marks=Array.from({length:count},(_,i)=>{const m=document.createElement('span');m.className='date-mark';m.style.top=(i/(count-1)*100)+'%';m.setAttribute('aria-hidden','true');track.append(m);return m;});
 rail.append(track,preview);document.body.append(rail);document.querySelector('.archive-page')?.classList.add('with-date-rail');
 let active=0,hovered=-1,dragging=false,frame=0,hideTimer=0;
 function highlight(i){track.setAttribute('aria-valuenow',String(i));track.setAttribute('aria-valuetext',groups[i].dataset.date);const mark=Math.round(i/(groups.length-1)*(count-1));marks.forEach((m,j)=>m.classList.toggle('current',j===mark));}
 function hide(){preview.hidden=true;rail.classList.remove('expanded');hovered=-1;highlight(active);}
 function show(i){clearTimeout(hideTimer);i=Math.max(0,Math.min(groups.length-1,i));rail.classList.add('expanded');preview.hidden=false;highlight(i);if(i===hovered)return;hovered=i;
  const start=Math.max(0,Math.min(groups.length-5,i-2)),end=Math.min(groups.length,start+5);
  preview.replaceChildren(...groups.slice(start,end).map((g,k)=>{const idx=start+k,a=document.createElement('a'),date=document.createElement('span'),title=document.createElement('span');a.href='#'+g.id;a.className='date-option';a.classList.toggle('selected',idx===i);if(idx===active)a.setAttribute('aria-current','date');date.className='date-label';date.textContent=g.dataset.date;title.className='date-summary';title.textContent=g.querySelector('.archive-issue-title')?.textContent||'';a.append(date,title);a.onclick=e=>{e.preventDefault();jump(idx);save();hide();};return a;}));
  const available=innerHeight-28;preview.style.maxHeight=available+'px';const h=preview.offsetHeight,r=track.getBoundingClientRect();preview.style.top=Math.max(14,Math.min(innerHeight-h-14,r.top+i/(groups.length-1)*r.height-h/2))-rail.getBoundingClientRect().top+'px';
 }
 function jump(i){active=Math.max(0,Math.min(groups.length-1,i));window.scrollTo({top:Math.max(0,scrollY+groups[active].getBoundingClientRect().top-76),behavior:'instant'});highlight(active);}
 function at(e){const r=track.getBoundingClientRect();return Math.round(Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))*(groups.length-1));}
 function save(){history.replaceState(history.state,'',location.pathname+location.search+'#'+groups[active].id);}
 function sync(){frame=0;if(dragging)return;let i=0;groups.forEach((g,j)=>{if(g.getBoundingClientRect().top<=100)i=j;});if(scrollY+innerHeight>=document.documentElement.scrollHeight-2)i=groups.length-1;active=i;if(hovered<0)highlight(active);}
 track.onpointermove=e=>{const i=at(e);if(dragging)jump(i);if(e.pointerType!=='touch'||dragging)show(i);};
 track.onpointerenter=e=>{if(e.pointerType!=='touch')show(at(e));};
 track.onpointerdown=e=>{if(e.button!==0)return;dragging=true;rail.classList.add('dragging');track.setPointerCapture(e.pointerId);track.focus({preventScroll:true});e.preventDefault();const i=at(e);jump(i);show(i);};
 function release(){if(!dragging)return;dragging=false;rail.classList.remove('dragging');save();hideTimer=setTimeout(hide,900);}
 track.onpointerup=release;track.onpointercancel=release;track.onlostpointercapture=release;
 rail.onpointerenter=()=>clearTimeout(hideTimer);rail.onpointerleave=()=>{if(!dragging)hideTimer=setTimeout(hide,150);};
 track.onfocus=()=>show(active);rail.onfocusout=e=>{if(!rail.contains(e.relatedTarget)&&!dragging)hide();};
 track.onkeydown=e=>{let i=hovered<0?active:hovered;if(e.key==='Escape'){hide();return;}if(e.key==='Enter'||e.key===' '){e.preventDefault();jump(i);save();hide();return;}if(e.key==='ArrowDown')i++;else if(e.key==='ArrowUp')i--;else if(e.key==='Home')i=0;else if(e.key==='End')i=groups.length-1;else return;e.preventDefault();jump(i);show(active);save();};
 window.addEventListener('scroll',()=>{if(!frame)frame=requestAnimationFrame(sync);},{passive:true});window.addEventListener('resize',()=>{hide();sync();});sync();
})();
