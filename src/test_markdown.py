import unittest
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestMarkdown(unittest.TestCase):
    def test_basic_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)
        ])
    
    def test_nontext_passthrough(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is a bold node", TextType.BOLD)
        ])

    def test_multiple_delimiter(self):
        node = TextNode("This is text with a `code block` word and `another` block", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word and ", TextType.PLAIN),
            TextNode("another", TextType.CODE),
            TextNode(" block", TextType.PLAIN)
        ])

    def test_starts_with_delimiter(self):
        node = TextNode("`code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)
        ])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("This is `code` text", TextType.PLAIN),
            TextNode("This is bold", TextType.BOLD),
            TextNode("Another `code` here", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.PLAIN),
            TextNode("This is bold", TextType.BOLD),
            TextNode("Another ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.PLAIN),
        ])

    def test_invalid_markdown(self):
        with self.assertRaises(Exception):
            node = TextNode("This is `invalid markdown", TextType.PLAIN)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extract_mixed_content(self):
        text = """This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) 
        and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) with a link 
        [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"""
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_split_images_passthrough(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN)
            ],
            new_nodes,
        )
    
    def test_split_images_starts_with(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is first in the text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is first in the text", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_passthrough(self):
        node = TextNode(
            "This is text with no links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.PLAIN)
            ],
            new_nodes,
        )
    
    def test_split_links_starts_with(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) is first in the text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is first in the text", TextType.PLAIN)
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    