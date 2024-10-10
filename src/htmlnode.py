from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # '<p>'
        self.value = value # text
        self.children = children # ['<li>', '<li>']
        self.props = props # { 'href': 'http://link.to.somewhere' }

    def to_html(self):
        raise NotImplementedError('Child classes must override')

    def props_to_html(self):
        if self.props == None:
            return ''
        if len(self.props) == 0:
            return ''
        return reduce(
            lambda acc, item: acc + f'{item[0]}="{item[1]}" ',
            self.props.items(),
            ''
        ).rstrip()

    def tag_to_html(self):
        if self.tag == None:
            return '', '', ''
        if self.tag == '':
            return '', '', ''
        if self.props is None or self.props == {}:
            return f"<{self.tag}", ">", f"</{self.tag}>"
        return f"<{self.tag} ", ">", f"</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode( {self.tag} , {self.value} , {self.children} , {self.props} )"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('LeafNode must have a value')
        openl, openr, close = self.tag_to_html()
        props = self.props_to_html()
        return f"{openl}{props}{openr}{self.value}{close}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == '':
            raise ValueError('ParentNode must have a tag')
        if self.children is None or self.children == []:
            raise ValueError('ParentNode must have LeafNode children')
        openl, openr, close_tag = self.tag_to_html()
        tag_props = self.props_to_html()
        open_tag = f'{openl}{tag_props}{openr}'
        children_html = reduce(
            lambda acc, node: acc + node.to_html(),
            self.children,
            ''
        )
        return f'{open_tag}{children_html}{close_tag}'
