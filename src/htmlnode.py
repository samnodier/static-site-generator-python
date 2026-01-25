import re
from typing import List
from blocknode import BlockType
from blocktype import block_to_block_type
from spliters import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str | None] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "Not implemented. Child classes will overried this method."
        )

    # turn a dictionary of props to html props
    def props_to_html(self):
        html = ""
        if self.props:
            for key in self.props:
                html += f' {key}="{self.props[key]}"'

        return html

    def __repr__(self):
        htmlrepr = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        children_repr = ""
        if self.children:
            children_repr = "\n".join(repr(child) for child in self.children)
            return f"{htmlrepr[:-(len({self.tag})+5)]}{children_repr}</{self.tag}>"
        else:
            return f"{htmlrepr[:-(len({self.tag})+3)]}{children_repr}</{self.tag}>"


# A leaf node is a node without any other children in it.
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


# A parent node a node with children nodes in it
class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag argument is not optional")
        if self.children is None:
            raise ValueError(
                "Children argument is not optional. Parent tag needs children"
            )
        # Create tags for the parent and recursives call children
        # This will respectively rerun this function or run the to_html function of the children
        # POLYMORPHISM Woaahh
        return f'<{self.tag}{self.props_to_html()}>{"\n".join(child.to_html() for child in self.children)}</{self.tag}>'


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img", text_node.text, {"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("Invalid TextNode")


# Takes a string text and returns a list of HTMLNode objects
# Here I think I will use the spliter funciton I created
def text_to_children(text, type):
    html_node = []
    if type == BlockType.PARA or type == BlockType.QOTE:
        text_nodes = text_to_textnodes(" ".join(text.split("\n")))
        html_node = list(map(text_node_to_html_node, text_nodes))
    elif type == BlockType.HDNG:
        heading = " ".join(text.split("\n")).lstrip("# ")
        text_nodes = text_to_textnodes(heading)
        html_node = list(map(text_node_to_html_node, text_nodes))
    elif type == BlockType.UNDL or type == BlockType.ORDL:
        text_nodes = []
        for list_item in text.split("\n"):
            parent_node = ("li", text_to_textnodes(list_item[2:]))
            text_nodes.append(parent_node)
        html_node = list(map(text_node_to_html_node, text_nodes))

    return html_node



def markdown_to_html_node(markdown):
    children_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARA:
                nodes = text_to_children(block, BlockType.PARA)
                parent_p = ParentNode('p', nodes)
                children_nodes.append(parent_p)
            case BlockType.HDNG:
                count = 0
                for char in block:
                    if char == "#":
                        count += 1
                    else:
                        break
                nodes = text_to_children(block, BlockType.PARA)
                parent_h = ParentNode(f"h{count}", nodes)
                children_nodes.append(parent_h)
            case BlockType.QOTE:
                nodes = text_to_children(block, BlockType.PARA)
                parent_q = ParentNode('blockquote', nodes)
                children_nodes.append(parent_q)
            case BlockType.CODE:
                text_node = TextNode(block, TextType.CODE)
                nodes = text_node_to_html_node(text_node)
                parent_c = ParentNode("<pre>", [nodes])
                children_nodes.append(parent_c)
            case BlockType.UNDL:
                nodes = text_to_children(block, BlockType.PARA)
                parent_u = ParentNode('ul', nodes)
                children_nodes.append(parent_u)
            case BlockType.ORDL:
                nodes = text_to_children(block, BlockType.PARA)
                parent_u = ParentNode('ol', nodes)
                children_nodes.append(parent_u)
    parent_block = ParentNode("div", children_nodes)
    return parent_block
