
from enum import Enum
import re


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING= "heading"
    CODE= "code"
    QUOTE= "quote"
    UNORDERED_LIST= "unordered_list"
    ORDERED_LIST= "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.fullmatch(r"#{1,6} .+", block):
        return BlockType.HEADING

    if re.fullmatch(r"```\n[\s\S]*\n```", block):
        return BlockType.CODE

    if re.fullmatch(r">[^\n]*(\n>[^\n]*)*", block):
        return BlockType.QUOTE

    if re.fullmatch(r"- [^\n]+(\n- [^\n]+)*", block):
        return BlockType.UNORDERED_LIST

    lines = block.split("\n")
    if all(
        re.fullmatch(rf"{i}\. .+", line)
        for i, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
