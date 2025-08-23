from htmlnode import HTMLNode
from typing import Optional, Dict

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag:str|None,
        value:str,
        props:Optional[Dict[str, str]] = None
    ):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Error: LeafNode expecting value property")
        if not self.tag:
            return f"{self.value}"
        
        return f"<{self.tag}{self.props_to_html()}>" + (f"{self.value}</{self.tag}>" if self.value != "" else "")