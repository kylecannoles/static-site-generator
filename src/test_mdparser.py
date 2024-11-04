import unittest

from textnode import TextNode, TextType
from mdparser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestMDParser(unittest.TestCase):
    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])
    def test_bold_delimiter(self):
        node = TextNode("This is *text with* bold letters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT), TextNode("text with", TextType.BOLD), TextNode(" bold letters", TextType.TEXT),])
    def test_italic_delimiter(self):
        node = TextNode("This is **text with italic** letters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT), TextNode("text with italic", TextType.ITALIC), TextNode(" letters", TextType.TEXT),])
    def test_left_delimiter(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])
    def test_right_delimiter(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE),])
    def test_missing_delimiter(self):
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a code block word", TextType.TEXT),])
    def test_missing_two_delimiters(self):
        node = TextNode("This is text with a code block` word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
    def test_one_delimiter_end(self):
        node = TextNode("This is text with a code block`", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
    def test_one_delimiter_start(self):
        node = TextNode("`", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
    def test_none_text(self):
        node = TextNode(None, TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_multiple_nodes(self):
        node_one = TextNode("Node one with a `code block` word", TextType.TEXT)
        node_two = TextNode("Node two with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_one, node_two], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Node one with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT), TextNode("Node two with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))
    def test_extract_markdown_images_parse_error(self):
        text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))
    def test_prevent_extract_md_images_as_links(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([], extract_markdown_links(text))
    def test_extract_md_links_first_char(self):
        text = "[to boot dev](https://www.boot.dev) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("to boot dev", "https://www.boot.dev")], extract_markdown_links(text))

    def test_split_nodes_image(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ], new_nodes)
    def test_empty_node_image(self):
        node = TextNode("This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan]https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif) and ![obi wan]https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
            ], new_nodes)
    def test_start_node_image(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ], new_nodes)
    def test_one_node_image(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            ], new_nodes)
    def test_text_after_node_image(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            ], new_nodes)


    def test_one_node_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ], new_nodes)
    def test_two_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)
    def test_empty_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev(https://www.boot.dev) and [to youtube]https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("This is text with a link [to boot dev(https://www.boot.dev) and [to youtube]https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ], new_nodes)
    def test_text_after_node_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and ", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            ], new_nodes)
    def test_star_node_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ], new_nodes)

