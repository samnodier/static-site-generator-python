import re

def extract_markdown_images(text):
    # Use the negation operator [^] to match anything but what's inside
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # Make sure that the link doesn't start with an "!"
    # Use the negation operator [^] to match anything but what's inside
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
