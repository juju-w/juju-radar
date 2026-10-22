"""Regression checks for authored examples, safe escaping and source bindings."""
import unittest
from html.parser import HTMLParser
from build import md, inline, source_for_item, ROOT
from markdown_blocks import mask_fences, split_sections, before_sources


class Tags(HTMLParser):
    def __init__(self, value):
        super().__init__()
        self.tags = []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


class MarkdownTests(unittest.TestCase):
    def test_fence_keeps_indentation_blank_lines_and_html_literal(self):
        source = 'if x < 2:\n    print("<script>literal</script>")\n\n## not a heading\n<!-- literal -->\n'
        rendered = md('```python\n' + source + '```\n\n## Real heading')
        self.assertIn('language-python', rendered)
        self.assertIn('    print("&lt;script&gt;literal&lt;/script&gt;")\n\n## not a heading', rendered)
        self.assertIn('&lt;!-- literal --&gt;', rendered)
        self.assertEqual(Tags(rendered).tags.count('h2'), 1)
        self.assertNotIn('script', Tags(rendered).tags)

    def test_tilde_and_unclosed_fences(self):
        self.assertIn('<code class="language-json">', md('~~~json\n{}\n~~~~'))
        self.assertIn('## still code', md('```\n## still code'))
        self.assertNotIn('h2', Tags(md('```\n## still code')).tags)

    def test_long_fence_can_contain_short_fence(self):
        rendered = md('````text\n```js\nconst x = 1;\n```\n````')
        self.assertIn('```js\nconst x = 1;\n```', rendered)
        self.assertEqual(Tags(rendered).tags.count('pre'), 1)

    def test_invalid_language_cannot_inject_attributes(self):
        rendered = md('```python\"onclick=x\nhello\n```')
        self.assertIn('language-text', rendered)
        self.assertNotIn('onclick=', rendered)

    def test_inline_code_is_literal_not_bold_or_link(self):
        rendered = inline('`**literal** [link](https://example.org/) <!-- keep -->`')
        self.assertEqual(rendered, '<code>**literal** [link](https://example.org/) &lt;!-- keep --&gt;</code>')

    def test_inline_html_is_escaped_and_links_still_work(self):
        rendered = inline('<script>alert(1)</script> **粗体** [原文](https://example.org/)')
        self.assertNotIn('script', Tags(rendered).tags)
        self.assertIn('<strong>粗体</strong>', rendered)
        self.assertIn('href="https://example.org/"', rendered)

    def test_table_alignment_escaped_pipe_code_and_link(self):
        rendered = md('| 项目 | 值 | 说明 |\n| :--- | ---: | :---: |\n| A \\| B | 12 | `x|y` 与 [原文](https://example.org/) |')
        self.assertEqual(Tags(rendered).tags.count('table'), 1)
        self.assertEqual(Tags(rendered).tags.count('th'), 3)
        self.assertEqual(Tags(rendered).tags.count('td'), 3)
        self.assertIn('A | B', rendered)
        self.assertIn('<code>x|y</code>', rendered)
        self.assertIn('class="align-right"', rendered)
        self.assertIn('role="region"', rendered)

    def test_incomplete_table_stays_prose(self):
        self.assertNotIn('table', Tags(md('a | b\nnot a delimiter')).tags)
        rendered = md('a | b\n--- | ---\none | two | extra-data')
        self.assertIn('extra-data', rendered)

    def test_mermaid_has_progressive_fallback(self):
        rendered = md('```mermaid\nflowchart LR\n A-->B\n```')
        self.assertIn('class="mermaid-block"', rendered)
        self.assertIn('class="diagram-source" open', rendered)
        self.assertIn('A--&gt;B', rendered)
        self.assertNotIn('script', Tags(rendered).tags)

    def test_feed_has_semantic_tables_and_code_without_controls(self):
        rendered = md('| a | b |\n| --- | --- |\n| 1 | 2 |\n\n```mermaid\nflowchart LR\n A-->B\n```', enhanced=False)
        self.assertIn('table', Tags(rendered).tags)
        self.assertIn('pre', Tags(rendered).tags)
        self.assertNotIn('button', Tags(rendered).tags)
        self.assertNotIn('diagram-viewport', rendered)

    def test_fenced_headings_do_not_change_source_binding(self):
        text = '## Actual\n```markdown\n## Fake\n<!-- source-id: fake -->\n[example](https://example.org/fake)\n```\n\n类别 · 8.5/10\n<!-- source-id: actual -->\n[原文](https://example.org/real)\n## Next\ntext'
        sections = split_sections(text)
        self.assertEqual(len(sections), 2)
        source, url, related = source_for_item('2026-10-22', [{'id':'actual','category':'类别','url':'https://example.org/real'}], 0, 'Actual', sections[0].partition('\n')[2])
        self.assertEqual(source['id'], 'actual')
        self.assertEqual(url, 'https://example.org/real')
        self.assertNotIn('https://example.org/fake', related)
        self.assertEqual(len(mask_fences(text)), len(text))

    def test_sources_heading_inside_code_does_not_truncate_article(self):
        text = '# C#\n\n```text\n## 原始资料\n```\n\nKeep this\n\n## 原始资料\nReal footer'
        self.assertIn('Keep this', before_sources(text))
        self.assertNotIn('Real footer', before_sources(text))
        self.assertIn('<h1>C#</h1>', md(text))

    def test_current_deepinfer_table_preserves_all_values(self):
        article = (ROOT/'issues/2026-10-22-deepinfer/article.md').read_text()
        rendered = md(before_sources(article))
        self.assertEqual(Tags(rendered).tags.count('table'), 1)
        for value in ['4891', '4816', '13730', '14466', '14962', '15961', '−1.5%', '+5.4%', '+6.7%']:
            self.assertIn(value, rendered)


if __name__ == '__main__':
    unittest.main()
