from text_node import TextNode, TextType
import re 

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

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