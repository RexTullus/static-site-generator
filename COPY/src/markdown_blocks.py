from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        if block != "":
            blocks.append(block.strip())

    return blocks

def block_to_block_type(block):
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith(("* ", "- ")) for line in block.split("\n")):
        return BlockType.ULIST
    elif all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == idx + 1 for idx, line in enumerate(block.split("\n"))):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def paragraph_to_html_node(block):
    paragraph = " ".join((block.split("\n")))
    return ParentNode("p", text_to_children(paragraph))

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = TextNode(block[4:-3], TextType.TEXT)
    text = text_node_to_html_node(text)
    code = ParentNode("code", [text])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith("-"):
            raise ValueError("invalid ulist block")
        children = text_to_children(line[2:])
        new_lines.append(ParentNode("li", children))
    return ParentNode("ul", new_lines)

def olist_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line or not line[0].isdigit():
            raise ValueError("invalid olist block")
        children = text_to_children(line.split(". ", 1)[1])
        new_lines.append(ParentNode("li", children))
    return ParentNode("ol", new_lines)

def text_to_children(text):
    HTMLNodes = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        HTMLNodes.append(text_node_to_html_node(node))
    return HTMLNodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html = []
    for block in blocks:
        html.append(block_to_html_node(block))
    return ParentNode("div", html)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLISTLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

