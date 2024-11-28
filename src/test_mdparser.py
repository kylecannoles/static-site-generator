import unittest

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from mdparser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type, parse_heading, parse_code, parse_quote, parse_ul, parse_ol, markdown_to_html_node

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

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
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
        ], new_nodes)
    def test_text_to_textnodes_reversed(self):
        text = "[link](https://boot.dev) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and an `code block` word and a *italic* with an **text**This is "
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with an ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode("This is ", TextType.TEXT),
        ], new_nodes)
    def test_text_to_textnodes_text_only(self):
        text = "This is basic text" 
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is basic text", TextType.TEXT),
        ], new_nodes)
    def test_text_to_textnodes_bold_only(self):
        text = "**This is bold text**" 
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is bold text", TextType.BOLD),
        ], new_nodes)
    def test_text_to_textnodes_italic_only(self):
        text = "*This is italic text*" 
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is italic text", TextType.ITALIC),
        ], new_nodes)
    def test_text_to_textnodes_image_only(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)" 
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ], new_nodes)
    def test_text_to_textnodes_link_only(self):
        text = "[link](https://boot.dev)" 
        new_nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], new_nodes)

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading
     
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
    
* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertEqual(["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", """* This is the first list item in a list block
* This is a list item
* This is another list item"""], markdown_to_blocks(markdown))

    def test_block_to_block_type_heading(self):
        md_block = "# Big Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(md_block))
    def test_block_to_block_type_code(self):
        md_block = '```\nprint("What is the answer to the universe")\nprint(42)\n```'
        self.assertEqual(BlockType.CODE, block_to_block_type(md_block))
    def test_block_to_block_type_quote(self):
        md_block = '> The best time to plant a tree was 20 years ago.\n> The second best time is now.'
        self.assertEqual(BlockType.QUOTE, block_to_block_type(md_block))
    def test_block_to_block_type_unordered_list(self):
        md_block = '- Eggs\n- Milk\n- Flour'
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md_block))
    def test_block_to_block_type_unordered_list_2(self):
        md_block = '* Eggs\n* Milk\n* Flour'
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(md_block))
    def test_block_to_block_type_ordered_list(self):
        md_block = '1. Eggs\n2. Milk\n3. Flour'
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(md_block))
    def test_block_to_block_type_paragraph(self):
        md_block = 'The quick brown fox jumps over the lazy dog. My favorite food is chicken.'
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md_block))

    def test_parse_heading(self):
        md_block = "# Big Heading"
        self.assertEqual(LeafNode("h1", "Big Heading"), parse_heading(md_block))
    def test_parse_heading(self):
        md_block = "###### Small Heading"
        self.assertEqual(LeafNode("h6", "Small Heading"), parse_heading(md_block))
    def test_parse_code(self):
        md_block = "```print()```"
        node = LeafNode("code", "print()")
        cmp_node = parse_code(md_block)
        self.assertEqual(node, cmp_node)
    def test_parse_quote(self):
        md_block = '> The best time to plant a tree was 20 years ago.\n> The second best time is now.'
        node = LeafNode("blockquote", "The best time to plant a tree was 20 years ago.\nThe second best time is now.")
        self.assertEqual(node, parse_quote(md_block))
    def test_parse_ul(self):
        md_block = '- Eggs\n- Milk\n- Flour'
        children = [LeafNode("li", "Eggs"), LeafNode("li", "Milk"), LeafNode("li", "Flour")]
        node = ParentNode("ul", children) 
        self.assertEqual(node, parse_ul(md_block))
    def test_parse_ol(self):
        md_block = '2. Eggs\n3. Milk\n4. Flour'
        children = [LeafNode("li", "Eggs"), LeafNode("li", "Milk"), LeafNode("li", "Flour")]
        node = ParentNode("ol", children, props={"start":"2"}) 
        self.assertEqual(node, parse_ol(md_block))
    def test_parse_md_to_html_nodes(self):
        markdown = "# Big Heading"
        markdown += '\n\n'
        markdown += '```\nprint("What is the answer to the universe")\nprint(42)\n```'
        markdown += '\n\n'
        markdown += '> The best time to plant a tree was 20 years ago.\n> The second best time is now.'
        markdown += '\n\n'
        markdown += '- Eggs\n- Milk\n- Flour'
        markdown += '\n\n'
        markdown += '* Eggs\n* Milk\n* Flour'
        markdown += '\n\n'
        markdown += '1. Eggs\n2. Milk\n3. Flour'
        markdown += '\n\n'
        markdown += 'The quick brown fox jumps over the lazy dog. My favorite food is chicken.'
        node = ParentNode("div", [
            LeafNode("h1", "Big Heading"),
            LeafNode("code", 'print("What is the answer to the universe")\nprint(42)'),
            LeafNode("blockquote", 'The best time to plant a tree was 20 years ago.\nThe second best time is now.'),
            ParentNode("ul", [
                LeafNode("li", "Eggs"),
                LeafNode("li", "Milk"),
                LeafNode("li", "Flour"),
            ]),
            ParentNode("ul", [
                LeafNode("li", "Eggs"),
                LeafNode("li", "Milk"),
                LeafNode("li", "Flour"),
            ]),
            ParentNode("ol", [
                LeafNode("li", "Eggs"),
                LeafNode("li", "Milk"),
                LeafNode("li", "Flour"),
                ], props={"start": "1"}
            ),
            LeafNode("p", "The quick brown fox jumps over the lazy dog. My favorite food is chicken."),
        ])
        self.assertEqual(node, markdown_to_html_node(markdown))
