import unittest

from blocknode import BlockNode, BlockType
from convert import text_node_to_html_node, text_to_text_nodes, markdown_to_html_node, block_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

class TestTextNodeToHTMLNode(unittest.TestCase):
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


class TestTextToTextNodes(unittest.TestCase):
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

class TestBlockNodeToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        node = BlockNode("This is a paragraph.", BlockType.PARAGRAPH)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "This is a paragraph.")

    def test_headings(self):
        node1 = BlockNode("# Heading 1", BlockType.HEADING)
        node2 = BlockNode("## Heading 2", BlockType.HEADING)
        node3 = BlockNode("### Heading 3", BlockType.HEADING)
        self.assertEqual(block_node_to_html_node(node1).tag, "h1")
        self.assertEqual(block_node_to_html_node(node1).value, "Heading 1")
        self.assertEqual(block_node_to_html_node(node2).tag, "h2")
        self.assertEqual(block_node_to_html_node(node2).value, "Heading 2")
        self.assertEqual(block_node_to_html_node(node3).tag, "h3")
        self.assertEqual(block_node_to_html_node(node3).value, "Heading 3")

    def test_code_block(self):
        code_text = "```\nprint('Hello')\nprint('World')\n```"
        node = BlockNode(code_text, BlockType.CODE)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "code")
        self.assertIn("print('Hello')", html_node.children[0].value)
        self.assertIn("print('World')", html_node.children[0].value)

    def test_blockquote(self):
        quote_text = "> First line\n> Second line\n> Third line"
        node = BlockNode(quote_text, BlockType.QUOTE)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node.tag, "blockquote")
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].value, "First line")
        self.assertEqual(html_node.children[1].value, "Second line")
        self.assertEqual(html_node.children[2].value, "Third line")

    def test_unordered_list(self):
        ul_text = "- Item 1\n- Item 2\n- Item 3"
        node = BlockNode(ul_text, BlockType.UNORDERED_LIST)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node.tag, "ul")
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].value, "Item 1")
        self.assertEqual(html_node.children[1].value, "Item 2")
        self.assertEqual(html_node.children[2].value, "Item 3")

    def test_ordered_list(self):
        ol_text = "1. First\n2. Second\n3. Third"
        node = BlockNode(ol_text, BlockType.ORDERED_LIST)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node.tag, "ol")
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].value, "First")
        self.assertEqual(html_node.children[1].value, "Second")
        self.assertEqual(html_node.children[2].value, "Third")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_all_types(self):
        markdown = """
        # Heading 1
        
        ## Heading 2
        
        ### Heading 3
        
        ```
        This is a code block
        
        of code
        
        and it contains multiple lines
        ```
        
        > We have quotes
        > Many quotes
        > So many quotes
        
        And paragraphs that contain text
        And newlines
        
        - There are also lists
        - That are unordered
        - Like this one
        
        1. And there are ordered lists
        2. That have numbers
        3. Like this one
        
        
        
        
        """
        
        html_root = markdown_to_html_node(markdown)
        html = html_root.children  # top-level nodes

        # Headings
        self.assertEqual(html[0].tag, "h1")
        self.assertEqual(html[0].value, "Heading 1")
        self.assertEqual(html[1].tag, "h2")
        self.assertEqual(html[1].value, "Heading 2")
        self.assertEqual(html[2].tag, "h3")
        self.assertEqual(html[2].value, "Heading 3")

        # Code block
        code_node = html[3]
        self.assertEqual(code_node.tag, "pre")
        self.assertEqual(len(code_node.children), 1)
        self.assertEqual(code_node.children[0].tag, "code")
        self.assertIn("This is a code block", code_node.children[0].value)
        self.assertIn("of code", code_node.children[0].value)
        self.assertIn("and it contains multiple lines", code_node.children[0].value)

        # Blockquote
        blockquote_node = html[4]
        self.assertEqual(blockquote_node.tag, "blockquote")
        self.assertEqual(len(blockquote_node.children), 3)
        self.assertEqual(blockquote_node.children[0].value, "We have quotes")
        self.assertEqual(blockquote_node.children[1].value, "Many quotes")
        self.assertEqual(blockquote_node.children[2].value, "So many quotes")

        # Paragraph
        paragraph_node = html[5]
        self.assertEqual(paragraph_node.tag, "p")
        self.assertIn("And paragraphs that contain text", paragraph_node.value)
        self.assertIn("And newlines", paragraph_node.value)

        # Unordered list
        ul_node = html[6]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)
        self.assertEqual(ul_node.children[0].value, "There are also lists")
        self.assertEqual(ul_node.children[1].value, "That are unordered")
        self.assertEqual(ul_node.children[2].value, "Like this one")

        # Ordered list
        ol_node = html[7]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)
        self.assertEqual(ol_node.children[0].value, "And there are ordered lists")
        self.assertEqual(ol_node.children[1].value, "That have numbers")
        self.assertEqual(ol_node.children[2].value, "Like this one")


if __name__ == "__main__":
    unittest.main()