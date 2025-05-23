from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block) -> BlockType:
    # TODO: modify this to handle syntax error cases
    # e.g. headings with too many hashes, ordered lists
    # with incorrect numbers, etc.
    lines = block.split("\n")

    if re.match("(?m)^#{1,6} .*", block):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        current_number = 1
        for line in lines:
            if not line.startswith(f"{current_number}. "):
                return BlockType.PARAGRAPH
            current_number += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []

    raw_blocks = markdown.split("\n\n")  # split on extra whitespace

    for raw_block in raw_blocks:
        raw_block = raw_block.strip()
        if len(raw_block) == 0:
            continue
        blocks.append(raw_block)

    return blocks
