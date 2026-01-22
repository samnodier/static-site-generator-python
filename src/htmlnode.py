from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str | None] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented. Child classes will overried this method.")

    def props_to_html(self):
        html = ""
        if self.props:
            for key in self.props:
                html += f' {key}="{self.props[key]}"'

        return html

    def __repr__(self):
        htmlrepr = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        children_repr = ""
        if self.children:
            children_repr = "\n".join(repr(child) for child in self.children)
            return f"{htmlrepr[:-(len({self.tag})+5)]}{children_repr}</{self.tag}>"
        else:
            return f"{htmlrepr[:-(len({self.tag})+3)]}{children_repr}</{self.tag}>"

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None = None, value: str | None = None, props: dict[str, str | None] | None = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str | None] | None = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag argument is not optional")
        if self.children is None:
            raise ValueError("Children argument is not optional. Parent tag needs children")
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
            return LeafNode("img", text_node.text, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextNode")
