"""Small, escaped Markdown renderer for the archive; no build-time dependencies.

Supports the article syntax we publish, including fenced code and GFM tables.
It intentionally does not accept raw HTML or run embedded code.
"""
import html
import re

FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})([^\n]*)$')
HEADING = re.compile(r'^ {0,3}(#{1,6})\s+(.+?)(?:\s+#+)?\s*$')
LIST = re.compile(r'^ {0,3}(?:([-*+])|(\d+)[.)])\s+(.+)$')


def fence_at(line):
    match = FENCE.match(line)
    if match and not (match[1][0] == '`' and '`' in match[2]):
        return match


def fence_end(lines, start, match):
    closing = re.compile(r'^ {0,3}' + re.escape(match[1][0]) + '{' + str(len(match[1])) + r',}\s*$')
    for index in range(start + 1, len(lines)):
        if closing.match(lines[index]):
            return index
    return len(lines)


def mask_fences(text):
    """Keep offsets/newlines while hiding fenced examples from editorial scanning."""
    lines = text.splitlines(keepends=True)
    index = 0
    while index < len(lines):
        match = fence_at(lines[index].rstrip('\r\n'))
        if match:
            end = fence_end([line.rstrip('\r\n') for line in lines], index, match)
            for offset in range(index, min(end + 1, len(lines))):
                lines[offset] = re.sub(r'[^\r\n]', ' ', lines[offset])
            index = end + 1
        else:
            index += 1
    return ''.join(lines)


def split_sections(text, level=2):
    matches = list(re.finditer(r'^' + '#' * level + r'\s+', mask_fences(text), re.M))
    return [text[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(text)]
            for index, match in enumerate(matches)]


def before_sources(text):
    match = re.search(r'^##\s+原始资料\s*$', mask_fences(text), re.M)
    return text[:match.start()] if match else text


def cells(line):
    """Split table pipes, protecting escaped pipes and backtick spans."""
    line = line.strip()
    result, current, ticks, index = [], [], 0, 0
    while index < len(line):
        char = line[index]
        if char == '\\' and index + 1 < len(line) and line[index + 1] == '|':
            current.append('|')
            index += 2
            continue
        if char == '`':
            end = index + 1
            while end < len(line) and line[end] == '`':
                end += 1
            count = end - index
            if not ticks:
                ticks = count
            elif count == ticks:
                ticks = 0
            current.append(line[index:end])
            index = end
            continue
        if char == '|' and not ticks:
            result.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    result.append(''.join(current).strip())
    if line.startswith('|'):
        result.pop(0)
    if line.endswith('|') and not line.endswith('\\|'):
        result.pop()
    return result


def table_header(lines, index):
    if index + 1 >= len(lines) or '|' not in lines[index]:
        return None
    header, separators = cells(lines[index]), cells(lines[index + 1])
    if not header or len(header) != len(separators):
        return None
    if not all(re.fullmatch(r':?-{3,}:?', cell) for cell in separators):
        return None
    alignment = ['center' if cell.startswith(':') and cell.endswith(':') else
                 'right' if cell.endswith(':') else 'left' for cell in separators]
    return header, alignment


def code_html(code, info, enhanced):
    language = info.strip().split()[0].lower() if info.strip() else 'text'
    if not re.fullmatch(r'[a-z0-9_+-]{1,40}', language):
        language = 'text'
    escaped = html.escape(code, quote=False)
    pre = f'<pre tabindex="0"><code class="language-{language}">{escaped}</code></pre>'
    if not enhanced:
        return ('<p>图示源码（网页版可查看图形）</p>' if language == 'mermaid' else '') + pre
    if language == 'mermaid':
        return ('<figure class="mermaid-block"><figcaption class="code-toolbar">'
                '<span>Mermaid 图示</span><span class="diagram-tools">'
                '<button type="button" class="diagram-expand" hidden>放大查看</button>'
                '<button type="button" class="copy-code" hidden>复制源码</button></span></figcaption>'
                '<p class="diagram-status" role="status">图示加载后显示，也可查看源码。</p>'
                '<div class="diagram-viewport" hidden></div>'
                '<details class="diagram-source" open><summary>查看图示源码</summary>' + pre + '</details></figure>')
    return ('<div class="code-block"><div class="code-toolbar"><span>' + html.escape(language) + '</span>'
            '<button type="button" class="copy-code" hidden>复制代码</button></div>' + pre + '</div>')


def render_markdown(text, inline, title=lambda value: value, enhanced=True):
    text = re.sub(r'\A---\n.*?\n---\n', '', text.replace('\r\n', '\n'), count=1, flags=re.S)
    lines, output, index = text.splitlines(), [], 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        match = fence_at(line)
        if match:
            end = fence_end(lines, index, match)
            code = '\n'.join(lines[index + 1:end])
            if end > index + 1:
                code += '\n'
            output.append(code_html(code, match[2], enhanced))
            index = end + 1
            continue
        if line.lstrip().startswith('<!--') and '-->' not in line:
            while index < len(lines) and '-->' not in lines[index]:
                index += 1
            index += 1
            continue
        match = HEADING.match(line)
        if match:
            level = len(match[1])
            output.append(f'<h{level}>{inline(title(match[2]))}</h{level}>')
            index += 1
            continue
        table = table_header(lines, index)
        if table:
            header, alignment = table
            row = lambda values, tag: '<tr>' + ''.join(
                f'<{tag} class="align-{alignment[col]}"' + (' scope="col"' if tag == 'th' else '') + '>' +
                inline(values[col] if col < len(values) else '') + f'</{tag}>' for col in range(len(header))) + '</tr>'
            rows, index = [], index + 2
            while index < len(lines) and lines[index].strip() and '|' in lines[index] and not fence_at(lines[index]):
                values = cells(lines[index])
                if len(values) > len(header):
                    break  # Keep malformed extra data as prose, rather than silently dropping it.
                rows.append(row(values, 'td'))
                index += 1
            table = '<table><thead>' + row(header, 'th') + '</thead><tbody>' + ''.join(rows) + '</tbody></table>'
            if enhanced:
                table = ('<div class="table-block"><p class="table-hint" hidden>左右滑动查看表格</p>'
                         '<div class="table-scroll" role="region" aria-label="数据表格，可左右滑动" tabindex="0">' + table + '</div></div>')
            output.append(table)
            continue
        if re.match(r'^ {0,3}>', line):
            quoted = []
            while index < len(lines) and re.match(r'^ {0,3}>', lines[index]):
                quoted.append(re.sub(r'^ {0,3}> ?', '', lines[index]))
                index += 1
            output.append('<blockquote>' + render_markdown('\n'.join(quoted), inline, title, enhanced) + '</blockquote>')
            continue
        match = LIST.match(line)
        if match:
            ordered, items = bool(match[2]), []
            start = int(match[2]) if ordered else 1
            while index < len(lines):
                match = LIST.match(lines[index])
                if not match or bool(match[2]) != ordered:
                    break
                items.append('<li>' + inline(match[3]) + '</li>')
                index += 1
            tag = 'ol' if ordered else 'ul'
            output.append('<' + tag + (f' start="{start}"' if ordered and start != 1 else '') + '>' + ''.join(items) + '</' + tag + '>')
            continue
        if re.fullmatch(r' {0,3}(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})', line):
            output.append('<hr>')
            index += 1
            continue
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            if fence_at(lines[index]) or HEADING.match(lines[index]) or LIST.match(lines[index]) or re.match(r'^ {0,3}>', lines[index]) or table_header(lines, index):
                break
            paragraph.append(lines[index])
            index += 1
        rendered = inline('\n'.join(paragraph)).replace('\n', '<br>')
        if rendered.strip():
            output.append('<p>' + rendered + '</p>')
    return '\n'.join(output)
