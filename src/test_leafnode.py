import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_empty_value(self):
        node = LeafNode("b", None)
        self.assertRaises(ValueError, node.to_html)
    def test_empty_tag(self):
        node = LeafNode(None, "Normal text")
        self.assertEqual(node.to_html(), "Normal text")

if __name__ == "__main__":
    unittest.main()
