from htmlnode import LeafNode

text_type_text = 'text'
text_type_bold = 'bold'
text_type_italic = 'italic'
text_type_code = 'code'
text_type_image = 'image'
text_type_link = 'link'

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

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
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
