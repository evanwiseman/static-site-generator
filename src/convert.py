import re

from blocknode import BlockNode, BlockType
from extract import split_nodes_delimiter, split_nodes_image, split_nodes_link, markdown_to_blocks
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from parentnode import ParentNode

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
    tag = text_node.get_html_tag()
    value = text_node.get_html_value()
    props = text_node.get_html_props()
    
    return LeafNode(tag, value, props)

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def block_node_to_html_node(block: BlockNode):
    text = block.text
    block_type = block.block_type
    match block.block_type:
        case BlockType.PARAGRAPH:
            return LeafNode(tag="p",value=text)
        
        case BlockType.HEADING:
            level = 0
            while level < len(text) and text[level] == "#" and level < 6:
                level += 1
            if level == 0:
                raise ValueError("Header level cannot be 0")
            return LeafNode(tag=f"h{level}", value=text[level:].lstrip())

        case BlockType.CODE:
            return ParentNode(
                tag="pre",
                children=[LeafNode(tag="code", value=text[3:-3])]
            )

        case BlockType.QUOTE:
            items = re.split(r'(?:^|\n)\s*>\s?', text)
            items = [item.strip() for item in items if item.strip()]
            return ParentNode(tag="blockquote", children=[LeafNode(tag="p", value=item) for item in items])
        
        case BlockType.UNORDERED_LIST:
            items = re.split(r'^\s*[-*+]\s', text, flags=re.MULTILINE)
            items = [item.strip() for item in items if item.strip()]
            return ParentNode(
                tag="ul",
                children=[LeafNode(tag="li", value=item) for item in items]
            )
        
        case BlockType.ORDERED_LIST:
            items = re.split(r'^\s*\d+\.\s', text, flags=re.MULTILINE)
            items = [item.strip() for item in items if item.strip()]
            return ParentNode(
                tag="ol",
                children=[LeafNode(tag="li", value=item) for item in items]
            )

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode(tag="div", children=[])
    for block in blocks:
        html_node = block_node_to_html_node(block)
        parent.children.append(html_node)
    return parent
        
            
        