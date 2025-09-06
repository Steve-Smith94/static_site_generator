from text_node import TextNode, TextType
import re 

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        while True:
            pairs = extract_markdown_images(remaining)
            if not pairs:
                break
            alt, url = pairs[0]
            snippet = f"![{alt}]({url})"
            left, right = remaining.split(snippet, 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = right

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        while True:
            pairs = extract_markdown_links(remaining)
            if not pairs:
                break
            text, url = pairs[0]
            snippet = f"[{text}]({url})"
            left, right = remaining.split(snippet, 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining = right

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:   
            if delimiter not in old_node.text:
                new_nodes.append(old_node) 
            else:
                parts = old_node.text.split(delimiter)
                if len(parts) % 2 == 0:  # Check ONCE after splitting
                    raise Exception("Invalid markdown syntax: unmatched delimiter")
                for i in range(len(parts)):
                    if parts[i]:
                        if i % 2 == 0: 
                            new_node = TextNode(parts[i], TextType.TEXT)
                            new_nodes.append(new_node)
                        else:  
                            new_node = TextNode(parts[i], text_type)
                            new_nodes.append(new_node)
         

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes 