import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Required value")
        self.assertEqual(node.to_html(), "Required value")

    def test_leaf_to_html_standard(self):
        node = LeafNode("p", "Required value")
        self.assertEqual(node.to_html(), "<p>Required value</p>")

    def test_leaf_to_html_with_props(self):
        props = {"href": "https://google.com"}
        node = LeafNode("a", "Click here", props)
        self.assertEqual(
            node.to_html(), '<a href="https://google.com">Click here</a>')

    def test_leaf_repr(self):
        props = {"href": "https://google.com"}
        node = LeafNode("a", "Click here", props)
        self.assertEqual(
            repr(node), "LeafNode(a, Click here, {'href': 'https://google.com'})")


if __name__ == "__main__":
    unittest.main()
