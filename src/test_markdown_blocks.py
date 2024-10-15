import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_p,
    block_type_h,
    block_type_ul,
    block_type_ol,
    block_type_quote,
    block_type_code,
)

test_markdown_case = '''# heading

* item 1
* item 2
* item 3

Some normal text *italic* now some `code` and **bold**.

1. yes
2. i
3. can

> i love
> programming

```
some code
```

## Heading 2


Click [here](https://google.com)'''

test_markdown_result = [
    '# heading',
    '* item 1\n* item 2\n* item 3',
    'Some normal text *italic* now some `code` and **bold**.',
    '1. yes\n2. i\n3. can',
    '> i love\n> programming',
    '```\nsome code\n```',
    '## Heading 2',
    'Click [here](https://google.com)',
]

test_markdown_types = [
    block_type_h,
    block_type_ul,
    block_type_p,
    block_type_ol,
    block_type_quote,
    block_type_code,
    block_type_h,
    block_type_p,
]

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(test_markdown_case)
        self.assertEqual(blocks, test_markdown_result)

    def test_blocks_to_types(self):
        blocks = markdown_to_blocks(test_markdown_case)
        for i in range(len(blocks)):
            self.assertEqual(block_to_block_type(blocks[i]), test_markdown_types[i])
        


if __name__ == "__main__":
    unittest.main()