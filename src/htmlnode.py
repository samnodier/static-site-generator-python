class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
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
