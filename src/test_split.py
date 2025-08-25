
import unittest

from split import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_to_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_text_to_bold(self):
        node = TextNode(
            "This is text with a **bold block** word",
            TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_text_no_delimiter(self):
        node = TextNode("This is text without a delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text without a delimiter", TextType.TEXT)
            ]
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_multi_before_and_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and text after", TextType.TEXT)
            ],
            new_nodes,
        )
    
    def test_no_image(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_image_only(self):
        node = TextNode(
            "![only](https://example.com/only.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("only", TextType.IMAGE, "https://example.com/only.png")],
            new_nodes
        )

    def test_image_at_start(self):
        node = TextNode(
            "![start](https://example.com/start.png) and then text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" and then text", TextType.TEXT)
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = TextNode(
            "Text before ![end](https://example.com/end.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes
        )

    def test_multiple_adjacent(self):
        node = TextNode(
            "![one](url1)![two](url2)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode("two", TextType.IMAGE, "url2")
            ],
            new_nodes
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_multi_before_and_after(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )
        
    def test_no_link(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_no_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_with_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
    
    def test_link_only(self):
        node = TextNode(
            "[boot](https://boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("boot", TextType.LINK, "https://boot.dev")],
            new_nodes
        )

    def test_link_at_start(self):
        node = TextNode(
            "[boot](https://boot.dev) is a good site",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" is a good site", TextType.TEXT)
            ],
            new_nodes
        )

    def test_link_at_end(self):
        node = TextNode(
            "Visit [boot](https://boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_multiple_adjacent(self):
        node = TextNode(
            "[one](url1)[two](url2)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "url1"),
                TextNode("two", TextType.LINK, "url2"),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main()