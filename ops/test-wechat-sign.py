import importlib.util,unittest,hashlib
from pathlib import Path
spec=importlib.util.spec_from_file_location('sign',Path(__file__).with_name('wechat-sign.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_url(self):
  u='https://www.asteronline.cn/juju-radar/read/2026-09-11/?from=timeline&x=%E4%B8%AD'
  self.assertEqual(m.validate_url(u),u)
  for u in ['http://www.asteronline.cn/juju-radar/','https://evil.test/juju-radar/','https://www.asteronline.cn:443/juju-radar/','https://www.asteronline.cn/juju-radar/%2e%2e/','https://www.asteronline.cn/juju-radar/#a','https://www.asteronline.cn/other/']:
   with self.assertRaises(ValueError):m.validate_url(u)
 def test_signature(self):
  self.assertEqual(m.signature('sM4AOVdWfPE4DxkXGEs8VMc8T5V4dB4N4S-pLgZztAOhPN89Sq5OZD','Wm3WZYTPz0wzccnW',1414587457,'http://mp.weixin.qq.com?params=value'),hashlib.sha1(b'jsapi_ticket=sM4AOVdWfPE4DxkXGEs8VMc8T5V4dB4N4S-pLgZztAOhPN89Sq5OZD&noncestr=Wm3WZYTPz0wzccnW&timestamp=1414587457&url=http://mp.weixin.qq.com?params=value').hexdigest())
 def test_cache(self):
  now=[0];calls=[]
  def api(path,payload=None):
   calls.append(path);return {'access_token':'t','ticket':'j','expires_in':7200}
  t=m.Tickets({'appId':'test','appSecret':'test'},api,lambda:now[0]);self.assertEqual(t.get(),'j');t.get();self.assertEqual(len(calls),2);now[0]=6901;t.get();self.assertEqual(len(calls),4)
 def test_rate(self):
  r=m.RateLimit();self.assertTrue(all(r.allow('a') for _ in range(30)));self.assertFalse(r.allow('a'))
unittest.main()
