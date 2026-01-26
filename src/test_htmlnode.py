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

    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
            # Heading level 1

            ## Heading level 2

            ### Heading level 3

            #### Heading level 4

            ##### Heading level 5

            ###### Heading level 6
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading level 1</h1><h2>Heading level 2</h2><h3>Heading level 3</h3><h4>Heading level 4</h4><h5>Heading level 5</h5><h6>Heading level 6</h6></div>"
        )

    def test_blockquote(self):
        md = """
            > Dorothy followed her through many of the beautiful rooms in her castle.
        """
        md2 = """
            > Dorothy followed her through many of the beautiful rooms in her castle.
            >
            > The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.

        """
        node = markdown_to_html_node(md)
        node2 = markdown_to_html_node(md2)
        html = node.to_html()
        html2 = node2.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Dorothy followed her through many of the beautiful rooms in her castle.</blockquote></div>"
        )
        self.assertEqual(
            html2,
            "<div><blockquote>Dorothy followed her through many of the beautiful rooms in her castle. The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.</blockquote></div>"
        )
        
    def test_unordered_list(self):
        md = """
            - First item
            - Second item
            - Third item
            - Fourth item
            * Fifth item
            * Sixth item
        """
        md2 = """
            * First _item_
            * Second item
            * Third item
            * Fourth item
        """
        node = markdown_to_html_node(md)
        node2 = markdown_to_html_node(md2)
        html = node.to_html()
        html2 = node2.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li><li>Fifth item</li><li>Sixth item</li></ul></div>"
        )
        self.assertEqual(
            html2,
            "<div><ul><li>First <i>item</i></li><li>Second item</li><li>Third item</li><li>Fourth item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
            1. First item
            2. Second item
            3. Third item
            4. Fourth item
        """
        md2 = """
            1. First item
            8. Second item
            3. Third item
            5. Fourth item

        """
        node = markdown_to_html_node(md)
        node2 = markdown_to_html_node(md2)
        html = node.to_html()
        html2 = node2.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ol></div>"
        )
        self.assertEqual(
            html2,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ol></div>"
        )

    def test_html_mixed(self):
        md = """# The Main Title

            This is a paragraph with **bold** text and a [link](https://google.com).

            * Item 1
            * Item 2

            ```python
            print('hello')```

        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            """<div><h1>The Main Title</h1><p>This is a paragraph with <b>bold</b> text and a <a href="https://google.com">link</a>.</p><ul><li>Item 1</li><li>Item 2</li></ul><pre><code>python\nprint('hello')</code></pre></div>"""
        )

if __name__ == "__main__":
    unittest.main()
