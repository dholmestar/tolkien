import unittest
from markdown_blocks import block_to_block_type, BlockType, markdown_to_blocks #type: ignore

class TestMarkdownBlocks(unittest.TestCase):
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
                "- This is a list\n- with items",
            ],
        )
    
    def test_single_block(self):
        md = "Just one block of text with no blank lines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block of text with no blank lines"])

    def test_extra_blank_lines(self):
        md = """

First block


Second block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_block_to_block_type_paragraph(self):
        block = "Just a normal paragraph."
        assert block_to_block_type(block) == BlockType.PARAGRAPH


    def test_block_to_block_type_heading(self):
        block = "## A heading"
        assert block_to_block_type(block) == BlockType.HEADING


    def test_block_to_block_type_code(self):
        block = "```\nprint('hi')\n```"
        assert block_to_block_type(block) == BlockType.CODE


    def test_block_to_block_type_quote(self):
        block = "> line one\n> line two"
        assert block_to_block_type(block) == BlockType.QUOTE


    def test_block_to_block_type_unordered_list(self):
        block = "- item 1\n- item 2"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST


    def test_block_to_block_type_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST


    def test_block_to_block_type_broken_ordered_list(self):
        block = "1. first\n3. third"
        assert block_to_block_type(block) == BlockType.PARAGRAPH