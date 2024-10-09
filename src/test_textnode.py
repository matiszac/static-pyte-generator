import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
