#!/usr/bin/env python3
"""Build a dependency-free public archive. Only explicitly approved content can deploy."""
import argparse, hashlib, html, json, re, shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]; SITE=ROOT/'site'; BASE='https://www.asteronline.cn/juju-radar/'; PREFIX='/juju-radar/'
E=lambda x:html.escape(str(x),quote=True)
FILES=['article.md','issue.json','sources.json','zotero-papers.json']
def digest(folder):
 # Delivery metadata can change without editorial changes. Hash only public editorial fields.
 parts=[]
 for name in FILES:
  p=folder/name
  if p.exists():
   d=p.read_text()
   if name=='issue.json':d=json.dumps(json.loads(d).get('sources',[]),ensure_ascii=False,sort_keys=True)
   if name=='sources.json':d=json.dumps(json.loads(d).get('sources',[]),ensure_ascii=False,sort_keys=True)
   parts.append(name+'\n'+d)
 return hashlib.sha256('\n'.join(parts).encode()).hexdigest()
def plain(s):
 s=re.sub(r'\[([^\]]+)\]\([^\)]+\)',r'\1',s)
 s=re.sub(r'<!--.*?-->','',s,flags=re.S)
 return re.sub(r'[*#>`]','',s).strip()
def inline(s):
 tokens=[]
 def link(m):
  u=html.unescape(m[2]); label=E(m[1]); val=f'<a href="{E(u)}" target="_blank" rel="noopener noreferrer">{label}</a>' if u.startswith(('https://','http://')) else label
  tokens.append(val);return f'LINKTOKEN{len(tokens)-1}END'
 s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',link,s)
 s=E(s);s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s);s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
 for i,t in enumerate(tokens):s=s.replace(f'LINKTOKEN{i}END',t)
 return s

def md(s):
 s=re.sub(r'^---\n.*?\n---\n','',s,flags=re.S);s=re.sub(r'<!--.*?-->','',s,flags=re.S)
 out=[]
 for block in re.split(r'\n\s*\n',s.strip()):
  if not block.strip():continue
  if block.startswith('#'):
   lines=block.split('\n');m=re.match(r'(#{1,6})\s+(.*)',lines[0])
   if m:out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>');out.extend('<p>'+inline(x)+'</p>' for x in lines[1:] if x);continue
  if block.startswith('>'):out.append('<blockquote>'+md(re.sub(r'^> ?', '',block,flags=re.M))+'</blockquote>');continue
  if all(re.match(r'^(?:[-*]|\d+\.)\s',x) for x in block.splitlines()):out.append('<ul>'+''.join('<li>'+inline(re.sub(r'^(?:[-*]|\d+\.)\s','',x))+'</li>' for x in block.splitlines())+'</ul>');continue
  if block.strip()=='---':out.append('<hr>');continue
  out.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
 return '\n'.join(out)
def paragraphs(text):
 return [plain(x) for x in text.split('\n\n') if len(plain(x))>45 and not x.lstrip().startswith(('#','>','['))]
def topics(text):
 patterns={'Agent':['agent','astra','终端','客服'],'机器人':['机器人','具身'],'视觉与多模态':['视频','视觉','图像','设计','worldsculpt','3d'],'AI 科研':['science','生物','衰老','数学','科研','navier','费马'],'算力与推理':['推理','缓存','kv','芯片','算力','diffusion'],'开源与训练':['训练','开源','distillation','compile'],'产业与安全':['战略','收购','事故','安全','越界','司法','监控']}
 result=[k for k,vs in patterns.items() if any(v.lower() in text.lower() for v in vs)]
 return result or ['其他']
def slug(x):return hashlib.sha256(x.encode()).hexdigest()[:16]
def jsonwrite(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2).replace('https://happy.asteronline.cn','https://www.asteronline.cn')+'\n')
def ris(p):
 def f(k,v):return k+'  - '+' '.join(str(v).splitlines())+'\n' if v else ''
 s=f('TY',{'report':'RPRT','journalArticle':'JOUR'}.get(p.get('item_type'),'UNPB'))+f('TI',p['title'])+f('UR',p['url'])+f('DO',p.get('doi'))+f('DA',p.get('published_date'))+f('JO',p.get('publicationTitle'))
 for a in p.get('authors',[]):s+=f('AU',a)
 for t in p.get('tags',[]):s+=f('KW',t)
 return s+f('N1',p['note'])+'ER  -\n'
ARROW='<svg class="arrow" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 10h13m-5-5 5 5-5 5"/></svg>'
def build(preview=False):
 registration=json.loads((SITE/'registration.json').read_text())
 paper_summaries=json.loads((SITE/'paper-summaries.json').read_text())
 registration_html='<div class="registration">'+''.join('<a href="'+E(registration[k+'_url'])+'" target="_blank" rel="noopener noreferrer">'+E(registration[k+'_number'])+'</a>' for k in ['icp','police'])+'</div>'
 approvals=json.loads((SITE/'publications.json').read_text())
 folders=[ROOT/'issues'/d for d in sorted(approvals['issues'])]
 if preview:
  folders=sorted(p for p in (ROOT/'issues').iterdir() if re.fullmatch(r'\d{4}-\d{2}-\d{2}',p.name) and (p/'article.md').exists())
 for p in folders:
  if not preview and approvals['issues'][p.name]['sha256']!=digest(p):raise ValueError('Content changed since approval: '+p.name)
 out=SITE/('preview' if preview else 'dist');out.mkdir(exist_ok=True)
 for old in out.iterdir():
  if old.is_dir():shutil.rmtree(old)
  else:old.unlink()
 css=(SITE/'assets/site.css').read_bytes();js=(SITE/'assets/site.js').read_bytes();cv=hashlib.sha256(css).hexdigest()[:10];jv=hashlib.sha256(js).hexdigest()[:10]
 (out/'assets').mkdir();(out/f'assets/site-{cv}.css').write_bytes(css);(out/f'assets/site-{jv}.js').write_bytes(js)
 music_source=SITE/'assets/music'
 music_names=['bootstrap.js','player.js','liquid-glass.js','music.css','shell.html']
 music_version=hashlib.sha256(b''.join((music_source/n).read_bytes() for n in music_names)).hexdigest()[:10]
 music_dest=out/'assets'/('music-'+music_version);music_dest.mkdir()
 for name in music_names:shutil.copyfile(music_source/name,music_dest/name)
 def shell(title,body,canonical='',script=''):
  return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Juju Radar</title><meta name="description" content="每日 AI 动态、论文和开源项目，附中文解读与原始链接。"><link rel="icon" href="data:,"><link rel="canonical" href="{BASE+canonical}"><link rel="stylesheet" href="{PREFIX}assets/site-{cv}.css"><link rel="alternate" type="application/rss+xml" title="Juju Radar 每日精选" href="{BASE}feed.xml"><link rel="alternate" type="application/rss+xml" title="Juju Radar 论文" href="{BASE}papers.xml"></head><body><div class="wrap"><header><a class="brand" href="{PREFIX}">Juju Radar</a><nav aria-label="主导航"><a data-view="daily" href="{PREFIX}">精选</a><a data-view="library" href="{PREFIX}papers/">论文库</a><a href="{PREFIX}archive/">往期</a><a href="{PREFIX}subscribe/">订阅</a></nav></header>{body}<footer><div class="footer-main"><span>内容由 AI 辅助整理 · 原始来源见各条链接</span><a href="{PREFIX}subscribe/">RSS 与文献导出</a></div>{registration_html}</footer></div>{script}<script src="{PREFIX}assets/music-{music_version}/bootstrap.js" defer></script></body></html>'''
 def save(path,text):
  p=out/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.replace('https://happy.asteronline.cn','https://www.asteronline.cn'))
 issues=[];entries=[];papers={};projects={}
 for folder in folders:
  date=folder.name;article=(folder/'article.md').read_text();info=json.loads((folder/'issue.json').read_text());sources=json.loads((folder/'sources.json').read_text())['sources']
  front=dict(re.findall(r'^(title|summary):\s*(.+)$',article,re.M));title=front['title'];desc=front.get('summary','')
  issues.append({'date':date,'title':title,'summary':desc,'path':PREFIX+'read/'+date+'/','sources_url':BASE+date+'/'})
  sections=re.split(r'^##\s+',article,flags=re.M)[1:]
  for n,section in enumerate(sections):
   heading,_,body=section.partition('\n'); heading=heading.strip()
   if not re.search(r'\d(?:\.\d)?/10',body[:180]):continue
   heading=re.sub(r'^[^\w\u4e00-\u9fff]+','',heading)
   urls=re.findall(r'\]\((https?://[^)]+)\)',body)
   source=next((s for s in info['sources'] if s.get('url') in urls),info['sources'][min(n,len(info['sources'])-1)])
   ps=paragraphs(body);summary=plain(re.sub(r'\[[^\]]+\]\(https?://[^)]+\)', '', next((b for b in body.split('\n\n') if len(plain(b))>45 and not b.lstrip().startswith(('#','>','['))), source.get('reason',''))))
   category=source.get('category','AI 进展');path='notes/'+date+'-'+str(n+1)+'/'
   e={'id':date+'-'+str(n+1),'type':'news','date':date,'dates':[date],'title':heading,'category':category,'topics':topics(category+' '+heading),'summary':summary,'note':plain(body),'url':urls[0] if urls else source['url'],'path':PREFIX+path,'backfill':'补看' in str(source.get('window_status','')), 'related_urls':urls}
   entries.append(e)
   save(path+'index.html',shell(heading,f'<main class="reading"><a class="back" href="{PREFIX}read/{date}/">返回 {date} 完整精选</a><h1>{E(heading)}</h1><div class="meta">{date} 收录 · {E(category)}</div>{md(body)}<div class="actions"><a href="{BASE+date}/">本期全部原始资料 {ARROW}</a></div></main>',path))
  text=article.split('## 原始资料')[0]
  text=re.sub(r'^---\n.*?\n---\n','',text,flags=re.S)
  save('read/'+date+'/index.html',shell(title,f'<main class="reading"><a class="back" href="{PREFIX}archive/">全部往期</a>{md(text)}<div class="actions"><a href="{BASE+date}/">本期全部原始资料 {ARROW}</a><a href="{PREFIX}?date={date}">本期精选列表</a></div></main>','read/'+date+'/'))
  if (folder/'zotero-papers.json').exists():
   for p in json.loads((folder/'zotero-papers.json').read_text())['papers']:
    if p.get('evidence_status')!='primary_verified':continue
    ident=(p.get('doi') or p['id']).lower()
    if ident in papers:papers[ident]['dates'].append(date);continue
    papers[ident]={**p,'dates':[date],'date':date}
  for s in sources:
   u=s['url'];m=re.match(r'https://github.com/([^/]+/[^/#?]+)',u)
   if not m:continue
   u='https://github.com/'+m[1].removesuffix('.git');ident=u.lower()
   if ident in projects:projects[ident]['dates'].append(date);continue
   parent=next((e for e in entries if e['date']==date and any(u in v for v in e.get('related_urls',[]))),None)
   projects[ident]={'id':ident,'type':'project','title':m[1],'url':u,'date':date,'dates':[date],'category':'开源项目','topics':topics(s.get('section','')+' '+(parent or {}).get('category','')),'summary':(parent or {}).get('summary','本期资料：'+s.get('section',s['label'])),'note':(parent or {}).get('note',s.get('section',s['label'])),'path':PREFIX+'projects/'+slug(ident)+'/'}
 allris=[]
 for ident,p in papers.items():
  path='papers/'+slug(ident)+'/'
  presentation=paper_summaries.get(ident)
  if not presentation:raise ValueError('Missing Chinese paper title and summary: '+ident)
  summary=presentation['summary']
  e={'id':ident,'type':'paper','title':p['title'],'title_zh':presentation['title_zh'],'date':p['date'],'dates':p['dates'],'url':p['url'],'category':'论文 / '+next((t for t in p.get('tags',[]) if t not in ['待阅读','补看','Juju Radar']),'研究'),'topics':topics(' '.join(p.get('tags',[]))+' '+p['title']),'summary':summary,'note':p['note'],'path':PREFIX+path,'authors':p.get('authors',[]),'backfill':'补看' in p.get('tags',[])}
  entries.append(e);pr=ris(p);allris.append(pr);save(path+'citation.ris',pr)
  note='\n\n'.join(re.sub(r'(https?://\S+)',lambda m:'['+m[1]+']('+m[1]+')',b) for b in p['note'].split('\n\n'))
  author='；'.join(p.get('authors',[]))
  body=f'<main class="reading"><a class="back" href="{PREFIX}papers/">论文库</a><h1>{E(presentation["title_zh"])}</h1><p class="paper-original">{E(p["title"])}</p><p class="lead">{E(summary)}</p><p class="meta">首次公开：{E(p.get("published_date","日期待补"))} · 收录：{E("、".join(p["dates"]))}</p>'+(f'<details><summary>作者</summary><p class="meta">{E(author)}</p></details>' if author else '')+f'<div class="actions"><a href="{E(p["url"])}" target="_blank" rel="noopener noreferrer">论文原文 {ARROW}</a>'+(f'<a href="{E(p["pdf_url"])}" target="_blank" rel="noopener noreferrer">PDF {ARROW}</a>' if p.get('pdf_url') else '')+f'<a href="{PREFIX+path}citation.ris" download>导入 Zotero（RIS）</a></div><h2>阅读笔记</h2>{md(note)}<p class="notice">笔记记录收录当期的判断。阅读一手材料不等于独立复现；后续进展请以原始来源为准。</p></main>'
  related=' · '.join(f'<a href="{PREFIX}read/{d}/">{d} 精选</a>' for d in p['dates'])
  body=body.replace('<h2>阅读笔记</h2>','<p class="paper-issues">相关期次：'+related+'</p><h2>阅读笔记</h2>')
  save(path+'index.html',shell(presentation['title_zh'],body,path))
 for e in projects.values():
  path=e['path'].removeprefix(PREFIX)
  save(path+'index.html',shell(e['title'],f'<main class="reading"><a class="back" href="{PREFIX}read/{e["date"]}/">对应文章</a><h1>{E(e["title"])}</h1><p class="meta">收录：{E("、".join(e["dates"]))}</p><p class="lead">{E(e["summary"])}</p><div class="actions"><a href="{E(e["url"])}" target="_blank" rel="noopener noreferrer">GitHub 仓库 {ARROW}</a><a href="{PREFIX}read/{e["date"]}/">查看本期文章</a></div><p class="notice">仓库状态可能随时间变化，开放范围与使用条件请查看项目自身的许可证和说明。</p></main>',path))
 issues.sort(key=lambda x:x['date'],reverse=True);entries.sort(key=lambda x:x['date'],reverse=True);latest=issues[0]['date'];catalog={'latest':latest,'issues':issues,'entries':entries}
 jsonwrite(out/'catalog.json',catalog);save('papers.ris','\n'.join(allris))
 dates=''.join(f'<li><a data-date="{i["date"]}" href="{PREFIX}?date={i["date"]}">{i["date"].replace("-",".")}{"（本期）" if i["date"]==latest else ""}</a></li>' for i in issues)
 sidebar=f'<aside class="sidebar"><section><h2>往期内容</h2><ul class="dates">{dates}</ul><a href="{PREFIX}archive/">查看全部 {ARROW}</a></section><section><h2>订阅与下载</h2><a class="sub-link" href="{PREFIX}subscribe/#daily">每日精选 RSS<small>每天一份，含完整精选内容</small></a><a class="sub-link" href="{PREFIX}subscribe/#papers">论文 RSS<small>每篇论文与中文阅读笔记</small></a><a class="sub-link" href="{PREFIX}papers.ris" download>导出 Zotero 文献<small>全库 {len(papers)} 篇 · RIS 格式</small></a></section></aside>'
 cards=''.join(f'<article class="entry"><div class="meta">{E(e["category"])} · {e["date"]} 收录</div><h2><a href="{e["path"]}">{E(e["title"])}</a></h2><p>{E(e["summary"])}</p><div class="links"><a href="{e["path"]}">阅读笔记 {ARROW}</a><a href="{E(e["url"])}" target="_blank" rel="noopener noreferrer">原始资料 {ARROW}</a></div></article>' for e in entries if e['type']=='news' and e['date']==latest)
 topicopts=''.join(f'<option>{E(t)}</option>' for t in sorted(set(t for e in entries for t in e['topics'])))
 body=f'<main><h1>AI 精选</h1><p class="intro">每日 AI 动态、论文和开源项目，附中文解读与原始链接。</p><div class="meta">{latest.replace("-",".")} 更新 · {len(issues)} 期归档 · {len(papers)} 篇论文</div><div class="filters" role="search"><div class="search"><label class="sr-only" for="query">搜索资料</label><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg><input id="query" type="search" placeholder="搜索精选内容、关键词…" autocomplete="off"></div><label class="sr-only" for="type">类型</label><select id="type"><option value="">精选</option></select><label class="sr-only" for="topic">主题</label><select id="topic"><option value="">全部主题</option>{topicopts}</select></div><div class="layout"><section aria-label="精选资料"><div class="section-head"><h2 class="section-title" id="results-title">最新精选</h2><p class="meta" id="result-count" role="status" aria-live="polite">{latest}</p></div><div id="results">{cards}</div></section>{sidebar}</div></main>'
 script='<script id="catalog-data" type="application/json">'+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+'</script>'+f'<script src="{PREFIX}assets/site-{jv}.js" defer></script>'
 save('index.html',shell('AI 精选与论文资料库',body,script=script))
 paper_cards=''.join(f'<article class="entry"><div class="meta">{E(e["category"])} · {e["date"]} 收录</div><h2><a href="{e["path"]}">{E(e["title_zh"])}</a></h2><p class="paper-original">{E(e["title"])}</p><p>{E(e["summary"])}</p><div class="links"><a href="{e["path"]}">阅读笔记 {ARROW}</a><a href="{E(e["url"])}" target="_blank" rel="noopener noreferrer">论文原文 {ARROW}</a></div><div class="paper-issues meta">相关期次：'+ ' · '.join(f'<a href="{PREFIX}read/{d}/">{d}</a>' for d in e['dates'])+'</div></article>' for e in entries if e['type']=='paper')
 library_body=body.replace('<h1>AI 精选</h1>','<h1>论文库</h1>').replace('每日 AI 动态、论文和开源项目，附中文解读与原始链接。','按研究主题查找论文，阅读方法与局限，查看原文或导入 Zotero。').replace('搜索精选内容、关键词…','搜索论文题目、作者、关键词…').replace('id="results-title">最新精选','id="results-title">全部论文').replace(cards,paper_cards).replace('<option value="">精选</option>','<option value="">论文</option>')
 save('papers/index.html',shell('论文库',library_body,'papers/',script=script))
 archive_groups=[]
 for issue in issues:
  daily=[e for e in entries if e['type']=='news' and issue['date'] in e['dates']]
  rows=''.join(f'<li class="archive-item"><a class="archive-item-title" href="{e["path"]}">{E(e["title"])}</a><div class="meta">{E(e["category"])}{" · 补看" if e.get("backfill") else ""}</div></li>' for e in daily)
  archive_groups.append(f'<section class="archive-group" data-date="{issue["date"]}"><div class="archive-heading"><h2>{issue["date"]}</h2><span class="meta">{len(daily)} 条精选</span><a href="{issue["path"]}">阅读整期 {ARROW}</a></div><p class="archive-issue-title">{E(issue["title"])}</p><ol class="archive-items">{rows}</ol></section>')
 save('archive/index.html',shell('往期归档','<main class="reading"><h1>往期归档</h1><p class="lead">按日期查看每条精选，也可以阅读整期文章。</p>'+''.join(archive_groups)+'</main>','archive/'))
 save('subscribe/index.html',shell('订阅与导出',f'<main class="reading"><h1>订阅与下载</h1><p class="lead">支持 RSS 订阅和 Zotero 文献导入。</p><h2 id="daily">每日精选 RSS</h2><p>每期一条，包含完整精选正文。复制下面的地址，在 RSS 阅读器中添加订阅。</p><a class="feed-url" href="{BASE}feed.xml">{BASE}feed.xml</a><h2 id="papers">论文 RSS</h2><p>每篇论文一条，附中文笔记和原始链接。同一论文重复收录时保留同一条订阅标识。</p><a class="feed-url" href="{BASE}papers.xml">{BASE}papers.xml</a><h2>导入 Zotero</h2><p><a href="{PREFIX}papers.ris" download>下载全部 {len(papers)} 篇论文（RIS）</a></p><p>在 Zotero 中选择“文件 → 导入”，打开下载的 RIS 文件。单篇论文页面也提供独立下载；PDF 为原始链接，未打包全文。</p><h2>内容如何更新</h2><p>每天整理一手材料，保留入选理由和证据边界；核验后每天更新。更正沿用原链接。所有日期均区分收录日与原始发布日期。</p></main>','subscribe/'))
 def feed(filename,title,items):
  ET.register_namespace('atom','http://www.w3.org/2005/Atom');root=ET.Element('rss',version='2.0');ch=ET.SubElement(root,'channel')
  for k,v in [('title',title),('link',BASE),('description','Juju Radar 中文精选与原始资料'),('language','zh-CN')]:ET.SubElement(ch,k).text=v
  ET.SubElement(ch,'{http://www.w3.org/2005/Atom}link',href=BASE+filename,rel='self',type='application/rss+xml')
  for item in items:
   node=ET.SubElement(ch,'item')
   for k in ['title','link','description','pubDate']:ET.SubElement(node,k).text=item[k].replace('https://happy.asteronline.cn','https://www.asteronline.cn')
   ET.SubElement(node,'guid',isPermaLink='true').text=item['link'].replace('https://www.asteronline.cn','https://happy.asteronline.cn')
  ET.ElementTree(root).write(out/filename,encoding='utf-8',xml_declaration=True)
 def pub(date):return format_datetime(datetime.fromisoformat(date).replace(hour=9,tzinfo=timezone(timedelta(hours=8))))
 feed('feed.xml','Juju Radar 每日精选',[{'title':i['title'],'link':BASE+'read/'+i['date']+'/','description':md((ROOT/'issues'/i['date']/'article.md').read_text().split('## 原始资料')[0]),'pubDate':pub(i['date'])} for i in issues])
 feed('papers.xml','Juju Radar 论文',[{'title':p['title'],'link':BASE+'papers/'+slug(ident)+'/','description':md(p['note'])+'<p><a href="'+E(p['url'])+'">论文原文</a></p>','pubDate':pub(p['date'])} for ident,p in sorted(papers.items(),key=lambda kv:kv[1]['date'],reverse=True)])
 urls=['', 'papers/','archive/','subscribe/']+['read/'+i['date']+'/' for i in issues]+[e['path'].removeprefix(PREFIX) for e in entries if e['type']!='news']
 sm=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
 for path in urls:ET.SubElement(ET.SubElement(sm,'url'),'loc').text=BASE+path
 ET.ElementTree(sm).write(out/'sitemap.xml',encoding='utf-8',xml_declaration=True)
 manifest={'mode':'preview' if preview else 'public','issues':{p.name:digest(p) for p in folders},'counts':{'issues':len(issues),'papers':len(papers),'projects':len(projects),'entries':len(entries)},'files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file()}}
 jsonwrite(SITE/('preview-build.json' if preview else 'build-receipt.json'),manifest)
 print(json.dumps({'output':str(out),**manifest['counts']},ensure_ascii=False))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args();build(args.preview)
