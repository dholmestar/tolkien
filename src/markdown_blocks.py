from enum import Enum
from .htmlnode import ParentNode  # type: ignore
from .inline_markdown import text_to_textnodes  # type: ignore
from .textnode import TextNode, TextType, text_node_to_html_node  # type: ignore


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    stripped_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        else:
            stripped_blocks.append(stripped_block)
    
    return stripped_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            prefix = f"{i}. "
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_block_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_block_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    level = max(1, min(level, 6))
    text = block[level:].strip()
    tag = f"h{level}"
    return ParentNode(tag, text_to_children(text))


def code_block_to_html_node(block):
    lines = block.split("\n")

    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]

    code_text = "\n".join(lines) + "\n"

    text_node = TextNode(code_text, TextType.TEXT)
    code_child = text_node_to_html_node(text_node)
    return ParentNode("pre", [code_child])


def quote_block_to_html_node(block):
    lines = block.split("\n")
    stripped = [line.lstrip(">").strip() for line in lines]
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:].strip()  # remove "- "
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        # remove "1. ", "2. ", etc.
        text = line.split(". ", 1)[1].strip()
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = paragraph_block_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_block_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_block_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_block_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_block_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_block_to_html_node(block)
        else:
            node = paragraph_block_to_html_node(block)

        children.append(node)

    return ParentNode("div", children)