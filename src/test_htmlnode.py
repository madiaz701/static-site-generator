import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_one_prop(self):
        test_props = {"href": "https://www.google.com"}
        node = HTMLNode('a', 'Google link', None, test_props)
        expected_output = ' href="https://www.google.com"'
        actual_output = node.props_to_html()
        self.assertEqual(expected_output, actual_output)

    def test_props_to_html_multiple_props(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode('a', 'Google link', None, test_props)
        expected_output = ' href="https://www.google.com" target="_blank"'
        actual_output = node.props_to_html()
        self.assertEqual(expected_output, actual_output)
    
    def test_no_props(self):
        node = HTMLNode()
        expected_output = ''
        actual_output = node.props_to_html()
        self.assertEqual(expected_output, actual_output)