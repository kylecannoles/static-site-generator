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
    def test_invalid_text_type(self):
        node = TextNode("This is an invalid text node", TextType.TEXT)
        node.text_type = "invalid"
        self.assertRaises(Exception, TextNode.text_node_to_html_node, node)
    def test_textnode_to_html_text(self):
        node = TextNode("This is a normal text html node", TextType.TEXT)
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),"This is a normal text html node")
    def test_textnode_to_html_bold(self):
        node = TextNode("This is a bold html node", TextType.BOLD)
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),"<b>This is a bold html node</b>")
    def test_textnode_to_html_italic(self):
        node = TextNode("This is an italic html node", TextType.ITALIC)
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),"<i>This is an italic html node</i>")
    def test_textnode_to_html_code(self):
        node = TextNode("This is a code html node", TextType.CODE)
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),"<code>This is a code html node</code>")
    def test_textnode_to_html_link(self):
        node = TextNode("This is an html link node", TextType.LINK, "https://google.com")
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),'<a href="https://google.com">This is an html link node</a>')
    def test_textnode_to_html_image(self):
        node = TextNode("This is an image html node", TextType.IMAGE, "https://imgur.com")
        self.assertEqual(TextNode.text_node_to_html_node(node).to_html(),'<img src="https://imgur.com" alt="This is an image html node">')

if __name__ == "__main__":
    unittest.main()
