class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("children will override this method")
    def props_to_html(self):
        if self.props:
            result = ""
            for key,value in self.props.items():
                result += f' {key}="{value}"'
            return result
        return None
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})'
