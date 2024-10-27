from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(text_node):
        match(text_node.text_type):
            case TextType.NORMAL.value:
                return LeafNode(None, text_node.text)
            case TextType.BOLD.value:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC.value:
                return LeafNode("i", text_node.text)
            case TextType.CODE.value:
                return LeafNode("code", text_node.text)
            case TextType.LINK.value:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE.value:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise Exception("Invalid TextType")

