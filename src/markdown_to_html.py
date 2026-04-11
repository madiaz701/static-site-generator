from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from markdown import text_to_textnodes
from conversion import text_node_to_html_node
from blocks import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):
    full_html = ParentNode('div', [])
    body_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.HEADING:
                # Figure out true heading 1-6
                heading_number = len(block.split(' ')[0])
                body_nodes.append(ParentNode(f'h{heading_number}', text_to_children(block.split(' ', 1)[1].strip('\n'))))
            case BlockType.PARAGRAPH:
                body_nodes.append(ParentNode('p', text_to_children(block.replace('\n', ' '))))
            case BlockType.QUOTE:
                lines = []
                # Strip the '>' from the beginning of each line
                for line in block.split('\n'):
                    if line.startswith('> '):
                        lines.append(line.split('> ', 1)[1])
                    else:
                        lines.append(line.split('>')[1])
                clean_text = '\n'.join(lines)
                body_nodes.append(ParentNode('blockquote', text_to_children(clean_text)))
            case BlockType.UNORDERED_LIST:
                list_items = []
                for line in block.split('\n'):
                    list_items.append(ParentNode('li', text_to_children(line.split('- ', 1)[1])))
                body_nodes.append(ParentNode('ul', list_items))
            case BlockType.ORDERED_LIST:
                list_items = []
                for line in block.split('\n'):
                    list_items.append(ParentNode('li', text_to_children(line.split('. ', 1)[1])))
                body_nodes.append(ParentNode('ol', list_items))
            case BlockType.CODE:
                code_html = text_node_to_html_node(TextNode(block.split('```', 1)[1].rsplit('```', 1)[0].lstrip('\n'), TextType.CODE))
                body_nodes.append(ParentNode('pre', [code_html]))

                
        
    full_html.children.extend(body_nodes)
    
    return full_html

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
