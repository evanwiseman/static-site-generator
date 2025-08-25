from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from extract import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_node_to_html_node(text_node:TextNode) -> HTMLNode:
    tag = text_node.text_type.value
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise TypeError("Error: text_node_to_html_node can't find TextType")

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes