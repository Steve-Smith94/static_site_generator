import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_three_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    
    def test_leading_and_trailing_newlines(self):
        md = """

First

Second

"""
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_multiple_blank_lines_collapsed(self):
        md = "One\n\n\n\nTwo\n\n\nThree"
        self.assertEqual(markdown_to_blocks(md), ["One", "Two", "Three"])

    def test_single_block_no_blank_lines(self):
        md = "Only one block with\ninternal newline"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Only one block with\ninternal newline"],
        )

    
    def test_whitespace_only_blocks_removed(self):
        md = "A\n\n   \n\t\nB"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

    def test_heading_paragraph_list(self):
        md = """# Title

A paragraph with text.

- item 1
- item 2
- item 3"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Title",
                "A paragraph with text.",
                "- item 1\n- item 2\n- item 3",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_blank_lines(self):
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])

if __name__ == "__main__":
    unittest.main()