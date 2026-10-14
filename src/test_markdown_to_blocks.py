import unittest
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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
    def test_block_to_block_type(self):
        assert block_to_block_type("# Heading") == BlockType.HEADING
        assert block_to_block_type("###### Heading") == BlockType.HEADING
        assert block_to_block_type("####### Heading") == BlockType.PARAGRAPH

        assert block_to_block_type("```\nprint('hello')\n```") == BlockType.CODE

        assert block_to_block_type("> Quote") == BlockType.QUOTE
        assert block_to_block_type("> First\n>Second") == BlockType.QUOTE
        assert block_to_block_type("> First\nSecond") == BlockType.PARAGRAPH

        assert block_to_block_type("- First\n- Second") == BlockType.UNORDERED_LIST
        assert block_to_block_type("- First\nSecond") == BlockType.PARAGRAPH

        assert block_to_block_type("1. First\n2. Second") == BlockType.ORDERED_LIST
        assert block_to_block_type("1. First\n3. Second") == BlockType.PARAGRAPH

        assert block_to_block_type("Normal paragraph") == BlockType.PARAGRAPH

if __name__ == "__main__":
    unittest.main()