from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        HTMLNode.__init__(self, tag, value, None, props)
    def __eq__(self, node):
        if not isinstance(node, LeafNode):
            return NotImplemented
        return self.tag == node.tag and self.value == node.value and self.props == node.props
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html() if self.props != None else ""}>{self.value}'
        return f'<{self.tag}{self.props_to_html() if self.props != None else ""}>{self.value}</{self.tag}>'
