from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('LeafNode must have a value')
        openl, openr, close = self.tag_to_html()
        props = self.props_to_html()
        return f"{openl}{props}{openr}{self.value}{close}"
