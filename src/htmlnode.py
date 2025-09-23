
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def to_html(self):
        raise NotImplementedError

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value or ""
        if self.tag == "img":
            return f'<img{self.props_to_html()}>'
        if self.value is None:
            raise ValueError("LeafNode must have a value unless tag is 'img'")
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children")
        inner = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>'



        
