import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links


class TestRegexExtraction(unittest.TestCase):
    def test_single_link(self):
        text = "This [link](https://google.com) is cool"
        expected = [("link", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "This [link](https://google.com) is cool and this [other link](https://bing.com) is too"
        expected = [("link", "https://google.com"),
                    ("other link", "https://bing.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_duplicate_links(self):
        text = "This [link](https://google.com) is cool and this [link](https://google.com) is equally cool"
        expected = [("link", "https://google.com"),
                    ("link", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "What link?"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_only(self):
        text = "[link](https://google.com)"
        expected = [("link", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_single_image(self):
        text = "This ![image](https://google.com) is cool"
        expected = [("image", "https://google.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "This ![image](https://google.com) is cool and this ![other image](https://bing.com) is too"
        expected = [("image", "https://google.com"),
                    ("other image", "https://bing.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "What image?"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_only(self):
        text = "![image](https://google.com)"
        expected = [("image", "https://google.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_mixed_links_images(self):
        text = "This ![image](https://google.com) is cool and this [link](https://bing.com) is too"
        expected_images = [("image", "https://google.com")]
        expected_links = [(("link", "https://bing.com"))]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)

    def test_link_image_only(self):
        text = "![image](https://google.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_image_link_only(self):
        text = "[link](https://google.com)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)


if __name__ == "__main__":
    unittest.main()
