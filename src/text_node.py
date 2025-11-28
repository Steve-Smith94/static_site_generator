from enum import Enum
from htmlnode import HTMLNode


class TextType(Enum):
    TEXT = "text"      # Plain text
    BOLD = "bold"      # Bold text (e.g., **Bold**)
    ITALIC = "italic"  # Italic text (e.g., _Italic_)
    CODE = "code"      # Inline code (e.g., `Code`)
    LINK = "link"      # A link (e.g., [text](url))
    IMAGE = "image"    # An image (e.g., ![alt](url))


class TextNode():
    def __init__(self, text, text_type, url=None):
    # Represents a piece of inline text and its type, with an optional URL for links/images
        self.text = text                # The actual text content
        self.text_type = text_type      # The kind of text (from TextType enum)
        self.url = url                  # URL if this node is a link or image, else None


    def __eq__(self, other):
    # Equality: all properties (text, type, and URL) must be the same
        return all([
        self.text == other.text, 
        self.text_type == other.text_type,
        self.url == other.url,
    ])


    def __repr__(self):
    # For debugging/printing: show a readable summary of this TextNode
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    

        


