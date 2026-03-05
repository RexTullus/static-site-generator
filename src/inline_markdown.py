import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            output.append(old_node)
            continue

        new_nodes = []
        blocks = old_node.text.split(delimiter)
        
        if not len(blocks) % 2:
            raise ValueError("Invalid markdown")

        for i in range(len(blocks)):            
            if i % 2 == 0:
                if blocks[i]:
                    new_nodes.append(TextNode(blocks[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(blocks[i], text_type))
        output.extend(new_nodes)
    return output

def split_nodes_image(old_nodes):
    output = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            output.append(old_node)
            continue
        
        new_nodes = []
        images = extract_markdown_images(old_node.text)
       
        remaining_text = old_node.text
        for image_alt, image_url in images:
            pattern = f"![{image_alt}]({image_url})"
            text_sections = remaining_text.split(pattern, 1)

            if len(text_sections) != 2:
                raise ValueError("invalid markdown, section not closed")
        
            if text_sections[0] != "":
                new_nodes.append(TextNode(text_sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

            remaining_text = text_sections[1]

        output.extend(new_nodes)
        if remaining_text != "":
            output.append(TextNode(remaining_text, TextType.TEXT))

    return output

def split_nodes_link(old_nodes):
    output = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            output.append(old_node)
            continue
        
        new_nodes = []
        links = extract_markdown_links(old_node.text)
       
        remaining_text = old_node.text
        for link_text, link_url in links:
            pattern = f"[{link_text}]({link_url})"
            text_sections = remaining_text.split(pattern, 1)

            if len(text_sections) != 2:
                raise ValueError("invalid markdown, section not closed")
        
            if text_sections[0] != "":
                new_nodes.append(TextNode(text_sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            remaining_text = text_sections[1]

        output.extend(new_nodes)
        if remaining_text != "":
            output.append(TextNode(remaining_text, TextType.TEXT))

    return output

def extract_markdown_images(text):
    pattern = r"!\[(\w.*?)\]\((\w.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[(\w.*?)\]\((\w.*?)\)"
    return re.findall(pattern, text)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        if block != "":
            blocks.append(block.strip())

    return blocks
    