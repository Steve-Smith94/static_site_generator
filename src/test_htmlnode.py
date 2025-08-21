import unittest
from htmlnode import HTMLNode, LeafNode  

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
        # so we'll check that both substrings are present instead of the exact order
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


if __name__ == "__main__":
    unittest.main()
    