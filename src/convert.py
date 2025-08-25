import re

from blocknode import BlockNode, BlockType
from htmlnode import HTMLNode
from leafnode import LeafNode
from split import split_nodes_delimiter, split_nodes_link, split_nodes_image
from textnode import TextNode, TextType
from typing import List
from parentnode import ParentNode

def text_to_html_nodes(text):
    text_nodes = text_to_text_nodes(text)
    return map(text_node_to_html_node, text_nodes)

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
    tag = text_node.get_html_tag()
    value = text_node.get_html_value()
    props = text_node.get_html_props()
    
    return LeafNode(tag, value, props)

def text_to_text_nodes(text) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown: str) -> List[BlockNode]:
    blocks = []
    current_block = []
    current_type = None
    in_code_block = False

    def flush_block():
        nonlocal current_block, current_type
        if current_block:
            blocks.append(BlockNode("\n".join(current_block).strip(), current_type or BlockType.PARAGRAPH))
            current_block = []
            current_type = None

    for line in markdown.splitlines():
        stripped = line.strip()

        # Detect code block fences
        if stripped.startswith("```"):
            if in_code_block:
                current_block.append(line)
                flush_block()
                in_code_block = False
            else:
                flush_block()
                current_block.append(line)
                current_type = BlockType.CODE
                in_code_block = True
            continue

        if in_code_block:
            current_block.append(line)
            continue

        # Skip empty lines outside of code
        if stripped == "":
            flush_block()
            continue

        # Detect block types
        if re.match(r"^#+\s", stripped):
            flush_block()
            current_block.append(line)
            current_type = BlockType.HEADING
            flush_block()
        elif stripped.startswith(">"):
            if current_type != BlockType.QUOTE:
                flush_block()
                current_type = BlockType.QUOTE
            current_block.append(line)
        elif re.match(r"^(\*|-|\+)\s", stripped):
            if current_type != BlockType.UNORDERED_LIST:
                flush_block()
                current_type = BlockType.UNORDERED_LIST
            current_block.append(line)
        elif re.match(r"^\d+\.\s", stripped):
            if current_type != BlockType.ORDERED_LIST:
                flush_block()
                current_type = BlockType.ORDERED_LIST
            current_block.append(line)
        else:
            if current_type not in (None, BlockType.PARAGRAPH):
                flush_block()
            current_type = BlockType.PARAGRAPH
            current_block.append(line)
    
    if in_code_block:
        raise ValueError("Error: markdown_to_blocks missing closing delimiter code block")

    flush_block()
    return blocks

def block_node_to_html_node(block: BlockNode):
    text = block.text
    block_type = block.block_type
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(
                tag="p",
                children=text_to_html_nodes(text)
            )
        
        case BlockType.HEADING:
            level = 0
            while level < len(text) and text[level] == "#" and level < 6:
                level += 1
            if level == 0:
                raise ValueError("Header level cannot be 0")
            return ParentNode(
                tag=f"h{level}", 
                children=text_to_html_nodes(text[level:].lstrip())
            )

        case BlockType.CODE:
            return ParentNode(
                tag="pre",
                children= [
                    LeafNode(tag="code", value=text[3:-3])
                ]
            )

        case BlockType.QUOTE:
            lines = text.splitlines()
            items = [line.lstrip("> ").rstrip() for line in lines if line.strip("> ").strip()]
            return ParentNode(
                tag="blockquote", 
                children=[LeafNode(None, value=item) for item in items]
            )
        
        case BlockType.UNORDERED_LIST:
            items = re.split(r'^\s*[-*+]\s', text, flags=re.MULTILINE)
            items = [item.strip() for item in items if item.strip()]
            return ParentNode(
                tag="ul",
                children=[ParentNode("li", children=text_to_html_nodes(item)) for item in items]
            )
        
        case BlockType.ORDERED_LIST:
            items = re.split(r'^\s*\d+\.\s', text, flags=re.MULTILINE)
            items = [item.strip() for item in items if item.strip()]
            return ParentNode(
                tag="ol",
                children=[ParentNode("li", children=text_to_html_nodes(item)) for item in items]
            )

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode(tag="div", children=[])
    for block in blocks:
        html_node = block_node_to_html_node(block)
        parent.children.append(html_node)
    return parent
        
            
        