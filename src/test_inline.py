import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter


class TestConvert(unittest.TestCase):
    def test_text_to_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )
            
    def test_text_to_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
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
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text without a delimiter", TextType.TEXT)
            ]
        )
    
    def test_bold_to_text(self):
        node = TextNode("This is bold text to plain text", TextType.BOLD)
    
    def test_merge(self):
        node1 = TextNode("This is text 1 ", TextType.TEXT)
        node2 = TextNode("This is text 2 ", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], None, TextType.TEXT)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text 1 This is text 2 ", TextType.TEXT)
            ]
        )
    
    def test_different_type_merge(self):
        node1 = TextNode("This is _italic text_", TextType.TEXT)
        node2 = TextNode("This is already italic", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic textThis is already italic", TextType.ITALIC)
            ]
        )

if __name__ == "__main__":
    unittest.main()