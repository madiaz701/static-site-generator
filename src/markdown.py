import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_node_list.append(node)
        elif len(node.text.split(delimiter)) % 2 == 0:
            raise Exception(f'{node} has invalid Markdown syntax')
        else:
            split_text_list = node.text.split(delimiter)
            for i, chunk in enumerate(split_text_list):
                if chunk == '':
                    continue
                if i % 2 == 0:
                    # plain text
                    new_node_list.append(TextNode(chunk, TextType.PLAIN))
                else:
                    # delimited text_type
                    new_node_list.append(TextNode(chunk, text_type))
    return new_node_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_node_list = []
    for node in old_nodes:
        remaining_text = node.text
        images = extract_markdown_images(node.text)
        
        if len(images) == 0:
            new_node_list.append(node)
            continue
        
        for alt, url in images:
            # split remaining_text on this specific image's markdown syntax
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            # sections[0] is text BEFORE this image
            # add it as PLAIN if not empty
            if sections[0] != '':
                new_node_list.append(TextNode(sections[0], TextType.PLAIN))
            
            # add the IMAGE node
            new_node_list.append(TextNode(alt, TextType.IMAGE, url))
            
            # sections[1] is everything AFTER — assign it back to remaining_text
            remaining_text = sections[1]
        
        # after the loop, anything left in remaining_text is trailing plain text
        # add it if not empty
        if remaining_text != '':
            new_node_list.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_node_list

def split_nodes_link(old_nodes):
    new_node_list = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(node.text)
        
        if len(links) == 0:
            new_node_list.append(node)
            continue
        
        for alt, url in links:
            # split remaining_text on this specific link's markdown syntax
            sections = remaining_text.split(f"[{alt}]({url})", 1)
            # sections[0] is text BEFORE this link
            # add it as PLAIN if not empty
            if sections[0] != '':
                new_node_list.append(TextNode(sections[0], TextType.PLAIN))
            
            # add the LINK node
            new_node_list.append(TextNode(alt, TextType.LINK, url))
            
            # sections[1] is everything AFTER — assign it back to remaining_text
            remaining_text = sections[1]
        
        # after the loop, anything left in remaining_text is trailing plain text
        # add it if not empty
        if remaining_text != '':
            new_node_list.append(TextNode(remaining_text, TextType.PLAIN))
    
    return new_node_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
