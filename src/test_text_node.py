import unittest

from text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2) 

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_and_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("shigella migella tigella figurella", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_same_text_different_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        node2 = TextNode("Click here", TextType.LINK, "https://www.example.com")
        self.assertNotEqual(node, node2)
    

if __name__ == "__main__":
    unittest.main()