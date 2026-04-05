from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    QUOTE = 'quote'
    CODE = 'code'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    block_strings = []
    split_markdown = markdown.split('\n\n')
    for block in split_markdown:
        # Not including empty blocks
        if block.strip() == '':
            continue
        block_strings.append(block.strip())

    return block_strings

def block_to_block_type(block):
    # Default type
    block_type = BlockType.PARAGRAPH
    if len(block) == 0:
        raise Exception('block is empty, must contain a string to determine block_type')
    
    if block.startswith('#'):
        # Check if meets heading requirements
        prefix = block.split(" ")[0] 
        if len(prefix) <= 6 and len(prefix.lstrip('#')) == 0:
            block_type = BlockType.HEADING

    if block.startswith('`') and block.endswith('`'):
        prefix = block.split("\n")[0]
        suffix = block.split("\n")[-1]
        if len(prefix) == 3 and len(suffix) == 3:
            block_type = BlockType.CODE 

    if block.startswith('>'):
        # Check every line make sure it starts with '>'
        is_quote = True
        for line in block.split('\n'):
            if not line.startswith('>'):
                is_quote = False
        if is_quote:
            block_type= BlockType.QUOTE

    if block.startswith('- '):
        # Check every line make sure it starts with '- '
        is_unordered = True
        for line in block.split('\n'):
            if not line.startswith('- '):
                is_quote = False
        if is_unordered:
            block_type= BlockType.UNORDERED_LIST
        
    if block.startswith('1. '):
        # Check every line make sure it's ordered
        lines = block.split('\n')
        is_ordered = True
        for i in range(0, len(lines)):
            if not lines[i].startswith(f'{i + 1}. '):
                is_ordered = False
        if is_ordered:
            block_type = BlockType.ORDERED_LIST
    return block_type