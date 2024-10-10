import unittest

from htmlnode import ParentNode, LeafNode


expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
expected_result_props = '<p class="css-class-p"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'

class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        self.assertEqual(node.to_html(), expected_result)

    def test_nested_parent(self):
        child_parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        parent_node = ParentNode('div', [child_parent_node])
        self.assertEqual(parent_node.to_html(), f'<div>{expected_result}</div>')

    def test_nested_parent_props(self):
        child_parent_node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        {
            'class': 'css-class-p'
        },
        )
        parent_node = ParentNode('div', [child_parent_node], { 'class': 'css-class-div' })
        self.assertEqual(parent_node.to_html(), f'<div class="css-class-div">{expected_result_props}</div>')

    def test_no_tag(self):
        node = ParentNode(
        '',
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_no_children(self):
        node = ParentNode('p', [])
        self.assertRaises(ValueError, node.to_html)



if __name__ == "__main__":
    unittest.main()
