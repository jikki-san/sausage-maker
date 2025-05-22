import unittest

from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link
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

    def test_split_image_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in it",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_image_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" after", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode(
            "This is text with no images in it",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no images in it", TextType.NORMAL)],
            new_nodes,
        )

    def test_split_image_duplicate_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_image_neighboring_images(self):
        node = TextNode(
            "This is text with ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) together",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" together", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_image_no_prefix(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) starts the node",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the node", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_image_no_suffix(self):
        node = TextNode(
            "Text with image: ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with image: ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_empty_nodes(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual([], new_nodes)

    def test_split_link_single_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) in it",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in it", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" after", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "This is text with no links in it",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no links in it", TextType.NORMAL)],
            new_nodes,
        )

    def test_split_link_duplicate_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_neighboring_links(self):
        node = TextNode(
            "This is text with [link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png) together",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" together", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_no_prefix(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) starts the node",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the node", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_no_suffix(self):
        node = TextNode(
            "Text with link: [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with link: ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_link_link_only(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_link_empty_nodes(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual([], new_nodes)

    def test_split_image_mixed(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ", TextType.NORMAL),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" after", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_mixed(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png) after",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " and an ![image](https://i.imgur.com/3elNhQu.png) after", TextType.NORMAL),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    # unittest.main()
    TestDelimiterSplit().test_split_link_link_only()
