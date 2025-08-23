from htmlnode import HTMLNode
from typing import Optional, List, Dict

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag:str,
        children:List[HTMLNode],
        props:Optional[Dict[str, str]] = None
    ):
        super().__init__(tag, "", children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: ParentNode expecting tag property")
        if not self.children:
            raise ValueError("Error: ParentNode expecting children property")

        return f"<{self.tag}>{"".join(child.to_html() for child in self.children)}</{self.tag}>"