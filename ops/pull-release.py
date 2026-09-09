#!/usr/bin/env python3
"""Pull a public GitHub release without credentials. Install only validated static files."""
import argparse,fcntl,hashlib,json,os,re,shutil,tarfile,tempfile,urllib.request
from pathlib import Path
from datetime import datetime,timezone

def fetch(url,limit=25000000):
 accept='application/octet-stream' if '/releases/assets/' in url else 'application/vnd.github+json' if 'api.github.com/' in url else '*/*'
 req=urllib.request.Request(url,headers={'User-Agent':'Juju-Radar-Static-Updater','Accept':accept})
 with urllib.request.urlopen(req,timeout=45) as r:
  data=r.read(limit+1)
  if len(data)>limit:raise ValueError('Response size limit exceeded')
  return data

def install(repo,root,state_dir):
 if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):raise ValueError('Invalid repository')
 state_dir.mkdir(parents=True,exist_ok=True);root.mkdir(parents=True,exist_ok=True)
 with (state_dir/'lock').open('w') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:return
  release=json.loads(fetch('https://api.github.com/repos/'+repo+'/releases/latest'))
  if release.get('draft') or release.get('prerelease'):raise ValueError('Release is not public stable')
  tag=release['tag_name']
  if not re.fullmatch(r'site-\d+-\d+',tag):raise ValueError('Unexpected release tag')
  current=json.loads((state_dir/'current.json').read_text()) if (state_dir/'current.json').exists() else {}
  if current.get('release_id')==release['id']:print('Unchanged '+tag);return
  if current.get('release_id',0)>release['id']:raise ValueError('Refusing older release')
  assets={a['name']:a['browser_download_url'] for a in release['assets']}
  asset_api={a['name']:a['url'] for a in release['assets']}
  for name in ['site.tar.gz','manifest.json']:
   expected='https://github.com/'+repo+'/releases/download/'+tag+'/'+name
   if assets.get(name)!=expected:raise ValueError('Missing or unexpected release asset')
   if not re.fullmatch(re.escape('https://api.github.com/repos/'+repo+'/releases/assets/')+r'\d+',asset_api.get(name,'')):raise ValueError('Unexpected asset API URL')
  manifest=json.loads(fetch(asset_api['manifest.json'],2000000));commit=manifest['commit']
  if not re.fullmatch(r'[0-9a-f]{40}',commit) or release['target_commitish']!=commit:raise ValueError('Release commit mismatch')
  files=manifest['files']
  if not isinstance(files,dict) or not 1<=len(files)<=5000:raise ValueError('Invalid manifest')
  for name,digest in files.items():
   path=Path(name)
   if path.is_absolute() or '..' in path.parts or any(p.startswith('.') for p in path.parts) or not re.fullmatch(r'[A-Za-z0-9_./-]+',name) or path.suffix not in ['.html','.css','.js','.json','.xml','.ris'] or not re.fullmatch(r'[0-9a-f]{64}',digest):raise ValueError('Unsafe manifest path or digest')
  if not all(p in files for p in ['index.html','feed.xml','papers.xml','catalog.json']):raise ValueError('Incomplete website')
  archive=fetch(asset_api['site.tar.gz'])
  if hashlib.sha256(archive).hexdigest()!=manifest['archive_sha256']:raise ValueError('Archive hash mismatch')
  release_dir=state_dir/'releases'/tag;release_dir.mkdir(parents=True,exist_ok=True)
  with tempfile.TemporaryDirectory(dir=state_dir) as tmp:
   tmp=Path(tmp);bundle=tmp/'site.tar.gz';bundle.write_bytes(archive);unpack=tmp/'unpack';unpack.mkdir()
   with tarfile.open(bundle,'r:gz') as tar:
    members=tar.getmembers()
    if len(members)!=len(files) or {m.name for m in members}!=set(files) or sum(m.size for m in members)>100000000:raise ValueError('Unexpected archive content')
    for m in members:
     if not m.isfile():raise ValueError('Only regular static files accepted')
     data=tar.extractfile(m).read()
     if hashlib.sha256(data).hexdigest()!=files[m.name]:raise ValueError('File hash mismatch')
     path=unpack/m.name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
   # Validate all destination paths before writing. Do not follow existing symlinks.
   for name in files:
    dest=root/name
    if any(p.is_symlink() for p in [dest,*dest.parents] if p==root or root in p.parents):raise ValueError('Symlink in destination')
   # Keep a backup per release. Index last; no downloaded program is executed.
   installed=[]
   try:
    for name in sorted(files,key=lambda p:p=='index.html'):
     dest=root/name;dest.parent.mkdir(parents=True,exist_ok=True);backup=release_dir/'backup'/name
     if dest.exists():backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
     staged=dest.with_name(dest.name+'.uploading');shutil.copy2(unpack/name,staged);os.replace(staged,dest);installed.append(name)
   except Exception:
    for name in reversed(installed):
     backup=release_dir/'backup'/name
     if backup.exists():os.replace(backup,root/name)
     else:(root/name).unlink(missing_ok=True)
    raise
   for name,digest in files.items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:raise ValueError('Post-install verification failed')
  result={'release_id':release['id'],'tag':tag,'commit':commit,'installed_files':len(files),'verified_at':datetime.now(timezone.utc).isoformat()}
  temp=state_dir/'current.json.tmp';temp.write_text(json.dumps(result,indent=2)+'\n');os.replace(temp,state_dir/'current.json');print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--state',type=Path,required=True);a=p.parse_args();install(a.repo,a.root.resolve(),a.state.resolve())
