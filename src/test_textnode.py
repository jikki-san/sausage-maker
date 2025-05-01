import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Test node", TextType.LINK, "https://google.com")
        node2 = TextNode("Test node", TextType.LINK, "https://google.com")
        self.assertEqual(node1, node2)

    def test_text_neq(self):
        node1 = TextNode("Test node", TextType.LINK, "https://google.com")
        node2 = TextNode("Other test node", TextType.LINK,
                         "https://google.com")
        self.assertNotEqual(node1, node2)

    def test_text_type_neq(self):
        node1 = TextNode("Test node", TextType.LINK, "https://google.com")
        node2 = TextNode("Test node", TextType.IMAGE, "https://google.com")
        self.assertNotEqual(node1, node2)

    def test_url_neq(self):
        node1 = TextNode("Test node", TextType.LINK, "https://google.com")
        node2 = TextNode("Test node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node1, node2)

    def test_url_default_none(self):
        node1 = TextNode("Test node", TextType.LINK, None)
        node2 = TextNode("Test node", TextType.LINK)
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode("Test node", TextType.LINK, "https://google.com")
        self.assertEqual(
            "TextNode(Test node, link, https://google.com)", repr(node))


if __name__ == "__main__":
    unittest.main()
