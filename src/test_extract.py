import unittest

from extract import extract_markdown_images, extract_markdown_links, extract_markdown_title


class TestExtractMarkdownImages(unittest.TestCase):
    def test_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual(
            [],
            matches
        )
    
    def test_links(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [],
            matches
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )
    
    def test_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual(
            [],
            matches
        )
    
    def test_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)


import unittest

class TestExtractMarkdownTitle(unittest.TestCase):
    def test_simple_h1(self):
        text = "# Hello World"
        self.assertEqual(extract_markdown_title(text), "Hello World")

    def test_leading_spaces(self):
        text = "   # Title With Spaces"
        self.assertEqual(extract_markdown_title(text), "Title With Spaces")

    def test_trailing_spaces(self):
        text = "# Title With Trailing   "
        self.assertEqual(extract_markdown_title(text), "Title With Trailing")

    def test_multiple_lines_first_is_h1(self):
        text = "# First Title\n\nSome text\n\n## Subtitle"
        self.assertEqual(extract_markdown_title(text), "First Title")

    def test_multiple_lines_h1_after_text(self):
        text = "Intro paragraph\n\n# Second Title\n\nMore text"
        self.assertEqual(extract_markdown_title(text), "Second Title")

    def test_no_h1_raises(self):
        text = "## This is not an H1\n\nParagraph text"
        with self.assertRaises(Exception):
            extract_markdown_title(text)

    def test_windows_line_endings(self):
        text = "# Windows Title\r\nSome text"
        self.assertEqual(extract_markdown_title(text), "Windows Title")

if __name__ == "__main__":
    unittest.main()