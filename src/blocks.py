
def markdown_to_blocks(markdown):
    block_strings = []
    split_markdown = markdown.split('\n\n')
    for block in split_markdown:
        # Not including empty blocks
        if block.strip() == '':
            continue
        block_strings.append(block.strip())

    return block_strings