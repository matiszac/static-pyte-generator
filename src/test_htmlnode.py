import unittest

from htmlnode import HTMLNode

props1 = {
    'href': 'https://github.com'
}

props2 = {
    'href': 'https://github.com',
    'target': '_blank'
}

class TestHTMLNode(unittest.TestCase):
    def test_props_zero(self):
        node = HTMLNode(None, None, None, None)
        node2 = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), '')
        self.assertEqual(node2.props_to_html(), '')
        
    def test_props_single(self):
        props = props1.copy()
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), 'href="https://github.com" ')

    def test_props_double(self):
        props = props2.copy()
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), 'href="https://github.com" target="_blank" ')

    def test_print(self):
        node = HTMLNode('p', 'This is a paragraph.', ['a', 'a'], {})
        print(node)


if __name__ == "__main__":
    unittest.main()
