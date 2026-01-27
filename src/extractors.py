import re

def extract_markdown_images(text):
    # Use the negation operator [^] to match anything but what's inside
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # Make sure that the link doesn't start with an "!"
    # Use the negation operator [^] to match anything but what's inside
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(markdown):
    # Match the "#" and any number of spaces, and the text
    match = re.search(r"^#\s*(.*)", markdown)
    if not match:
        raise Exception ("You need to have a `h1` header in the markdown")
    else:
        return match.group(1)
