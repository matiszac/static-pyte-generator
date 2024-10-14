import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
)

case_images = (
    'This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)',
    [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
)
case_links = (
    'This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)',
    [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
)

test_markdown_text = '''# heading

* item 1
* item 2
* item 3

Some normal text *italic* now some `code` and **bold**.



## Heading 2


Click [here](https://google.com)'''

test_markdown_result = [
    '# heading',
    '* item 1\n* item 2\n* item 3',
    'Some normal text *italic* now some `code` and **bold**.',
    '## Heading 2',
    'Click [here](https://google.com)',
]

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_images(self):
        result = extract_markdown_images(case_images[0])
        self.assertEqual(result, case_images[1])

    def test_extract_links(self):
        result = extract_markdown_links(case_links[0])
        self.assertEqual(result, case_links[1])

    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(test_markdown_text)
        self.assertEqual(blocks, test_markdown_result)
        


if __name__ == "__main__":
    unittest.main()