import unittest

from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestDelimiterSplit(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This `code block` is simple", TextType.TEXT)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" is simple", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_multiple_same_delimiter(self):
        node = TextNode(
            "This `code block` is simple and this `code block` is too", TextType.TEXT)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" is simple and this ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" is too", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_multiple_diff_delimiter(self):
        node = TextNode(
            "This `code block` is relevant; this *bold text* is not", TextType.TEXT)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" is relevant; this *bold text* is not", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_beginning_delimiter(self):
        node = TextNode("`This here` was a code block", TextType.TEXT)
        expected = [
            TextNode("This here", TextType.CODE),
            TextNode(" was a code block", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(
            [node], "`", TextType.CODE), expected)

    def test_ending_delimiter(self):
        node = TextNode("This is another edge `code block`", TextType.TEXT)
        expected = [
            TextNode("This is another edge ", TextType.TEXT),
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
            TextNode("This `code block` is neat", TextType.TEXT),
            TextNode("This is another code block", TextType.CODE),
            TextNode("This is one last `code block`", TextType.TEXT),
        ]
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" is neat", TextType.TEXT),
            TextNode("This is another code block", TextType.CODE),
            TextNode("This is one last ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
        self.assertEqual(split_nodes_delimiter(
            nodes, "`", TextType.CODE), expected)

    def test_split_image_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_no_image(self):
        node = TextNode(
            "This is text with no images in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no images in it", TextType.TEXT)],
            new_nodes,
        )

    def test_split_image_duplicate_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_neighboring_images(self):
        node = TextNode(
            "This is text with ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) together",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" together", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_no_prefix(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) starts the node",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_no_suffix(self):
        node = TextNode(
            "Text with image: ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with image: ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
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
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "This is text with no links in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no links in it", TextType.TEXT)],
            new_nodes,
        )

    def test_split_link_duplicate_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_neighboring_links(self):
        node = TextNode(
            "This is text with [link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png) together",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" together", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_no_prefix(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) starts the node",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_no_suffix(self):
        node = TextNode(
            "Text with link: [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with link: ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_link_link_only(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
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
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_mixed(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/3elNhQu.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " and an ![image](https://i.imgur.com/3elNhQu.png) after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_text_only(self):
        text = "This just text tho"
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
