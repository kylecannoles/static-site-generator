import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    # test 0 children
    def test_zero_children(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)
    # test 1 child
    def test_one_child(self):
        node = ParentNode("p", [LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p>Normal text</p>")
    # test 2 children
    def test_two_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text</p>")
    # test 3 children
    def test_three_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "Italic text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i></p>")
    # test 1 child w/ nested child
    def test_parent_of_parent(self):
        node = ParentNode("h1", [ParentNode("p", [LeafNode(None, "Title text")]), LeafNode("i", "Italic text")])
        self.assertEqual(node.to_html(), "<h1><p>Title text</p><i>Italic text</i></h1>")
    # test 1 parent w/ nested parent (parent->parent->parent->child)
    def test_parent_parent_parent(self):
        node = ParentNode("h1", [ParentNode("h2", [ParentNode("h3", [LeafNode(None, "Nested text")])]), LeafNode("i", "Italic text")])
        self.assertEqual(node.to_html(), "<h1><h2><h3>Nested text</h3></h2><i>Italic text</i></h1>")
