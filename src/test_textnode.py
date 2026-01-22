import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text node", TextType.BOLD)
        node4 = TextNode("This is a different text node", TextType.PLAIN)
        lnode = TextNode("This is a link node", TextType.ANCHOR, url="https://google.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node3, node4)

if __name__ == "__main__":
    unittest.main()
