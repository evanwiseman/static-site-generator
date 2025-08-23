import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_to_html_with_inline_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        
    def test_to_html_with_only_parents(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)
    
    def test_to_html_with_empty_tag(self):
        node = ParentNode("", [LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_empty_tag_children(self):
        child_node = ParentNode("", [LeafNode(None, "Normal text")])
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)
    
    def test_child_to_parent_to_child(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        child_node.children = [parent_node]
        self.assertRaises(RecursionError, parent_node.to_html)

if __name__ == "__main__":
    unittest.main()