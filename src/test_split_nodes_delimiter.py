import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class Testsplit_nodes_delimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_node2s = split_nodes_delimiter([node2], "**", TextType.BOLD)
        manual_new_nodes = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),]
        manual_new_node2s = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, manual_new_nodes)
        self.assertEqual(new_node2s, manual_new_node2s)

if __name__ == "__main__":
    unittest.main()

