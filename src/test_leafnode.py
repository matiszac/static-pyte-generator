import unittest

from leafnode import LeafNode

props = {
    'href': 'https://github.com',
    'target': '_blank'
}

value_raw = 'this is some raw text'
value_a = 'This is a LINK'

class TestLeafNode(unittest.TestCase):
    def test_html_no_tag(self):
        node = LeafNode(value_raw)
        self.assertEqual(node.to_html(), value_raw)

    def test_html_a_tag(self):
        node = LeafNode(value_a, 'a', props)
        self.assertEqual(
            node.to_html(),
            f'<a href="https://github.com" target="_blank">{value_a}</a>'
        )

    def test_no_value(self):
        node = LeafNode(None)
        self.assertRaises(ValueError, node.to_html)



if __name__ == "__main__":
    unittest.main()

