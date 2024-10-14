import unittest

from textnode import (TextNode, text_node_to_html_node)
from htmlnode import LeafNode


t_text = (['text text', 'text', ''], 'text text')
t_bold = (['bold text', 'bold', ''], '<b>bold text</b>')
t_italic = (['italic text', 'italic', ''], '<i>italic text</i>')
t_code = (['code text', 'code', ''], '<code>code text</code>')
t_link = (['anchor text', 'link', 'link/url'], '<a href="link/url">anchor text</a>')
t_image = (['alt text', 'image', 'img/url'], '<img src="img/url" alt="alt text"></img>')

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode('some text', 'italic', 'https://boot.dev')
        node4 = TextNode('some text', 'italic', 'https://boot.dev')
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_nteq(self):
        node = TextNode("This is a text node", "bold")
        node4 = TextNode('some text', 'italic', 'https://boot.dev')
        node5 = TextNode('some texx', 'italic', 'https://boot.dev')
        node6 = TextNode('some text', 'italii', 'https://boot.dev')
        node7 = TextNode('some text', 'italic', 'https://boot.dex')
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node4, node6)
        self.assertNotEqual(node4, node7)

    def test_to_node_invalid_type(self):
        node = TextNode('text', 'xyz', 'googles')
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_to_node_text(self):
        node = TextNode(*t_text[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_text[1])

    def test_to_node_bold(self):
        node = TextNode(*t_bold[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_bold[1])

    def test_to_node_italic(self):
        node = TextNode(*t_italic[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_italic[1])

    def test_to_node_code(self):
        node = TextNode(*t_code[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_code[1])

    def test_to_node_link(self):
        node = TextNode(*t_link[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_link[1])

    def test_to_node_image(self):
        node = TextNode(*t_image[0])
        leaf_html = text_node_to_html_node(node).to_html()
        self.assertEqual(leaf_html, t_image[1])



if __name__ == "__main__":
    unittest.main()
