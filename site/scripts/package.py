#!/usr/bin/env python3
"""Build the site, include dated source pages, validate and package static files only."""
import hashlib,json,subprocess,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];DIST=ROOT/'site/dist'
def run(*args):subprocess.run(args,cwd=ROOT,check=True)
run('python3','site/scripts/check.py','--source-only')
run('python3','site/scripts/build.py')
for date in json.loads((ROOT/'site/publications.json').read_text())['issues']:
 # Run source index builder against a temporary copy so approved input files stay unchanged.
 import tempfile,shutil
 with tempfile.TemporaryDirectory() as t:
  folder=Path(t)/'issues'/date;folder.mkdir(parents=True);(Path(t)/'site').mkdir()
  shutil.copy2(ROOT/'issues'/date/'article.md',folder/'article.md');shutil.copy2(ROOT/'site/registration.json',Path(t)/'site/registration.json')
  shutil.copy2(ROOT/'site/reading-guides.json',Path(t)/'site/reading-guides.json')
  subprocess.run(['python3',str(ROOT/'site/scripts/build-source-page.py'),str(folder)],check=True,stdout=subprocess.DEVNULL)
  (DIST/date).mkdir(exist_ok=True);shutil.copy2(folder/'sources.html',DIST/date/'index.html')
run('python3','site/scripts/check.py')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
files={str(p.relative_to(DIST)):hashlib.sha256(p.read_bytes()).hexdigest() for p in DIST.rglob('*') if p.is_file()}
assert all((Path(p).suffix in ['.html','.css','.js','.json','.xml','.ris'] or p in ['assets/share-cover.png','assets/wechat-cover.png','robots.txt']) for p in files)
release=ROOT/'release';release.mkdir(exist_ok=True)
with tarfile.open(release/'site.tar.gz','w:gz') as tar:
 for name in sorted(files):tar.add(DIST/name,arcname=name,recursive=False)
manifest={'commit':commit,'archive_sha256':hashlib.sha256((release/'site.tar.gz').read_bytes()).hexdigest(),'files':files}
(release/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Packaged',len(files),'static files')
