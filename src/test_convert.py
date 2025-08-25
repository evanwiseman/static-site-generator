import unittest

from convert import text_node_to_html_node, text_to_text_nodes
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType


class TestConvert(unittest.TestCase):
    # text_node_to_html_node
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.boot.dev\">This is a link</a>")
    
    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://www.boot.dev', 'alt': 'This is a image node'})
        self.assertEqual(html_node.to_html(), "<img src=\"https://www.boot.dev\" alt=\"This is a image node\">")

    # text_to_text_nodes
    def test_text_to_text_nodes_full_pipeline(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    
    def test_text_to_text_nodes_plain_text(self):
        text = "Just plain text"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [TextNode("Just plain text", TextType.TEXT)]
        )
    
    def test_text_to_text_nodes_bold_only(self):
        text = "Hello **world**!"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ]
        )

    def test_text_to_text_nodes_multiple_italics(self):
        text = "_first_ then _second_"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("first", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("second", TextType.ITALIC),
            ]
        )

    def test_text_to_text_nodes_code_only(self):
        text = "`inline code`"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [TextNode("inline code", TextType.CODE)]
        )
    
    def test_text_to_text_nodes_image_only(self):
        text = "![alt](https://example.com/img.png)"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")]
        )
    
    def test_text_to_text_nodes_link_only(self):
        text = "[Boot.dev](https://boot.dev)"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [TextNode("Boot.dev", TextType.LINK, "https://boot.dev")]
        )
    
    def test_text_to_text_nodes_adjacent_elements(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ]
        )
    
    def test_text_to_text_nodes_mixed(self):
        text = "Here is **bold**, _italic_, and a [link](https://x.com)"
        nodes = text_to_text_nodes(text)

        self.assertListEqual(
            nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://x.com"),
            ]
        )

    def test_text_to_text_nodes_unbalanced_bold_raises(self):
        text = "This is **broken bold"
        with self.assertRaises(ValueError):
            text_to_text_nodes(text)


if __name__ == "__main__":
    unittest.main()