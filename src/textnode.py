from enum import Enum, auto

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str|None=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, value):
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"

    def get_html_tag(self):
        match self.text_type:
            case TextType.BOLD:
                return "b"
            case TextType.ITALIC:
                return "i"
            case TextType.CODE:
                return "code"
            case TextType.LINK:
                return "a"
            case TextType.IMAGE:
                return "img"
            case _:
                return None
    
    def get_html_value(self):
        match self.text_type:
            case TextType.IMAGE:
                return ""
            case _:
                return self.text

    def get_html_props(self):
        match self.text_type:
            case TextType.LINK:
                return {"href": self.url}
            case TextType.IMAGE:
                return {"src": self.url, "alt": self.text}
            case _:
                return None        

    