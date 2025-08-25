from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

class BlockNode:
    def __init__(self, text:str, block_type:BlockType):
        self.text = text
        self.block_type = block_type
    
    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type})"