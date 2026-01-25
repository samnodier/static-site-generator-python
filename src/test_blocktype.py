import unittest

from blocknode import BlockType
from blocktype import block_to_block_type
from spliters import markdown_to_blocks

class TestBlockType(unittest.TestCase):
    def test_blocktype(self):
        heading = "## This is a Heading"

        paragraph = "This is a simple paragraph that contains some text to describe what is happening in this markdown file."

        quote = "> This is a blockquote. It usually contains a famous saying or a citation that stands out from the rest of the text."

        unordered_list = """
            * This is the first item in an unordered list
            * This is the second item
            * This is the third item
        """

        ordered_list = """
            1. This is the first item in an ordered list
            2. This is the second item
            3. This is the third item
        """

        code = """
            ```python
            def hello_world():
                print("This is a code block")
            ```
        """

        h_type = block_to_block_type(markdown_to_blocks(heading)[0])
        p_type = block_to_block_type(markdown_to_blocks(paragraph)[0])
        q_type = block_to_block_type(markdown_to_blocks(quote)[0])
        u_type = block_to_block_type(markdown_to_blocks(unordered_list)[0])
        o_type = block_to_block_type(markdown_to_blocks(ordered_list)[0])
        c_type = block_to_block_type(markdown_to_blocks(code)[0])

        self.assertEqual(h_type, BlockType.HDNG)
        self.assertEqual(p_type, BlockType.PARA)
        self.assertEqual(q_type, BlockType.QOTE)
        self.assertEqual(u_type, BlockType.UNDL)
        self.assertEqual(o_type, BlockType.ORDL)
        self.assertEqual(c_type, BlockType.CODE)

if __name__ == "__main__":
    unittest.main()
