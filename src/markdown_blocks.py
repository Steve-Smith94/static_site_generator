from enum import Enum 


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block: str) -> BlockType:
    # code block: starts and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # heading: 1–6 '#' then a space
    if block and block[0] == "#":
        i = 0
        while i < len(block) and block[i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(block) and block[i] == " ":
            return BlockType.HEADING

    # quote: every line starts with '>'
    lines = block.splitlines()
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # unordered list: every line starts with '- '
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ordered list: lines start with '1. ', '2. ', ... incrementing
    if lines:
        ok = True
        for i, line in enumerate(lines, start=1):
            prefix = f"{i}. "
            if not line.startswith(prefix):
                ok = False
                break
        if ok:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH



def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for piece in blocks:
        stripped = piece.strip()
        if stripped != "":
            cleaned_blocks.append(stripped)
    return cleaned_blocks



