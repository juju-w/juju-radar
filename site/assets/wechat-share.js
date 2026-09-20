/* Only the top-level WeChat page owns JS-SDK configuration. */
(() => {
 if(window!==window.top||!/MicroMessenger/i.test(navigator.userAgent))return;
 let sdkReady=false, desired, configured=false, lastDocument;
 const entryUrl=location.href.split('#')[0];
 const ios=/iPhone|iPad|iPod/i.test(navigator.userAgent);
 let signingUrl='',signGeneration=0,sdkLoaded;
 const origin='https://www.asteronline.cn';
 const currentDocument=()=>document.querySelector('#site')?.contentDocument||document;
 const meta=(doc,key)=>doc.querySelector(`meta[property="${key}"]`)?.content||'';
 function apply(){
  if(!sdkReady||!desired)return;
  const data={...desired};configured=false;let friend=false,timeline=false;
  const success=()=>{if(desired.link===data.link)configured=friend&&timeline;};
  wx.updateAppMessageShareData({...data,success:()=>{friend=true;success();},fail:()=>{configured=false;}});
  wx.updateTimelineShareData({title:data.title,link:data.link,imgUrl:data.imgUrl,success:()=>{timeline=true;success();},fail:()=>{configured=false;}});
 }
 function sync(){
  if(document.querySelector('#site')?.hidden)return;
  const doc=currentDocument();if(!doc||doc===lastDocument)return;
  lastDocument=doc;
  const link=doc.querySelector('link[rel="canonical"]')?.href;
  if(!link?.startsWith(origin+'/juju-radar/'))return;
  desired={title:meta(doc,'og:title')||doc.title,desc:(meta(doc,'og:description')||'').slice(0,120),link,imgUrl:origin+'/juju-radar/assets/wechat-cover.png?v=8077d64f03'};
  configure();apply();
  if(doc.defaultView.sessionStorage.getItem('juju-wechat-share')===link){doc.defaultView.sessionStorage.removeItem('juju-wechat-share');show(link,desired.title);}
 }
 function show(link,title){
  let dialog=document.querySelector('#wechat-share-help');
  if(!dialog){
   dialog=document.createElement('dialog');dialog.id='wechat-share-help';
   // Inline styles keep this top-level dialog usable with the music shell stylesheet.
   dialog.style.cssText='box-sizing:border-box;width:min(360px,calc(100vw - 32px));padding:24px;border:1px solid #ddd;border-radius:16px;background:white;color:#26332d;font:15px/1.7 system-ui;';
   dialog.setAttribute('aria-labelledby','wechat-share-heading');
   dialog.innerHTML='<h2 id="wechat-share-heading" style="font-size:20px;margin-top:0">分享这篇文章</h2><p data-hint></p><button data-copy style="width:auto;min-width:80px;min-height:44px;white-space:nowrap;padding:8px 12px;border:1px solid #ddd;border-radius:8px;background:white;color:#26332d">复制链接</button><form method="dialog" style="display:inline;margin-left:16px"><button style="width:auto;min-width:80px;min-height:44px;white-space:nowrap;padding:8px 12px;border:1px solid #ddd;border-radius:8px;background:white;color:#26332d">关闭</button></form><textarea readonly aria-label="分享标题和链接" hidden style="box-sizing:border-box;width:100%;margin-top:12px" rows="4"></textarea><p role="status" data-status></p>';
   document.body.append(dialog);
  }
  dialog.querySelector('[data-hint]').textContent=sdkReady&&configured?'点击右上角 ···，发送给朋友或分享到朋友圈。':'可点击右上角 ··· 转发，也可以复制链接；卡片信息尚未确认就绪。';
  const area=dialog.querySelector('textarea');area.hidden=true;area.value=title+'\n'+link;
  dialog.querySelector('[data-status]').textContent='';
  dialog.querySelector('[data-copy]').onclick=async()=>{try{await navigator.clipboard.writeText(area.value);dialog.querySelector('[data-status]').textContent='已复制';}catch{area.hidden=false;area.focus();area.select();}};
  if(!dialog.open)dialog.showModal();
 }
 window.jujuWechatShare={show};
 function configure(){
  const url=ios?entryUrl:location.href.split('#')[0];
  if(!sdkLoaded||url===signingUrl)return;
  signingUrl=url;sdkReady=false;configured=false;
  const generation=++signGeneration,controller=new AbortController();
  const timer=setTimeout(()=>controller.abort(),10000);
  Promise.all([sdkLoaded,fetch('/juju-radar/api/wechat-sign',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url}),signal:controller.signal}).then(r=>{if(!r.ok)throw Error('Unavailable');return r.json();})]).then(([,config])=>{
   if(generation!==signGeneration)return;
   wx.ready(()=>{if(generation===signGeneration){sdkReady=true;apply();}});
   wx.error(()=>{if(generation===signGeneration){sdkReady=false;configured=false;}});
   wx.config({...config,debug:false,jsApiList:['updateAppMessageShareData','updateTimelineShareData']});
  }).catch(()=>{if(generation===signGeneration)signingUrl='';}).finally(()=>clearTimeout(timer));
 }
 // The music shell emits this after mirroring the reading URL to the address bar.
 window.addEventListener('juju:reading-ready',()=>{lastDocument=null;sync();});
 sdkLoaded=new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://res.wx.qq.com/open/js/jweixin-1.6.0.js';s.onload=resolve;s.onerror=reject;document.head.append(s);});
 sync();configure();
})();
