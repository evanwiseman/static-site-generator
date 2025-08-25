import unittest

from extract import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()