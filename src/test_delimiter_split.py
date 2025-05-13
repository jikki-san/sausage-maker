import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestDelimiterSplit(unittest.TestCase):
    test1 = TextNode("`This here` was a code block", TextType.NORMAL)
    test2 = TextNode("This is another edge `code block`", TextType.NORMAL)
    test3 = TextNode("This `code block` is simpler", TextType.NORMAL)
    delim = "`"
    new_nodes1 = split_nodes_delimiter([test1], delim, TextType.CODE)
    new_nodes2 = split_nodes_delimiter([test2], delim, TextType.CODE)
    new_nodes3 = split_nodes_delimiter([test3], delim, TextType.CODE)

    def test_single_delimiter(self):
        node = TextNode("This `code block` is simple", TextType.NORMAL)
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" is simple", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_multiple_same_delimiter(self):
        node = TextNode(
            "This `code block` is simple and this `code block` is too", TextType.NORMAL)
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" is simple and this ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" is too", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_multiple_diff_delimiter(self):
        node = TextNode(
            "This `code block` is relevant; this *bold text* is not", TextType.NORMAL)
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" is relevant; this *bold text* is not", TextType.NORMAL)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_beginning_delimiter(self):
        node = TextNode("`This here` was a code block", TextType.NORMAL)
        expected = [
            TextNode("This here", TextType.CODE),
            TextNode(" was a code block", TextType.NORMAL),
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_ending_delimiter(self):
        node = TextNode("This is another edge `code block`", TextType.NORMAL)
        expected = [
            TextNode("This is another edge ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_same_text_type(self):
        node = TextNode("This is already a code block", TextType.CODE)
        expected = [node]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_multi_node_input(self):
        nodes = [
            TextNode("This `code block` is neat", TextType.NORMAL),
            TextNode("This is another code block", TextType.CODE),
            TextNode("This is one last `code block`", TextType.NORMAL),
        ]
        expected = [
            TextNode("This ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" is neat", TextType.NORMAL),
            TextNode("This is another code block", TextType.CODE),
            TextNode("This is one last ", TextType.NORMAL),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "`", TextType.CODE), expected)


if __name__ == "__main__":
    unittest.main()
