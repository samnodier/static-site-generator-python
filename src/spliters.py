from extractors import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # grab the node text to use throughout the function without modifying the node
        node_text = node.text
        if not node_text:
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            splitted_node = node_text.split(delimiter)
            # if the delimiters do not match.
            # Because if you have an odd number of delimiters you will get even len of the list
            if len(splitted_node) % 2 == 0:
                raise Exception("Invalid Markdown Syntax: Delimiter not matched")
            for i in range(len(splitted_node)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted_node[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted_node[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # grab the node text to use throughout the function without modifying the node
        node_text = node.text
        # if the node text is empty
        if not node_text:
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            image_matches = extract_markdown_images(node_text)
            if len(image_matches) == 0:
                new_nodes.append(node)
            else:
                for i in range(len(image_matches)):
                    match = image_matches[i]
                    # split the text based on the match that was found
                    sections = node_text.split(f"![{match[0]}]({match[1]})", 1)
                    # if there was text before the image
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
                    if sections[1]:
                        node_text = sections[1]
                        if i + 1 == len(image_matches):
                            # we got to the end of the string there's still more text type available
                            # add it as a text node
                            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # grab the node text to use throughout the function without modifying the node
        node_text = node.text
        # if the text node is empty, do nothing
        if not node_text:
            continue
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            image_matches = extract_markdown_links(node_text)
            if len(image_matches) == 0:
                new_nodes.append(node)
            else:
                for i in range(len(image_matches)):
                    match = image_matches[i]
                    sections = node_text.split(f"[{match[0]}]({match[1]})", 1)
                    # if there was text before the link
                    if sections[0]:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                    # add the link node
                    new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
                    if sections[1]:
                        node_text = sections[1]
                        if i + 1 == len(image_matches):
                            # we got to the end of the string there's still more text type available
                            # add it as a text node
                            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


# Bundle everything together
# Split any type of text
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    bold_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes


def markdown_to_blocks(markdown):
    blocks = []  # Create a list to return all MD blocks
    line_blocks = markdown.split("\n\n")
    for line in line_blocks:
        # If the length of a stripped line is greater than 0 i.e. the line is not empty
        # This checks for "\n" lines as well
        if len(line.strip()) > 0:
            sublist = []
            for subline in line.strip().split("\n"):
                sublist.append(subline.strip())
            blocks.append("\n".join(sublist))
    return blocks
