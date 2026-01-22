from htmlnode import HTMLNode
from textnode import TextNode
from textnode import TextType

def main():
    text = TextNode("This is some bold text", TextType.BOLD, "https://google.com")
    node = HTMLNode("a", "Google", props={"href": "https://www.google.com", "target": "_blank"})
    node2 = HTMLNode("a", "Boot.dev", props={"href": "https://www.boot.dev", "target": "_blank"})
    node3 = HTMLNode("div", children=[node, node2])
    print(node)
    print(node3)

main()
