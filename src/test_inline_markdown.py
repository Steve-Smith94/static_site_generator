import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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


#split node tests
class TestSplitNodesImagesAndLinks(unittest.TestCase):
    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("no images here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("no images here", TextType.TEXT)], new_nodes)

    def test_split_images_only_image(self):
        node = TextNode("![alt](http://x/y.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "http://x/y.png")],
            new_nodes,
        )

    def test_split_images_preserve_non_text_nodes(self):
        nodes = [
            TextNode("start ![a](u)", TextType.TEXT),
            TextNode("already link", TextType.LINK, "http://boot.dev"),
            TextNode("already image", TextType.IMAGE, "http://img"),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0], TextNode("start ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("a", TextType.IMAGE, "u"))
        self.assertEqual(new_nodes[2], nodes[1])
        self.assertEqual(new_nodes[3], nodes[2])

    def test_split_images_adjacent(self):
        node = TextNode("![a](u1)![b](u2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode("b", TextType.IMAGE, "u2"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "link to [boot dev](https://www.boot.dev) and [yt](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("yt", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("no links here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("no links here", TextType.TEXT)], new_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[text](http://x)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("text", TextType.LINK, "http://x")],
            new_nodes,
        )

    def test_split_links_preserve_non_text_nodes(self):
        nodes = [
            TextNode("[a](u)", TextType.TEXT),
            TextNode("plain", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://img"),
        ]
        new_nodes = split_nodes_link(nodes)
        # Expect link node from first, plain preserved, image preserved
        self.assertEqual(new_nodes[0], TextNode("a", TextType.LINK, "u"))
        self.assertEqual(new_nodes[1], TextNode("plain", TextType.TEXT))
        self.assertEqual(new_nodes[2], nodes[2])

    def test_split_links_adjacent(self):
        node = TextNode("[a](u1)[b](u2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "u1"),
                TextNode("b", TextType.LINK, "u2"),
            ],
            new_nodes,
        )

    def test_split_mix_run_images_then_links(self):
        node = TextNode(
            "t ![img](u) and [link](v) end",
            TextType.TEXT,
        )
        after_images = split_nodes_image([node])
        # Then run links on result
        final = split_nodes_link(after_images)
        self.assertListEqual(
            [
                TextNode("t ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "u"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "v"),
                TextNode(" end", TextType.TEXT),
            ],
            final,
        )

#text to text node tests
class TestTextToTextNodes(unittest.TestCase):
    
    def test_simple_text(self):
        # Test with just plain text
        result = text_to_textnodes("Hello world")
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_bold_only(self):
        # Test with just bold text
        result = text_to_textnodes("**bold**")
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(result, expected)
    
    def test_italic_only(self):
        # Test with just italic text
        result = text_to_textnodes("_italic_")
        expected = [TextNode("italic", TextType.ITALIC)]
        self.assertEqual(result, expected)
    
    def test_code_only(self):
        # Test with just code text
        result = text_to_textnodes("`code`")
        expected = [TextNode("code", TextType.CODE)]
        self.assertEqual(result, expected)
    
    def test_mixed_formatting(self):
        # Test with multiple formatting types
        result = text_to_textnodes("This is **bold** and _italic_ text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_with_code_block(self):
        # Test including code blocks
        result = text_to_textnodes("Text with `code block` here")
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_with_image(self):
        # Test with an image
        result = text_to_textnodes("Here's an ![alt text](https://example.com/image.jpg)")
        expected = [
            TextNode("Here's an ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(result, expected)
    
    def test_with_link(self):
        # Test with a link
        result = text_to_textnodes("Visit [Boot.dev](https://boot.dev) today")
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" today", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    
    def test_complex_example(self):
        # Test the exact example from the assignment
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        result = text_to_textnodes("")
        expected = []  
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()