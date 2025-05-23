from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_htmlnode(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        nodes.append(block_to_htmlnode(block))

    return ParentNode("div", children=nodes)


def block_to_htmlnode(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_node(block)
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return list_block_to_html_node(
                block, BlockType.UNORDERED_LIST)
        case BlockType.ORDERED_LIST:
            return list_block_to_html_node(
                block, BlockType.ORDERED_LIST)
        case _:
            raise ValueError("invalid block type")


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    text = ' '.join(block.split("\n"))
    return ParentNode("p", children=text_to_children(text))


def heading_block_to_html_node(block: str) -> HTMLNode:
    # TODO: this assumes a single line, consider multiline case
    hashes, text = block.split(" ", 1)
    level = len(hashes)
    if level > 6:
        raise ValueError(f"invalid heading value: {level}")
    return ParentNode(f"h{level}", children=text_to_children(text))


def code_block_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block.strip("```").lstrip()
    code_node = ParentNode("code", children=[LeafNode(None, text)])
    return ParentNode("pre", children=[code_node])


def quote_block_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        clean_lines.append(line.lstrip(">").strip())
    text = " ".join(clean_lines)
    return ParentNode("blockquote", children=text_to_children(text))


def list_block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        _, text = line.split(" ", 1)
        list_items.append(ParentNode("li", children=text_to_children(text)))
    match block_type:
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", children=list_items)
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", children=list_items)


def text_to_children(text) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))
