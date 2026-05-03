def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if len(block) > 0:
            clean_blocks.append(block.strip())
    return clean_blocks

