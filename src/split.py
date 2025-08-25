import re

from extract import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
from typing import List

def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:TextType) -> List[TextNode]:
    if not delimiter:
        raise ValueError("Error: split_nodes_delimiter expecting valid delimiter")
    
    match text_type:
        case TextType.IMAGE | TextType.LINK | TextType.TEXT:
            raise ValueError("Error: split_nodes_delimiter invalid text type")
        case _:
            pass
    
    new_nodes:List[TextNode] = []
    pattern = f"({re.escape(delimiter.strip())})"
    for node in old_nodes:
        if not node:
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

def split_nodes_link(old_nodes:List[TextNode]) -> List[TextNode]:
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

