from enum import Enum

class BlockType(Enum):
    PARA = "paragraph"
    HDNG = "heading"
    CODE = "code"
    QOTE = "quote"
    UNDL = "unordered_list"
    ORDL = "ordered list"
