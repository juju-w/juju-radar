#!/usr/bin/env python3
"""Same-site WeChat JS-SDK signer; secrets never leave the service."""
import hashlib,json,os,re,secrets,threading,time,urllib.parse,urllib.request
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from collections import OrderedDict

ORIGIN='https://www.asteronline.cn'
def validate_url(value):
 if not isinstance(value,str) or len(value)>4096 or any(ord(c)<33 for c in value) or '#' in value:raise ValueError('Invalid URL')
 u=urllib.parse.urlsplit(value)
 if u.scheme!='https' or u.netloc!='www.asteronline.cn' or not u.path.startswith('/juju-radar/'):raise ValueError('Invalid URL')
 decoded=urllib.parse.unquote(u.path)
 if '\\' in decoded or any(x in ['.','..'] for x in decoded.split('/')) or not re.fullmatch(r'/juju-radar/[A-Za-z0-9_./-]*',decoded):raise ValueError('Invalid path')
 return value

def signature(ticket,nonce,timestamp,url):
 return hashlib.sha1(f'jsapi_ticket={ticket}&noncestr={nonce}&timestamp={timestamp}&url={url}'.encode()).hexdigest()

def api(path,payload=None):
 data=json.dumps(payload).encode() if payload else None
 request=urllib.request.Request('https://api.weixin.qq.com/cgi-bin/'+path,data=data,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(request,timeout=10) as r:result=json.load(r)
 if result.get('errcode',0)!=0:raise RuntimeError('WeChat API unavailable')
 return result

class Tickets:
 def __init__(self,credentials,request=api,clock=time.time):
  self.credentials=credentials;self.request=request;self.clock=clock;self.lock=threading.Lock();self.token='';self.ticket='';self.token_until=0;self.ticket_until=0
 def get(self):
  with self.lock:
   now=self.clock()
   if self.ticket and now<self.ticket_until:return self.ticket
   if not self.token or now>=self.token_until:
    r=self.request('stable_token',{'grant_type':'client_credential','appid':self.credentials['appId'],'secret':self.credentials['appSecret'],'force_refresh':False})
    self.token=r['access_token'];self.token_until=now+max(0,r['expires_in']-300)
   try:r=self.request('ticket/getticket?'+urllib.parse.urlencode({'access_token':self.token,'type':'jsapi'}))
   except Exception:
    self.token_until=0
    raise
   self.ticket=r['ticket'];self.ticket_until=now+max(0,r['expires_in']-300)
   return self.ticket

class RateLimit:
 def __init__(self):self.lock=threading.Lock();self.clients=OrderedDict();self.global_window=(0,0)
 def allow(self,ip):
  now=int(time.time()//60)
  with self.lock:
   minute,total=self.global_window
   if minute!=now:total=0
   if total>=300:return False
   minute,count=self.clients.pop(ip,(now,0))
   count=count if minute==now else 0
   self.clients[ip]=(now,count+1)
   while len(self.clients)>2000:self.clients.popitem(last=False)
   self.global_window=(now,total+1)
   return count<30

class Handler(BaseHTTPRequestHandler):
 server_version='JujuSigner';sys_version=''
 def log_message(self,*args):pass
 def reply(self,status,data):
  b=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=='/healthz':return self.reply(200,{'ok':True})
  return self.reply(404,{'error':'not_found'})
 def do_POST(self):
  if self.path!='/juju-radar/api/wechat-sign':return self.reply(404,{'error':'not_found'})
  if self.headers.get('Origin')!=ORIGIN:return self.reply(403,{'error':'origin_rejected'})
  # Proxy overwrites this header; the service is reachable only on the Docker bridge.
  ip=self.headers.get('X-Real-IP',self.client_address[0])
  if not self.server.limiter.allow(ip):return self.reply(429,{'error':'rate_limited'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<=8192:raise ValueError()
   self.connection.settimeout(10)
   body=json.loads(self.rfile.read(length));url=validate_url(body.get('url'))
  except (ValueError,AttributeError,TimeoutError):return self.reply(400,{'error':'invalid_request'})
  try:
   ticket=self.server.tickets.get();timestamp=int(time.time());nonce=secrets.token_hex(16)
   return self.reply(200,{'appId':self.server.tickets.credentials['appId'],'timestamp':timestamp,'nonceStr':nonce,'signature':signature(ticket,nonce,timestamp,url)})
  except Exception:return self.reply(503,{'error':'temporarily_unavailable'})

if __name__=='__main__':
 credentials=json.loads(Path(os.environ['WECHAT_CREDENTIAL_FILE']).read_text())
 server=ThreadingHTTPServer((os.environ.get('WECHAT_BIND','127.0.0.1'),8766),Handler)
 server.tickets=Tickets(credentials);server.limiter=RateLimit();server.serve_forever()
