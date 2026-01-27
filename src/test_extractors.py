import unittest

from extractors import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        matches2 = extract_markdown_images(
            "![a](u1) and [b](u2)"
        )
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertEqual([("a", "u1")], matches2)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches2 = extract_markdown_links(
            "![a](u1) and [b](u2)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],  matches)
        self.assertEqual([("b", "u2")], matches2)

    def test_extract_title(self):
        md = "# This is a header"
        md2 = "#This is header with no space"
        md3 = "#        This is header with multiple spaces"
        h1 = extract_title(md)
        h21 = extract_title(md2)
        h31 = extract_title(md3)
        self.assertEqual(h1, "This is a header")
        self.assertEqual(h21, "This is header with no space")
        self.assertEqual(h31, "This is header with multiple spaces")

if __name__ == "__main__":
    unittest.main()

