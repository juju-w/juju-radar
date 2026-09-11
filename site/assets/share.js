/* Share the selected article's permanent URL, including inside the music frame. */
(() => {
 let status, dialog, timer;
 function announce(message) {
  if (!status) {status=document.createElement('div');status.className='share-status';status.setAttribute('role','status');document.body.append(status);}
  status.textContent=message;status.hidden=false;clearTimeout(timer);timer=setTimeout(()=>{status.hidden=true;},2600);
 }
 function manual(text, trigger) {
  if(!dialog){
   dialog=document.createElement('dialog');dialog.className='share-dialog';dialog.setAttribute('aria-labelledby','share-dialog-title');
   dialog.innerHTML='<h2 id="share-dialog-title">复制分享链接</h2><p>请选中下方文字，复制后发送给朋友。</p><textarea aria-label="文章标题和分享链接" readonly rows="4"></textarea><form method="dialog"><button class="share-button">关闭</button></form>';
   document.body.append(dialog);
  }
  dialog.querySelector('textarea').value=text;dialog.onclose=()=>trigger.focus();dialog.showModal();dialog.querySelector('textarea').focus();dialog.querySelector('textarea').select();
 }
 document.addEventListener('click',async event=>{
  const button=event.target.closest('[data-share-url]');if(!button||button.disabled)return;
  const url=new URL(button.dataset.shareUrl);
  if(url.origin!=='https://www.asteronline.cn'||!url.pathname.startsWith('/juju-radar/'))return;
  url.search='';url.hash='';
  const title=button.dataset.shareTitle||document.title;
  const text=title+'\n'+url.href;
  if(/MicroMessenger/i.test(navigator.userAgent)){
   const canonical=document.querySelector('link[rel="canonical"]')?.href;
   if(canonical!==url.href){sessionStorage.setItem('juju-wechat-share',url.href);location.assign(url.pathname);return;}
   if(window.top.jujuWechatShare){window.top.jujuWechatShare.show(url.href,title);return;}
   manual(text,button);return;
  }
  button.disabled=true;
  try{
   if(typeof navigator.share==='function'){
    try{await navigator.share({title,url:url.href});return;}catch(error){if(error.name==='AbortError')return;}
   }
   try{await navigator.clipboard.writeText(text);announce('已复制');}catch{manual(text,button);}
  }finally{button.disabled=false;}
 });
})();
