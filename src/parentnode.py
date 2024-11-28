from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)     
    def __eq__(self, node):
        if not isinstance(node, ParentNode):
            return NotImplemented
        return self.tag == node.tag and self.children == node.children and self.props == node.props
    def to_html(self):
        if self.tag is None:
            raise ValueError("An html tag is required")
        if self.children is None or self.children == []:
            raise ValueError("A parent node must have children. Did you mean to make a LeafNode?")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f'<{self.tag}>{result}</{self.tag}>'
