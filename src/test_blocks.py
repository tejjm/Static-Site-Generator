import unittest
from split_blocks import markdown_to_blocks, BlockType,block_to_block_type




class TestHTMLNode(unittest.TestCase):
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

        def test_two_new_lines_blocks(self):
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

        def test_markdown_to_blocks_extra_whitespace(self):
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

        def test_markdown_to_blocks_emptystr(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks,[])


        def test_block_type_heading(self):
            block = "## This is a correct heading"
            expected = BlockType.HEADING
            self.assertEqual(expected,block_to_block_type(block))

        def test_code_type(self):
             block = "```\n This is a code block \n```"
             expected = BlockType.CODE
             self.assertEqual(expected,block_to_block_type(block))
            
        def test_quote_type(self):
             block = ">This is a quote \n>This is also a quote \n>This is also another quote"
             expected = BlockType.QUOTE
             self.assertEqual(expected,block_to_block_type(block))

        def test_unordered_list(self):
             block = "- This is first but unordered\n- This is second but unordered"
             expected = BlockType.UNORDERED_LIST
             self.assertEqual(expected,block_to_block_type(block))

        def test_ordered_list(self):
             block = "1. Whats up \n2. Nothing you tell me \n3. Nothing from my end"
             expected = BlockType.ORDERED_LIST
             self.assertEqual(expected,block_to_block_type(block))
        