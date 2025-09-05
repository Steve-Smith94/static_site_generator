import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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


if __name__ == "__main__":
    unittest.main()