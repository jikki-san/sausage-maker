import unittest

from block_markdown import BlockType, block_to_block_type, extract_title, markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = """
This is **just** one line
"""
        expected = ["This is **just** one line"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_single_multiline_block(self):
        md = """
This is a paragraph
This is another paragraph
"""
        expected = ["This is a paragraph\nThis is another paragraph"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_empty(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_markdown_to_blocks_excess_newline(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trailing_newlines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_all_newlines(self):
        md = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_block_to_block_type_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_false_heading(self):
        block = "####### Not actually a heading; I have too many hashes..."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```
            func main() {
                fmt.Println("I am Go code!")
            }
        ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> You miss 100% of the shots you don't take. -Wayne Gretzky -Michael Scott"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "Nothing special about this one"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_extract_title(self):
        md = """
# Title

- This is a list
- with items
"""
        expected = "Title"
        self.assertEqual(extract_title(md), expected)


if __name__ == "__main__":
    unittest.main()
