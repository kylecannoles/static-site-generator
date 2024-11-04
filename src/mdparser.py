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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        # if no images
        if images == []:
            return old_nodes
        text_to_parse = node.text
        # add first image node if text starts with image
        image_alt, image_link = images[0]
        if text_to_parse.startswith(f"![{image_alt}]({image_link})"):
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

        for image_alt, image_link in images:
            sections = text_to_parse.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if len(sections) > 1:
                text_to_parse = sections[1]
        if text_to_parse != "":# if last image parsed, add remaining text as a text node
                new_nodes.append(TextNode(text_to_parse, TextType.TEXT))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        # if no links
        if links == []:
            return old_nodes
        text_to_parse = node.text
        # add first link node if text starts with link
        link_text, link_url = links[0]
        if text_to_parse.startswith(f"[{link_text}]({link_url})"):
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        for link_text, link_url in links:
            sections = text_to_parse.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            if len(sections) > 1:
                text_to_parse = sections[1]
        if text_to_parse != "":# if last image parsed, add remaining text as a text node
                new_nodes.append(TextNode(text_to_parse, TextType.TEXT))
    return new_nodes
