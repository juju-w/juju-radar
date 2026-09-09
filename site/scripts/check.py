#!/usr/bin/env python3
"""Validate the explicit public file boundary and generated static site. No matched secrets in logs."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
STATIC={'.gitignore','.public-export-marker','README.md','SECURITY.md','.github/workflows/publish.yml','site/paper-summaries.json','site/publications.json','site/registration.json','site/assets/site.css','site/assets/site.js','site/scripts/build.py','site/scripts/build-source-page.py','site/scripts/check.py','site/scripts/package.py','ops/pull-release.py'}
PATTERNS=[('private key',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),('GitHub credential',r'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'),('cloud access key',r'(?:AKIA|ASIA)[A-Z0-9]{16}|AKID[A-Za-z0-9]{28,}'),('credential URL',r'https?://[^\s/@:]+:[^\s/@]+@'),('credential assignment',r'(?i)(?:api[_-]?key|app[_-]?secret|access[_-]?token|password|secret[_-]?key)\s*[=:]\s*[\"\x27][A-Za-z0-9/+_=-]{12,}'),('local metadata',r'/Users/[A-Za-z0-9_-]+/|/home/[A-Za-z0-9_-]+/')]
def scan(paths):
 bad=[]
 for path in paths:
  rel=path.relative_to(ROOT).as_posix()
  if path.is_symlink():bad.append((rel,'symlink'));continue
  if rel not in STATIC and not re.fullmatch(r'issues/\d{4}-\d{2}-\d{2}/(?:article\.md|issue\.json|sources\.json|zotero-papers\.json)',rel):bad.append((rel,'not in public allowlist'))
  text=path.read_text()
  for label,pattern in PATTERNS:
   # Scanner code contains detector literals, not actual deployment information.
   if rel=='site/scripts/check.py' and label=='local metadata':continue
   if re.search(pattern,text):bad.append((rel,label))
 if bad:
  for rel,label in bad:print(rel+': '+label,file=sys.stderr)
  raise SystemExit('Public boundary scan failed (values redacted)')
def sources():
 result=[]
 for p in ROOT.rglob('*'):
  if not p.is_file():continue
  rel=p.relative_to(ROOT)
  if '.git' in rel.parts or '__pycache__' in rel.parts or rel.parts[0] in ['public','release'] or str(rel).startswith(('site/dist/','site/preview/')) or p.suffix=='.pyc' or p.name.startswith('.scan-') or p.name in ['build-receipt.json','preview-build.json']:continue
  result.append(p)
 return result
class Links(HTMLParser):
 def __init__(self,root):super().__init__();self.root=root
 def handle_starttag(self,t,attrs):
  for k,v in attrs:
   if k in ['href','src'] and v.startswith('/juju-radar/'):
    path=v.removeprefix('/juju-radar/').split('?')[0].split('#')[0]
    if not path or path.endswith('/'):path+='index.html'
    assert (self.root/path).is_file(),'Missing link '+path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source-only',action='store_true');a=ap.parse_args()
 scan(sources())
 if not a.source_only:
  dist=ROOT/'site/dist';data=json.loads((dist/'catalog.json').read_text());paper_count=sum(e['type']=='paper' for e in data['entries'])
  for p in dist.rglob('*.html'):Links(dist).feed(p.read_text());assert '粤ICP备2025379346号-1' in p.read_text()
  for name,count in [('feed.xml',len(data['issues'])),('papers.xml',paper_count)]:
   items=ET.parse(dist/name).findall('./channel/item');assert len(items)==count;assert len({i.findtext('guid') for i in items})==count
  assert (dist/'papers.ris').read_text().count('ER  -')==paper_count
  assert not any(e['type']=='project' for e in data['entries'])
  library=(dist/'papers/index.html').read_text()
  for e in data['entries']:
   if e['type']=='paper':
    assert e['title_zh'] and e['summary']
    assert 'href="'+e['path']+'"' in library
  archive=(dist/'archive/index.html').read_text()
  for e in data['entries']:
   if e['type']=='news':assert 'href="'+e['path']+'"' in archive,'Archive omits selected item '+e['id']
 print('Public file allowlist and '+('source' if a.source_only else 'site')+' checks passed')
if __name__=='__main__':main()
