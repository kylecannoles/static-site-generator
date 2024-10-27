import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    delim_len = len(delimiter)
    for node in old_nodes:
        if node.text_type == "text":
            if node.text is None or node.text == "":
                raise Exception("Empty node text")
            start = node.text.find(delimiter)
            if start == -1:
                raise Exception("Delimiter not found")
            first = node.text[0:start]
            if start + delim_len > len(node.text):
                raise Exception("Only one delimiter found at end of string")
            remainder = node.text[start+delim_len:]
            end = remainder.find(delimiter)
            if end == -1:
                raise Exception("Delimiter not found")
            second = remainder[:end]
            third = remainder[end+delim_len:]

            if len(first) == 0:
                new_nodes.extend([
                    TextNode(second, text_type),
                    TextNode(third, TextType.TEXT),
                ])
            elif len(third) == 0:
                new_nodes.extend([
                    TextNode(first, TextType.TEXT),
                    TextNode(second, text_type),
                ])
            else:
                new_nodes.extend([
                    TextNode(first, TextType.TEXT),
                    TextNode(second, text_type),
                    TextNode(third, TextType.TEXT),
                ])
        else:
            new_nodes.extend(node)
    return new_nodes

def extract_markdown_images(text):
    image_list = []
    matches = re.findall(r"!\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    return matches
def extract_markdown_links(text):
    image_list = []
    matches = re.findall(r"(?:[^!]|^)\[([^\[\]]*?)\]\(([^\(\)]*?)\)", text)
    return matches
