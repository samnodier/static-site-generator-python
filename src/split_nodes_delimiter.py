from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        splitted_node = node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise Exception("Invalid Markdown Syntax: Delimiter not matched")
        for i in range(len(splitted_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(splitted_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splitted_node[i], text_type))
    return new_nodes
