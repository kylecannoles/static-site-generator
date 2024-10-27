import unittest

from textnode import TextNode, TextType
from mdparser import split_nodes_delimiter

class TestInline(unittest.TestCase):
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
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)
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

