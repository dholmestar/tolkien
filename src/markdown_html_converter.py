from htmlnode import ParentNode # type: ignore
from markdown_blocks import ( # type: ignore
    markdown_to_blocks,
    block_to_block_type,
    BLOCK_TYPE_PARAGRAPH,
)
from inline_markdown import text_to_textnodes, text_node_to_html_node # type: ignore
from textnode import TextNode, TextType # type: ignore


def _text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def _paragraph_block_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", _text_to_children(text))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BLOCK_TYPE_PARAGRAPH:
            node = _paragraph_block_to_html_node(block)
        else:
            node = _paragraph_block_to_html_node(block)

        children.append(node)

    return ParentNode("div", children)