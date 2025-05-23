import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_parent_node_repr(self):
        child = LeafNode("a", "Click here!", props={
                         "href": "https://google.com"})
        parent = ParentNode("p", [child], {"class": "red"})
        expected = "ParentNode(p, [LeafNode(a, Click here!, {'href': 'https://google.com'})], {'class': 'red'})"
        self.assertEqual(repr(parent), expected)

    def test_parent_node_empty_children(self):
        node = ParentNode("div", children=[])
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html_single(self):
        child = LeafNode("a", "Click here!", props={
                         "href": "https://google.com"})
        parent = ParentNode("p", [child])
        expected = '<p><a href="https://google.com">Click here!</a></p>'
        self.assertEqual(parent.to_html(), expected)

    def test_parent_to_html_multiple_leaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_to_html_with_grandchildren(self):
        leaf = LeafNode("a", "clik")
        mid = ParentNode("p", [leaf])
        parent = ParentNode("p", [mid])
        expected = "<p><p><a>clik</a></p></p>"
        self.assertEqual(parent.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
