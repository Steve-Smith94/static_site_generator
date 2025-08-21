

class HTMLNode():
    
    def __init__(self, tag = None, value = None, children = None, props = None):
        # Store the HTML tag name (like "p", "a", "div", etc.)
        self.tag = tag
        # Store the text content inside the tag
        self.value = value  
        # Store a list of child HTMLNode objects (for nested HTML)
        self.children = children
        # Store a dictionary of HTML attributes (like {"href": "google.com"})
        self.props = props

    # This method will be overridden by child classes to actually generate HTML
    def to_html(self):
        # Raise an error since this base class doesn't know how to render HTML
        raise NotImplementedError
    
    # This method converts the props dictionary into HTML attribute strings
    def props_to_html(self):
        # If there are no props, return empty string
        if not self.props:
            return ""
        
        # Build up the attribute string piece by piece
        pairs = ""
        for key in self.props:
            # For each key-value pair, create " key=\"value\""
            result_string = f" {key}=\"{self.props[key]}\""
            # Add this piece to our final result
            pairs += result_string
        # Return the complete attribute string
        return pairs
        
    # This method defines how the object looks when printed (for debugging)
    def __repr__(self):
        # Return a string showing all the object's data
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
    # Initialize the parent HTMLNode with tag, value, no children, and optional props    
        super().__init__(tag, value, None, props)

# Render the leaf node as an HTML string
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        
        # If the tag is None, it's just raw text (not wrapped in any HTML tag)
        elif self.tag == None:
            return self.value
        
        # Otherwise, build the HTML string: <tag props>value</tag>
        # self.props_to_html() returns the attributes or an empty string
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
