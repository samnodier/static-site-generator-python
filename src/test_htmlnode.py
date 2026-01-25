import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html_node, text_node_to_html_node

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        img_node = TextNode("A flower close-up", TextType.IMAGE, "flower.jpg")
        html_node = text_node_to_html_node(node)
        img_html_node = text_node_to_html_node(img_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(img_html_node.tag, "img")
        self.assertEqual(img_html_node.props_to_html(), ' src="flower.jpg" alt="A flower close-up"')

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

if __name__ == "__main__":
    unittest.main()
