import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        
        self.assertEqual(
            node.props_to_html(),
            " href=\"https://www.google.com\" target=\"_blank\""
        )
    
    def test_props_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_repr_empty(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")
    
    def test_repr(self):
        node = HTMLNode(
            tag="h",
            value="This is a heading",
            children=[HTMLNode()],
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            str(node),
            "HTMLNode(h, This is a heading, [HTMLNode(None, None, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
        )

if __name__ == "__main__":
    unittest.main()