import re

from blocknode import BlockNode, BlockType
from textnode import TextNode, TextType
from typing import List

def valid_delimiter(delimiter:str) -> bool:
    if not delimiter.strip():
        return False
    return True

def valid_node(node) -> bool:
    if not node:
        return False
    return True

def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:TextType) -> List[TextNode]:
    if not valid_delimiter(delimiter):
        raise ValueError("Error: split_nodes_delimiter expecting valid delimiter")
    
    match text_type:
        case TextType.IMAGE | TextType.LINK | TextType.TEXT:
            raise ValueError("Error: split_nodes_delimiter invalid text type")
        case _:
            pass
    
    new_nodes:List[TextNode] = []
    pattern = f"({re.escape(delimiter.strip())})"
    for node in old_nodes:
        if not valid_node(node):
            raise ValueError("Error: split_nodes_delimiter node cannot be None")
        
        # Don't convert non TEXT nodes, append as is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Split node text by pattern
        parts = re.split(pattern, node.text)
        is_delimiter_open = False
        for part in parts:
            if not part:
                continue
            
            if part == delimiter:
                is_delimiter_open = not is_delimiter_open
                continue
            
            part_type = text_type if is_delimiter_open else node.text_type
            new_nodes.append(TextNode(part, part_type, node.url))
        
        # Check if delimiter was closed
        if is_delimiter_open:
            raise ValueError("Error: split_nodes_delimiter missing closing delimiter")                    
    
    return new_nodes

def extract_markdown_images(text) -> List[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> List[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes:List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not node:
            raise ValueError("Error: split_nodes_image node cannot be None")
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        matches = extract_markdown_images(node.text)
        parts = [node.text]
        
        # Find text and images and append to new_nodes
        for alt, url in matches:
            parts = parts[-1].split(f"![{alt}]({url})", maxsplit=1)
            
            if parts[0]: # Text before the image(s)
                new_nodes.append(TextNode(parts[0], node.text_type, node.url))
            
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        
        if parts[-1]: # Text trailing the image(s)
            new_nodes.append(TextNode(parts[-1], node.text_type, node.url))
            
    return new_nodes

def split_nodes_link(old_nodes:List[TextNode]) -> TextNode:
    new_nodes = []
    for node in old_nodes:
        if not node:
            raise ValueError("Error: split_nodes_link node cannot be None")
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        matches = extract_markdown_links(node.text)
        parts = [node.text]
        
        # Find text and images and append to new_nodes
        for alt, url in matches:
            parts = parts[-1].split(f"[{alt}]({url})", maxsplit=1)
            
            if parts[0]: # Text before the image(s)
                new_nodes.append(TextNode(parts[0], node.text_type, node.url))
            
            new_nodes.append(TextNode(alt, TextType.LINK, url))
        
        if parts[-1]: # Text trailing the image(s)
            new_nodes.append(TextNode(parts[-1], node.text_type, node.url))
            
    return new_nodes

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
