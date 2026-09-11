#!/usr/bin/env python3
"""Build a small mobile source index from a Juju Radar article."""
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: build-source-page.py ISSUE_DIR")

    folder = Path(sys.argv[1]).resolve()
    article_path = folder / "article.md"
    article = article_path.read_text(encoding="utf-8")
    title_match = re.search(r"^title:\s*(.+)$", article, re.M)
    title = title_match.group(1).strip() if title_match else folder.name

    sources = []
    seen = set()
    current_section = "原始资料"
    for line in article.splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current_section = re.sub(r"^[^\w\u4e00-\u9fff]+\s*", "", heading.group(1)).strip()
        for match in re.finditer(r"\[([^\]]+)\]\((https?://[^)]+)\)", line):
            label, url = match.group(1).strip(), match.group(2).strip()
            if url in seen:
                continue
            seen.add(url)
            sources.append({"label": label, "url": url, "section": current_section})

    if not sources:
        raise SystemExit("No Markdown source links found")

    cards = []
    for index, source in enumerate(sources, 1):
        cards.append(
            '<a class="source" href="{url}" target="_blank" rel="noopener noreferrer">'
            '<span class="index">{index:02d}</span><span class="copy">'
            '<strong>{label}</strong><small>{section}</small><em>{url}</em>'
            '</span><span class="arrow">↗</span></a>'.format(
                index=index,
                label=escape(source["label"]),
                section=escape(source["section"]),
                url=escape(source["url"], quote=True),
            )
        )

    registration_html = ""
    registration_path = folder.parent.parent / "site" / "registration.json"
    if registration_path.exists():
        registration = json.loads(registration_path.read_text())
        registration_html = '<div style="margin-top:18px;line-height:2;text-align:center">' + '<br>'.join(
            '<a style="color:inherit;text-decoration:none" href="' + escape(registration[k + '_url'], quote=True) + '" target="_blank" rel="noopener noreferrer">' + escape(registration[k + '_number']) + '</a>'
            for k in ['icp', 'police']) + '</div>'

    page = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="light">
<title>{title}｜原始资料</title>
<style>
:root{{--ink:#17212b;--muted:#687684;--line:#dfe7ed;--blue:#0f4c81;--wash:#f4f7f9}}
*{{box-sizing:border-box}}html{{background:var(--wash)}}body{{margin:0;color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
main{{width:min(100%,680px);min-height:100vh;margin:0 auto;padding:38px 20px 56px;background:#fff}}
.eyebrow{{margin:0 0 10px;color:var(--blue);font-size:12px;font-weight:700;letter-spacing:.14em}}h1{{margin:0;font-size:26px;line-height:1.35;letter-spacing:-.02em}}
.intro{{margin:14px 0 26px;color:var(--muted);font-size:14px}}.source{{display:flex;gap:13px;align-items:flex-start;margin:0 0 12px;padding:17px 15px;border:1px solid var(--line);border-radius:12px;color:inherit;text-decoration:none;background:#fff}}
.source:active{{background:var(--wash)}}.index{{flex:0 0 30px;color:var(--blue);font-size:12px;font-weight:800;line-height:1.8}}.copy{{min-width:0;flex:1}}strong,small,em{{display:block}}
strong{{font-size:16px;line-height:1.45}}small{{margin-top:3px;color:var(--muted);font-size:12px}}em{{margin-top:7px;overflow:hidden;color:#71808e;font-size:11px;font-style:normal;text-overflow:ellipsis;white-space:nowrap}}
.arrow{{color:var(--blue);font-size:17px;line-height:1.4}}footer{{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}}
</style>
</head>
<body><main>
<p class="eyebrow">JUJU RADAR · SOURCE INDEX</p>
<h1>{title}</h1>
<p class="intro">本页汇总本期引用的官方公告、论文和代码仓库。点击条目即可前往原始页面。</p>
{cards}
<footer>Juju Radar · {date}<br>资料链接以原始发布页面为准。{registration_html}</footer>
</main></body></html>
""".format(title=escape(title), cards="\n".join(cards), date=escape(folder.name[:10] + (' · 特别版' if len(folder.name)>10 else '')), registration_html=registration_html)

    output = folder / "sources.html"
    output.write_text(page, encoding="utf-8")
    manifest = {
        "source_count": len(sources),
        "sources": sources,
        "html_path": str(output),
        "html_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }
    (folder / "sources.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
