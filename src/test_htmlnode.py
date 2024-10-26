import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "", None, {"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')
    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")
    def test_child(self):
        node = HTMLNode("p", None, [HTMLNode("b", "test", None, None)], None)
        self.assertEqual(str(node.children[0]), 'HTMLNode(b, test, None, None)')

if __name__ == "__main__":
    unittest.main()
