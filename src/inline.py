import re

from textnode import TextNode, TextType
from typing import List

def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str|None, text_type:TextType):
    new_nodes:List[TextNode] = []
    if delimiter is None:
        if text_type == TextType.TEXT:
            text = "".join([node.text for node in old_nodes])
            return [TextNode(text, text_type, None)]
        else:
            raise ValueError("Error: split_nodes_delimiter delimiter invalid type")
    else:
        pattern = f"({re.escape(delimiter)})"
        for node in old_nodes:
            parts = re.split(pattern, node.text)
            part_type = node.text_type
            inside = False
            for part in parts:
                if part == delimiter:       # Toggle inside flag (Track if delimiter has a matching pair)
                    inside = not inside
                elif part:
                    part_type = text_type if inside else node.text_type
                    if new_nodes and new_nodes[-1].text_type == part_type:
                        new_nodes[-1].text += part
                    else:
                        new_nodes.append(TextNode(part, part_type))
            
            if inside:
                raise ValueError("Error: split_nodes_delimiter missing closing delimiter")                    
    
    return new_nodes
        