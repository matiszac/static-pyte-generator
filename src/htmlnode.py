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
            lambda acc, item: acc + f"{item[0]}=\"{item[1]}\" ",
            self.props.items(),
            ''
        )

    def __repr__(self):
        return f"HTMLNode( {self.tag} , {self.value} , {self.children} , {self.props} )"
