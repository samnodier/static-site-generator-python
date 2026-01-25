from blocknode import BlockType


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HDNG
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QOTE
    elif block.startswith("- ") or block.startswith("* "):
        return BlockType.UNDL
    elif block.startswith("1. "):
        return BlockType.ORDL
    else:
        return BlockType.PARA
