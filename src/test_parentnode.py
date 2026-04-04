import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_multiple_children(self):
        bold_child = LeafNode('b', 'Bold text')
        normal_child = LeafNode(None, 'Normal text')
        italic_child = LeafNode('i', 'italic text')
        parent_node = ParentNode("p", [bold_child, normal_child, italic_child])
        self.assertEqual(parent_node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i></p>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

    def test_to_html_deeply_nested(self):
        great_grandchild = LeafNode("b", "deep")
        grandchild = ParentNode("span", [great_grandchild])
        child = ParentNode("p", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p><span><b>deep</b></span></p></div>")

    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode('p', None).to_html()
    
    def test_to_html_without_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            ParentNode(None, [child_node]).to_html()
    
