from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case 'text':
                return LeafNode(None, text_node.text)
            case 'bold':
                return LeafNode('b', text_node.text)
            case 'italic':
                return LeafNode('i', text_node.text)
            case 'code':
                return LeafNode('code', text_node.text)
            case 'link':
                return LeafNode('a', text_node.text, { 'href': text_node.url })
            case 'image':
                return LeafNode('img', '', { 'src': text_node.url, 'alt': text_node.text })
            case _:
                raise ValueError('Not a valid TextNode type')

    def __eq__(self, text_node):
        if self.url != text_node.url:
            return False
        if self.text_type != text_node.text_type:
            return False
        if self.text != text_node.text:
            return False
        return True

    def __repr__(self):
        return f"TextNode( {self.text} , {self.text_type} , {self.url} )"
