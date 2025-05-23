import unittest

from markdown_to_html import markdown_to_htmlnode


class TestMarkdownToHTML(unittest.TestCase):
    def test_empty_block(self):
        md = ""
        expected = "<div></div>"
        node = markdown_to_htmlnode(md)
        self.assertEqual(node.to_html(), expected)

    def test_paragraph_single_block(self):
        md = """
This is **bolded** paragraph
text in a p
tag here
"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        node = markdown_to_htmlnode(md)
        self.assertEqual(node.to_html(), expected)

    def test_paragraph_multiple_blocks(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = "# Heading"
        self.assertEqual(markdown_to_htmlnode(
            md).to_html(), "<div><h1>Heading</h1></div>")
        md = "### Small Heading"
        self.assertEqual(markdown_to_htmlnode(
            md).to_html(), "<div><h3>Small Heading</h3></div>")

    def test_quote_single_line(self):
        md = "> I am a quote."
        node = markdown_to_htmlnode(md)
        expected = "<div><blockquote>I am a quote.</blockquote></div>"
        self.assertEqual(node.to_html(), expected)

    def test_quote_multiline(self):
        md = "> I am a quote\n> that continues across\n> three lines of text."
        node = markdown_to_htmlnode(md)
        expected = "<div><blockquote>I am a quote that continues across three lines of text.</blockquote></div>"
        self.assertEqual(node.to_html(), expected)

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_htmlnode(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = "- This is a list\n- with items"
        node = markdown_to_htmlnode(md)
        expected = "<div><ul><li>This is a list</li><li>with items</li></ul></div>"
        self.assertEqual(node.to_html(), expected)

    def test_ordered_list(self):
        md = "1. This is an ordered list\n2. with items"
        node = markdown_to_htmlnode(md)
        expected = "<div><ol><li>This is an ordered list</li><li>with items</li></ol></div>"
        self.assertEqual(node.to_html(), expected)

    def test_full_document(self):
        md = """
# Heading

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

```
This is text that _should_ remain
the **same** even with inline stuff
```

## Smaller Heading

- This is a list
- with items

1. This is an ordered list
2. with items

> This is a quote
> that spans two lines.

"""
        node = markdown_to_htmlnode(md)
        expected = "<div><h1>Heading</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre><h2>Smaller Heading</h2><ul><li>This is a list</li><li>with items</li></ul><ol><li>This is an ordered list</li><li>with items</li></ol><blockquote>This is a quote that spans two lines.</blockquote></div>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
