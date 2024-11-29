import re
from enum import Enum

from textnode import TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delim_len = len(delimiter)
    for node in old_nodes:
        if node.text_type == "text":
            if node.text is None or node.text == "":
                raise Exception("Empty node text")
            start = node.text.find(delimiter)
            # check if text has odd number of delimiters
            num_delimiters = node.text.count(delimiter)
            if num_delimiters % 2 != 0:
                raise Exception("Parsing error: Delimiter not closed")
            elif num_delimiters == 0:
                # skip processing node
                new_nodes.extend([node])
            else:
                # try string.split
                split_text = node.text.split(delimiter)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                if split_text[1] != "":
                    new_nodes.append(TextNode(split_text[1], text_type))
                if split_text[2] != "":
                    new_nodes.append(TextNode(split_text[2], TextType.TEXT))
        else:
            new_nodes.extend([node])
    return new_nodes

def extract_markdown_images(text):
    image_list = []
    matches = re.findall(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    return matches
def extract_markdown_links(text):
    image_list = []
    matches = re.findall(r"(?:[^!]|^)\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        # if no images
        if images == []:
            new_nodes.extend([node])
            continue
        text_to_parse = node.text
        # add first image node if text starts with image
        image_alt, image_link = images[0]
        if text_to_parse.startswith(f"![{image_alt}]({image_link})"):
            new_nodes.extend([TextNode(image_alt, TextType.IMAGE, image_link)])

        for image_alt, image_link in images:
            sections = text_to_parse.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.extend([TextNode(sections[0], TextType.TEXT)])
                new_nodes.extend([TextNode(image_alt, TextType.IMAGE, image_link)])
            if len(sections) > 1:
                text_to_parse = sections[1]
        if text_to_parse != "":# if last image parsed, add remaining text as a text node
                new_nodes.extend([TextNode(text_to_parse, TextType.TEXT)])
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        # if no links
        if links == []:
            new_nodes.extend([node])
            continue
        text_to_parse = node.text
        # add first link node if text starts with link
        link_text, link_url = links[0]
        if text_to_parse.startswith(f"[{link_text}]({link_url})"):
            new_nodes.extend([TextNode(link_text, TextType.LINK, link_url)])

        for link_text, link_url in links:
            sections = text_to_parse.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.extend([TextNode(sections[0], TextType.TEXT)])
                new_nodes.extend([TextNode(link_text, TextType.LINK, link_url)])
            if len(sections) > 1:
                text_to_parse = sections[1]
        if text_to_parse != "":# if last image parsed, add remaining text as a text node
                new_nodes.extend([TextNode(text_to_parse, TextType.TEXT)])
    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "*", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def markdown_to_blocks(markdown):
    sections = re.split(r'\n[\t\f\v\r ]*\n', markdown)
    sections = list(map(str.strip, sections))
    sections = [s for s in sections if s != ""]
    return sections
def block_to_block_type(markdown_block):
    block_types = {
        BlockType.HEADING : r'#{1,6} .+',
        BlockType.CODE : r'^`{3}\n[\S\s]+\n`{3,}',
        BlockType.QUOTE : r'>{1,}[\s]+.+',
        BlockType.UNORDERED_LIST : r'([-\*] .*)',
        BlockType.ORDERED_LIST : r'([0-9]. .*)',
    }
    for typ, pattern in block_types.items():
        if re.findall(pattern, markdown_block):
            return typ
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    # parse markdown into blocks
    md_blocks = markdown_to_blocks(markdown)
    node_list = []
    # parse blocks into html nodes
    for block in md_blocks:
        # determine type of block
        block_type = block_to_block_type(block)
        # create HTMLNode based on block type
        block_html_node = None
        match block_type:
            case BlockType.HEADING:
                block_html_node = parse_heading(block)
            case BlockType.CODE:
                block_html_node = parse_code(block)
            case BlockType.QUOTE:
                block_html_node = parse_quote(block)
            case BlockType.UNORDERED_LIST:
                block_html_node = parse_ul(block)
            case BlockType.ORDERED_LIST:
                block_html_node = parse_ol(block)
            case BlockType.PARAGRAPH:
                block_html_node = parse_paragraph(block)
        node_list.append(block_html_node)

    # add all html nodes as children under a <div> node
    markdown_node = ParentNode("div", node_list)
    return markdown_node

def parse_heading(block):
    # number of # symbols = header level
    count = 0
    inner_text = ""
    pos = 0
    for pos in range(len(block)):
        if block[pos] == '#':
            count += 1
        else:
            break
    if block[pos] ==  ' ':
        node_list = text_to_textnodes(block[pos+1:])
        if len(node_list) > 1:
            html_nodes = text_node_list_to_html_node_list(node_list)
            return ParentNode(f"h{count}", html_nodes)
        else:
            return LeafNode(f"h{count}", block[pos+1:])
    return None
def parse_code(block):
    if block.startswith("```") and block.endswith("```"):
        return LeafNode("code", block[3:-3].strip())
def parse_quote(block):
    final_quote = ""
    split_block = block.split("\n")
    for line in split_block:
        if line.startswith("> "):
            final_quote += line[2:] + "\n"
    return LeafNode("blockquote", final_quote[:-1])
def parse_ul(block):
    children = []
    split_block = block.split("\n")
    for line in split_block:
        if line.startswith("-") or line.startswith("*"):
            node_list = text_to_textnodes(line[2:])
            if len(node_list) > 1:
                html_nodes = text_node_list_to_html_node_list(node_list)
                children.append(ParentNode("li", html_nodes))
            else:
                children.append(LeafNode("li", line[2:]))
    return ParentNode("ul", children) 
def parse_ol(block):
    children = []
    split_block = block.split("\n")
    start_pos = split_block[0].find(".")
    start = split_block[0][:start_pos]
    text = split_block[0][start_pos+1:].lstrip()
    children.append(LeafNode("li", text))
    for line in split_block[1:]:
        line_pos = line.find(".")
        text = line[line_pos+1:].lstrip()
        node_list = text_to_textnodes(text)
        if len(node_list) > 1:
            html_nodes = text_node_list_to_html_node_list(node_list)
            children.append(ParentNode("li", html_nodes))
        else:
            children.append(LeafNode("li", text))
    return ParentNode("ol", children, props={"start": start})
def parse_paragraph(block):
    node_list = text_to_textnodes(block)
    if len(node_list) > 1:
        html_nodes = text_node_list_to_html_node_list(node_list)
        return ParentNode("p", html_nodes)
    return LeafNode("p", block)
def text_node_list_to_html_node_list(textnode_list):
    html_node_list = []
    for node in textnode_list:
        html_node_list.append(TextNode.text_node_to_html_node(node))
    return html_node_list

def extract_title(markdown):
    title = markdown.lstrip()
    title_end_pos = title.find("\n")
    title = title[:title_end_pos]
    if title.startswith("# "):
        return title[2:].lstrip()
    raise ValueError("Markdown must contain a title (heading 1) as the first block")
