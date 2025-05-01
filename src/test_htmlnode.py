import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_default_values(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        child = HTMLNode("a", "Click here!", props={
                         "href": "https://google.com"})
        parent = HTMLNode("p", "See below link", [child])
        self.assertEqual(
            "HTMLNode(p, See below link, [HTMLNode(a, Click here!, None, {'href': 'https://google.com'})], None)",
            repr(parent)
        )

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click", props={
            "href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multi(self):
        props = {
            "prop1": "val1",
            "prop2": "val2",
            "prop3": "val3",
        }
        node = HTMLNode("p", "Paragraph", props=props)
        self.assertEqual(node.props_to_html(),
                         ' prop1="val1" prop2="val2" prop3="val3"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Simple paragraph")
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
