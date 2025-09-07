

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for piece in blocks:
        stripped = piece.strip()
        if stripped != "":
            cleaned_blocks.append(stripped)
    return cleaned_blocks
