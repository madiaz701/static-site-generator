import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type


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

        def test_block_to_blockType_paragraph(self):
            md = """
This is just regular text
Nothing to see here
"""
            blockType = block_to_block_type(md)
            self.assertEqual(blockType, BlockType.PARAGRAPH)

        def test_block_to_blockType_heading(self):
            md = '### This is a heading block'
            blockType = block_to_block_type(md)
            self.assertEqual(blockType, BlockType.HEADING)

        # DO MORE block_to_block_type TESTS!!!!!!