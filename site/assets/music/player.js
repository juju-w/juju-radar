(() => {
const $=id=>document.getElementById(id),audio=$('audio');let all=[],tracks=[],index=0,repeat='all',generation=0,shuffle=false,bag=[],history=[];
const icons={play:'<path d="m9 5 11 7-11 7z" fill="currentColor" stroke="none"/>',pause:'<path d="M9 5v14M16 5v14" stroke-width="3"/>',next:'<path d="m5 5 10 7L5 19z" fill="currentColor" stroke="none"/><path d="M19 5v14"/>',prev:'<path d="m19 5-10 7 10 7z" fill="currentColor" stroke="none"/><path d="M5 5v14"/>',loop:'<path d="m17 2 4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4M21 13v2a3 3 0 0 1-3 3H3"/>',list:'<path d="M4 6h16M4 12h16M4 18h10"/>',shuffle:'<path d="m16 3 4 4-4 4M4 7h3c4 0 6 10 10 10h3M16 13l4 4-4 4M4 17h3c1.4 0 2.6-1.2 3.8-3M14 9c1-1.2 2-2 3-2h3"/>',fold:'<path d="m9 5 7 7-7 7"/>',expand:'<path d="m15 5-7 7 7 7"/>',close:'<path d="m6 6 12 12M18 6 6 18"/>'};
function icon(id,key){$(id).innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true">'+icons[key]+'</svg>';}
for(const id of ['play','next','prev','loop','list','close','shuffle','fold'])icon(id,id);
const time=n=>Number.isFinite(n)?`${Math.floor(n/60)}:${String(Math.floor(n%60)).padStart(2,'0')}`:'0:00';
function list(){ $('tracks').replaceChildren(...tracks.map((t,i)=>{const li=document.createElement('li'),b=document.createElement('button'),num=document.createElement('span'),name=document.createElement('span');num.className='num';num.textContent=String(t.track).padStart(2,'0');name.textContent=t.title;b.append(num,name);b.setAttribute('aria-current',String(i===index));b.onclick=()=>{bag=[];history=[];load(i,true);};li.append(b);return li;}));}
async function play(){const g=generation;try{await audio.play();if(g===generation)$('status').textContent='';}catch(e){if(g===generation&&e.name!=='AbortError')$('status').textContent=e.name==='NotAllowedError'?'Press play to listen.':'Unable to play. Please try again.';}}
function load(i,start=false){generation++;index=(i+tracks.length)%tracks.length;const t=tracks[index];audio.src=t.url;$('title').textContent=t.title;$('artist').textContent=t.artist;$('art').src=t.cover;$('duration').textContent=time(t.duration);$('elapsed').textContent='0:00';$('seek').value=0;list();positionPanel();if(start)play();}
$('play').onclick=()=>audio.paused?play():audio.pause();$('prev').onclick=()=>load(shuffle&&history.length?history.pop():index-1,true);$('next').onclick=()=>advance();
audio.onplay=()=>{icon('play','pause');$('play').setAttribute('aria-label','Pause');$('play').title='Pause';};audio.onpause=()=>{icon('play','play');$('play').setAttribute('aria-label','Play');$('play').title='Play';};audio.onended=()=>repeat==='one'?load(index,true):advance();audio.onerror=()=>{$('status').textContent='Unable to load this track. Try the next one.';};
audio.ontimeupdate=()=>{$('elapsed').textContent=time(audio.currentTime);if(Number.isFinite(audio.duration)&&audio.duration>0)$('seek').value=audio.currentTime/audio.duration*1000;};
$('seek').oninput=()=>{if(Number.isFinite(audio.duration))audio.currentTime=Number($('seek').value)/1000*audio.duration;};audio.volume=.25;$('volume').oninput=()=>audio.volume=Number($('volume').value);
$('loop').onclick=()=>{repeat=repeat==='all'?'one':'all';$('loop').dataset.mode=repeat;const label=repeat==='all'?'Repeat all':'Repeat one';$('loop').setAttribute('aria-label',label);$('loop').title=label;};
function panel(open){$('panel').hidden=!open;$('list').setAttribute('aria-expanded',String(open));positionPanel();} $('list').onclick=()=>panel($('panel').hidden);$('close').onclick=()=>{panel(false);$('list').focus();};document.addEventListener('keydown',e=>{if(e.key==='Escape')panel(false);});
$('album').onchange=()=>{const playing=!audio.paused;bag=[];history=[];tracks=all.filter(t=>t.album===$('album').value);load(0,playing);};
fetch('/juju-radar/music-v1/playlist.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{all=data;for(const artist of [...new Set(all.map(t=>t.artist))]){const group=document.createElement('optgroup');group.label=artist;for(const name of [...new Set(all.filter(t=>t.artist===artist).map(t=>t.album))]){const o=document.createElement('option');o.value=o.textContent=name;group.append(o);}$('album').append(group);}$('album').value='Misty for Direct Cutting';tracks=all.filter(t=>t.album===$('album').value);load(0,true);}).catch(()=>{$('title').textContent='Playlist unavailable';$('status').textContent='Please refresh the page.';});

$("site").addEventListener("load",()=>{try{const d=$("site").contentDocument;const style=d.createElement("style");style.textContent="body{padding-bottom:180px}";d.head.append(style);}catch(e){}});

function shuffledNext(){
 if(tracks.length<2)return index;
 if(!bag.length){bag=tracks.map((_,i)=>i).filter(i=>i!==index);for(let i=bag.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[bag[i],bag[j]]=[bag[j],bag[i]];}}
 return bag.pop();
}
function advance(){if(!tracks.length)return;history.push(index);if(history.length>100)history.shift();load(shuffle?shuffledNext():index+1,true);}
$('shuffle').onclick=()=>{shuffle=!shuffle;bag=[];history=[];$('shuffle').setAttribute('aria-pressed',String(shuffle));$('shuffle').title=shuffle?'Shuffle on':'Shuffle off';};
const widget=document.querySelector('.player');let fraction=1,dragging=null,folded=false;
try{const saved=JSON.parse(localStorage.getItem('jazz-widget')||'null');if(saved){fraction=Number.isFinite(saved.y)?Math.min(1,Math.max(0,saved.y)):1;folded=!!saved.folded;}}catch(e){}
function saveWidget(){try{localStorage.setItem('jazz-widget',JSON.stringify({y:fraction,folded}));}catch(e){}}
function positionPanel(){
 if($('panel').hidden)return;
 const rect=widget.getBoundingClientRect(),p=$('panel');
 p.style.bottom='auto';p.style.maxHeight=Math.max(100,innerHeight-28)+'px';
 const height=p.getBoundingClientRect().height;
 const above=rect.top-height-12,below=rect.bottom+12;
 p.style.top=Math.max(14,Math.min(innerHeight-height-14,above>=14?above:below))+'px';
}
function positionWidget(){const max=Math.max(14,innerHeight-widget.offsetHeight-14);widget.style.bottom='auto';widget.style.top=(14+fraction*(max-14))+'px';positionPanel();}
function setFolded(value){folded=value;widget.classList.toggle('folded',folded);icon('fold',folded?'expand':'fold');$('fold').setAttribute('aria-label',folded?'Expand player':'Collapse player');$('fold').title=folded?'Expand':'Collapse';$('fold').setAttribute('aria-expanded',String(!folded));if(folded)panel(false);positionWidget();saveWidget();}
$('fold').onclick=()=>setFolded(!folded);
$('drag').onpointerdown=e=>{if(e.button!==0)return;panel(false);dragging={start:e.clientY,top:widget.getBoundingClientRect().top};$('drag').setPointerCapture(e.pointerId);document.body.classList.add('dragging');e.preventDefault();};
$('drag').onpointermove=e=>{if(!dragging)return;const max=Math.max(14,innerHeight-widget.offsetHeight-14),top=Math.max(14,Math.min(max,dragging.top+e.clientY-dragging.start));fraction=max>14?(top-14)/(max-14):0;positionWidget();};
function endDrag(){if(!dragging)return;dragging=null;document.body.classList.remove('dragging');saveWidget();}
$('drag').onpointerup=endDrag;$('drag').onpointercancel=endDrag;$('drag').onlostpointercapture=endDrag;
$('drag').onkeydown=e=>{if(!['ArrowUp','ArrowDown','Home','End'].includes(e.key))return;e.preventDefault();const span=Math.max(1,innerHeight-widget.offsetHeight-28);fraction=e.key==='Home'?0:e.key==='End'?1:Math.max(0,Math.min(1,fraction+(e.key==='ArrowUp'?-1:1)*(e.shiftKey?80:24)/span));positionWidget();saveWidget();};
window.addEventListener('resize',positionWidget);new ResizeObserver(positionWidget).observe(widget);setFolded(folded);

const opticalSurfaces=[widget,$('panel')].map(el=>({el,glass:liquidGlass(el,{scale:-112,chroma:4,border:.075,mapBlur:8,blur:1.8,saturate:1.3,fallbackBlur:18})}));
for(const {el,glass} of opticalSurfaces){el.dataset.refraction=glass.supported?'svg':'fallback';el.addEventListener('pointermove',e=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;const r=el.getBoundingClientRect();el.style.setProperty('--light-x',((e.clientX-r.left)/r.width*100)+'%');el.style.setProperty('--light-y',((e.clientY-r.top)/r.height*100)+'%');});el.addEventListener('pointerleave',()=>{el.style.removeProperty('--light-x');el.style.removeProperty('--light-y');});}

})();
