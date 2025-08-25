import unittest

from blocknode import BlockNode, BlockType
from extract import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_link, markdown_to_blocks
)
from textnode import TextNode, TextType


class TestExtractInline(unittest.TestCase):
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


class TestMarkdownToBlocks(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.PARAGRAPH)
        self.assertEqual(blocks[0].text, "This is a paragraph.")

    def test_heading(self):
        md = "# Heading 1\n\n## Heading 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0].block_type, BlockType.HEADING)
        self.assertEqual(blocks[0].text, "# Heading 1")
        self.assertEqual(blocks[1].block_type, BlockType.HEADING)
        self.assertEqual(blocks[1].text, "## Heading 2")

    def test_code_block(self):
        md = "```\ncode line 1\ncode line 2\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.CODE)
        self.assertIn("code line 1", blocks[0].text)
        self.assertIn("code line 2", blocks[0].text)

    def test_quote_block(self):
        md = "> This is a quote\n> spanning multiple lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.QUOTE)
        self.assertIn("spanning multiple lines", blocks[0].text)

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.UNORDERED_LIST)
        self.assertIn("Item 2", blocks[0].text)

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.ORDERED_LIST)
        self.assertIn("Second", blocks[0].text)
    
    def test_paragraph_with_inline_code(self):
        md = "This is a paragraph with `inline code` inside."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.PARAGRAPH)
        self.assertIn("`inline code`", blocks[0].text)

    def test_paragraph_with_bold_italic(self):
        md = "This has **bold** text and _italic_ text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.PARAGRAPH)
        self.assertIn("**bold**", blocks[0].text)
        self.assertIn("_italic_", blocks[0].text)

    def test_paragraph_with_link(self):
        md = "Check out [Google](https://google.com) for more info."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.PARAGRAPH)
        self.assertIn("[Google](https://google.com)", blocks[0].text)

    def test_mixed_inline_in_code(self):
        md = "```\nSome code with `inline` backticks inside\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.CODE)
        self.assertIn("`inline`", blocks[0].text)

    def test_inline_quote_in_paragraph(self):
        md = "He said, > 'This is inline quote style' in the paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].block_type, BlockType.PARAGRAPH)
        self.assertIn("> 'This is inline quote style'", blocks[0].text)


if __name__ == "__main__":
    unittest.main()