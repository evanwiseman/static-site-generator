from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
    tag = text_node.text_type.value
    match text_node.text_type:
        case TextType.TEXT | TextType.BOLD | TextType.ITALIC | TextType.CODE:
            return LeafNode(text_node.text_type.value, text_node.text)
        case TextType.LINK:
            return LeafNode(text_node.text_type.value, text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(text_node.text_type.value, "", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise TypeError("Error: text_node_to_html_node can't find TextType")
        