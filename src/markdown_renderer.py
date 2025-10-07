from htmlnode import ParentNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes, text_nodes_to_html_nodes

def markdown_to_html_node(markdown):
    parent = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown.strip())
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            stripped = block.lstrip()
            hashes, rest = 0, stripped
            while hashes < len(rest) and rest[hashes] == "#":
                hashes += 1
            text = rest[hashes:].strip()
            level = hashes
            if 1 <= level <= 6:
                tnodes = text_to_textnodes(text)
                children = text_nodes_to_html_nodes(tnodes)
                parent.children.append(ParentNode(f"h{level}", children))
                continue  

        s = block.lstrip()
        if s.startswith("# "):
            text = s[2:].strip()
            tnodes = text_to_textnodes(text)
            children = text_nodes_to_html_nodes(tnodes)
            parent.children.append(ParentNode("h1", children))
            continue

       
        s = block.lstrip()
        if s.startswith(">"):
            parts = []
            for ln in block.splitlines():
                t = ln.lstrip()
                if t.startswith(">"):
                    parts.append(t[1:].lstrip())
            text = " ".join([p for p in parts if p])
            tnodes = text_to_textnodes(text)
            children = text_nodes_to_html_nodes(tnodes)
            parent.children.append(ParentNode("blockquote", children))
            continue
        
        if btype == BlockType.PARAGRAPH:
            lines = [ln.strip() for ln in block.splitlines()]
            text = " ".join([ln for ln in lines if ln])
            tnodes = text_to_textnodes(text)
            children = text_nodes_to_html_nodes(tnodes)
            parent.children.append(ParentNode("p", children))
        
        if btype == BlockType.UNORDERED_LIST:
            items = []
            for ln in block.splitlines():
                s = ln.strip()
                if s.startswith("- "):
                    text = s[2:].strip()
                    tnodes = text_to_textnodes(text)
                    children = text_nodes_to_html_nodes(tnodes)
                    items.append(ParentNode("li", children))
            parent.children.append(ParentNode("ul", items))
            continue

        if btype == BlockType.ORDERED_LIST:
            items = []
            for ln in block.splitlines():
                s = ln.strip()
                # find "N. " prefix
                if "." in s and s.split(".", 1)[0].isdigit():
                    text = s.split(".", 1)[1].strip()
                    tnodes = text_to_textnodes(text)
                    children = text_nodes_to_html_nodes(tnodes)
                    items.append(ParentNode("li", children))
            parent.children.append(ParentNode("ol", items))
            continue
    return parent