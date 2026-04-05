import unittest
from blocks import markdown_to_blocks


class TestMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items"
                ],
            )

        def test_empty_blocks(self):
            md = """
This is **bolded** paragraph



- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "- This is a list\n- with items"
                ],
            )

        def test_leading_and_trailing_space_block_level(self):
            md = """
   This is **bolded** paragraph

- This is a list
- with items     
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "- This is a list\n- with items"
                ],
            )