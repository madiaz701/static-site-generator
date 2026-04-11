import unittest
from markdown import extract_title, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestMarkdown(unittest.TestCase):
    
    #######################################
    # SPLIT NODES DELIMITER TESTS
    #######################################
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


    #######################################
    # EXTRACT MARKDOWN TESTS
    #######################################

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

    #######################################
    # SPLIT IMAGES TESTS
    #######################################

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

    #######################################
    # SPLIT LINKS TESTS
    #######################################

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

    #######################################
    # TEXT TO TEXTNODE TESTS
    #######################################

    def test_text_to_textnode(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.assertEqual([
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], text_to_textnodes(text))
    
    def test_text_to_textnode_plain(self):
        text = "This is plain text only, not expecting any splits"
        self.assertEqual(text_to_textnodes(text), [TextNode(text, TextType.PLAIN)])
    
    def test_text_to_textnode_invalid_markdown(self):
        text = "This is **an example of invalid markdown"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

    def test_extract_title(self):
        md = """# This is the title
This is the subtitle
"""
        self.assertEqual(extract_title(md), "This is the title")

    def test_extract_title_no_title(self):
        md = """This is the subtitle
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_middle_title_exception(self):
        md = """This is the subtitle
# This is the title
"""
        with self.assertRaises(Exception):
            extract_title(md)
