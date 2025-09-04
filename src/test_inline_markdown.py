import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links 
from text_node import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_multiple_same(self):
        node = TextNode("**bold1** and **bold2** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This has unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)




    # image extraction tests
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_markdown_images_multiple(self):
        text = "![a](http://a.com/x.png) and ![b cat](https://b.org/y.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("a", "http://a.com/x.png"), ("b cat", "https://b.org/y.jpg")],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("no images here, only text")
        self.assertListEqual([], matches)
        

    # link extraction tests
    def test_extract_markdown_links_single(self):
        text = "Go [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "See [Docs](https://docs.example.com) and [Repo](https://github.com/x)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("Docs", "https://docs.example.com"), ("Repo", "https://github.com/x")],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "![alt](https://img.com/x.png) plus [site](https://site.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("site", "https://site.com")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("plain text no links")
        self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()