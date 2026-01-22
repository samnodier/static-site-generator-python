import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "Google", props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "Boot.dev", props={"href": "https://www.boot.dev", "target": "_blank"})
        node3 = HTMLNode("div", children=[node, node2])
        node_props = ' href="https://www.google.com" target="_blank"'
        node2_props = ' href="https://www.boot.dev" target="_blank"'
        node3_props = ""
        self.assertEqual(node.props_to_html(), node_props)
        self.assertEqual(node2.props_to_html(), node2_props)
        self.assertEqual(node3.props_to_html(), node3_props)

if __name__ == "__main__":
    unittest.main()
