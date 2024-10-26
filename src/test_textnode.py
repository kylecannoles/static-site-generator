import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(None, node.url)
    def test_texttype_property_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(TextType.ITALIC.value, node.text_type)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
        self.assertEqual("TextNode(This is a text node, bold, https://google.com)", str(node))

if __name__ == "__main__":
    unittest.main()
