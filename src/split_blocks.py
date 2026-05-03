from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ",)):
        return BlockType.HEADING
    if block.startswith(("```\n")) and block.endswith(("```")):
        return BlockType.CODE
    if block.startswith(">"):
        items = block.split("\n")
        condtion = True
        for item in items:
            if not item.startswith(">"):
                condtion = False
        if condtion:
            return BlockType.QUOTE
    if block.startswith("- "):
        items = block.split("\n")
        condtion = True
        for item in items:
            if not item.startswith("- "):
                condtion = False
        if condtion:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        items = block.split("\n")
        condtion = True
        n = 1
        for item in items:
            if not item.startswith(f"{n}. "):
                condtion = False
            n += 1
        if condtion:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if len(block) > 0:
            clean_blocks.append(block.strip())
    return clean_blocks

