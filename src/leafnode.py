from htmlnode import HTMLNode
from typing import Optional, Dict

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag:str,
        value:str,
        props:Optional[Dict[str, str]] = None
    ):
        super().__init__(
            tag, 
            value, 
            None, 
            props
        )
    
    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"