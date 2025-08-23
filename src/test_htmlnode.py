import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_node import TextNode, TextType
from main import text_node_to_html_node

# Test class for HTMLNode
class TestHTMLNode(unittest.TestCase):
    # Test HTMLNode.props_to_html with no props
    def test_props_to_html_no_props(self):
        # Create an HTMLNode with no props (default)
        node = HTMLNode()
        # props_to_html should return an empty string when there are no props
        self.assertEqual(node.props_to_html(), "")

    # Test HTMLNode.props_to_html with one prop
    def test_props_to_html_one_prop(self):
        # Create an HTMLNode with one property (e.g. href)
        node = HTMLNode(props={"href": "https://www.google.com"})
        # props_to_html should return the properly formatted property string
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    # Test HTMLNode.props_to_html with multiple props
    def test_props_to_html_multiple_props(self):
        # Create a node with multiple properties
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        # props_to_html returns all properties as a string;
        # The order of the props is not guaranteed in a dictionary,
        # check that both substrings are present instead of the exact order
        output = node.props_to_html()
        self.assertIn('href="https://www.google.com"', output)
        self.assertIn('target="_blank"', output)

# Test class for LeafNode
class TestLeafNode(unittest.TestCase):
    # Test rendering a single paragraph tag leaf
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Test rendering an anchor tag leaf with an attribute
    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    # Test rendering a leaf node with no tag (just raw text)
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

class Test_node_to_html_node(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("Go to Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Go to Boot.dev")
        self.assertDictEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_text_image(self):
        node = TextNode("A beautiful sunset", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertDictEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "A beautiful sunset"})

    def test_unsupported_type_raises_exception(self):
        class UnknownTextType: # A dummy class to represent an unknown type
            pass
        
        node = TextNode("Unknown text", UnknownTextType()) 
        
        with self.assertRaises(Exception) as cm: # You used Exception, so we check for that
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
    