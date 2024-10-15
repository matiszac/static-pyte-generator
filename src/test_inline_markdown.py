import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)

case_images = (
    'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)',
    [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
)
case_links = (
    'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)',
    [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
)

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_images(self):
        result = extract_markdown_images(case_images[0])
        self.assertEqual(result, case_images[1])

    def test_extract_links(self):
        result = extract_markdown_links(case_links[0])
        self.assertEqual(result, case_links[1])
        


if __name__ == "__main__":
    unittest.main()