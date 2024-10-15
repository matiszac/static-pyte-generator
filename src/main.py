import re
from htmlnode import ParentNode, LeafNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
)
from inline_markdown import (
    text_to_textnodes,
)
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
)

test_case = 'Follow ![some alt text](url/to/img) `this` ****[link](url/to/link) some more text *** for *more info*** hi**  '

old_nodes = [
    TextNode('Hello, please visit [google](https://google.com) to search for cat images like ![funny cat](url/to/img)', text_type_text),
    TextNode('nothing but text', text_type_text),
    TextNode('funny cat', text_type_image, 'url/to/img'),
    TextNode('google', text_type_link, 'https://google.com'),
    TextNode('![funny cat1](url/to/img) [google2](https://google.com) ![funny cat2](url/to/img)', text_type_text)
]

line = 'This is **text** with an *italic* word and a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'

test_text = '''# heading

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


def main():
    res = markdown_to_blocks(test_text)
    for r in res:
        print(block_to_block_type(r))



def txt_to_nodes(line):
    tags, has_children, content, start, end, = [], [], [], [], []
    index, ignore_asterisks, i = 0, 0, 0
    line_length = len(line)
    while i < line_length:
        iteration = i

        # move cursor past the amount of ignored asterisks
        # asterisks ignore count increases after successfully
        # identifying bold or italic tags
        # this is to prevent trying to parse closing asterisks
        while line[i] == '*' and ignore_asterisks > 0:
            i += 1
            ignore_asterisks -= 1
            if i >= line_length:
                i -= 1

        # check for inline code ` `
        if i+1 < line_length:
            if line[i] == '`' and line[i+1] != '`':
                tags.append('code')
                content.append('')
                start.append(i)
                index += 1
                for x in range(i+1, line_length):
                    if line[x] == '`':
                        i = x + 1
                        end.append(x-1)
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # check for image ![]()
        if i+3 < line_length:
            if line[i]+line[i+1] == '![' and line[i+2]+line[i+3] != '![':
                tags.append('img')
                content.append('')
                start.append(i)
                index += 1
                for x in range(i+2, line_length):
                    if line[x] == ')':
                        i = x+1
                        end.append(x-1)
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # check for link []()
        if i+1 < line_length:
            if line[i] == '[' and line[i+1] != '[':
                tags.append('a')
                content.append('')
                start.append(i)
                index += 1
                for x in range(i+1, line_length):
                    if line[x] == ')':
                        i = x + 1
                        end.append(x-1)
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # check for italic nesting bold ***
        if i+3 < line_length:
            if  line[i]+line[i+1]+line[i+2] == '***' and line[i+3] != '*':
                tags.append('i')
                content.append('**')
                start.append(i)
                index += 1
                for x in range(i+3, line_length):
                    if line[x] == '*':
                        if x+2 >= line_length:
                            break
                        if line[x+1]+line[x+2] != '**':
                            break
                        i += 1
                        content[index-1] += '**'
                        end.append(x+1)
                        ignore_asterisks += 1
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # check for bold **
        if i+2 < line_length:
            if line[i]+line[i+1] == '**' and line[i+2] != '*':
                tags.append('b')
                content.append('')
                start.append(i)
                index += 1
                for x in range(i+2, line_length):
                    if line[x] == '*':
                        if x+1 >= line_length:
                            break
                        if line[x+1] != '*':
                            break
                        i += 2
                        end.append(x)
                        ignore_asterisks += 2
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # check for italic *
        if i+1 < line_length:
            if line[i] == '*' and line[i+1] != '*':
                tags.append('i')
                content.append('')
                start.append(i)
                index += 1
                for x in range(i+1, line_length):
                    if line[x] == '*':
                        i += 1
                        end.append(x-1)
                        ignore_asterisks += 1
                        break
                    content[index-1] += line[x]
                if len(end) != index:
                    del tags[-1]
                    del content[-1]
                    del start[-1]
                    index -= 1

        # if nothing was detected, advance the cursor by 1
        if i < line_length:
            if iteration == i:        
                i += 1

   
    # simplify checking line index out of bounds
    # by fixing the end values last
    # did not want to complicate tag parsing logic 
    for i in range(0, len(end)):
        if end[i]+2 < line_length+1:
            end[i] += 2


    # identify parents
    for i in range(0, len(tags)):
        children = 0
        for x in range(i+1, len(tags)):
            if start[x] > start[i] and end[x] < end[i]:
                children += 1
        if children > 0:
            has_children.append(children)
            content[i] = ''
        else:
            has_children.append(0)


    # parse raw text nodes
    raw_tags, raw_has_children, raw_content, raw_start, raw_end = [], [], [], [], []
    x, se_index, raw_index, skip_asterisk = 0, 0, 0, 0
    while x < line_length:
        raw_tags.append('')
        raw_content.append('')
        raw_has_children.append(0)
        raw_start.append(x)
        raw_index+=1
        for y in range(x, line_length):
            if y == start[se_index]:
                if tags[se_index] == 'i':
                    skip_asterisk += 1
                    x = start[se_index]+1
                elif tags[se_index] == 'b':
                    skip_asterisk += 2
                    x = start[se_index]+2
                else:
                    x = end[se_index]
                se_index += 1
                if y == raw_start[raw_index-1]:
                    break
                raw_end.append(y)
                break
            
            if line[y] == '*' and skip_asterisk > 0:
                raw_end.append(y)
                x = y + skip_asterisk
                skip_asterisk = 0
                break

            raw_content[raw_index-1] += line[y]

        if len(raw_end) != raw_index:
            del raw_tags[-1]
            del raw_has_children[-1]
            del raw_content[-1]
            del raw_start[-1]
            raw_index -= 1

        if se_index+1 == len(end) and x < line_length:
            x = end[se_index]
            raw_tags.append('')
            raw_has_children.append(0)
            raw_content.append(line[x:])
            raw_start.append(x)
            raw_end.append(line_length)
            raw_index+=1
            x = line_length

    raw_nodes = list(zip(raw_tags, raw_has_children, raw_content, raw_start, raw_end))


    #            10        20        30        40        50        60        70        80        90        100
    #   1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9 1 3 5 7 9
    #   | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
    # >Follow ![some alt text](url/to/img) `this` ****[link](url/to/link) some more text *** for *more info*** hi**  <
    #  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
    #  0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0 2 4 6 8 0
    #            10        20        30        40        50        60        70        80        90        100       110

    
    tagged_nodes =  list(zip(tags, has_children, content, start, end))

    # sort all nodes by starting index
    all_nodes = sorted([*raw_nodes, *tagged_nodes], key=lambda node: node[3])

    # properly nest nodes
    # returns a list of tuples [tag, has_children, content, start_slice, end_slice, [children]]
    organized_nodes = get_nodes_and_children(all_nodes)

    #return None

def get_nodes_and_children(all_nodes):
    node_count = len(all_nodes)
    organized_nodes = []
    index = 0
    while index < node_count:
        # if node does not have children
        if all_nodes[index][1] == 0:
            organized_nodes.append(all_nodes[index]+(None,))
            index += 1
        else:
            resume_index = index
            # search for node index of next non child
            # set it as an index to resume from
            for curr in range(index+1, node_count):
                if curr >= node_count:
                    break
                if all_nodes[curr][3] > all_nodes[index][4]:
                    resume_index = curr
                    break
            # recursively call self to get children
            children = get_nodes_and_children(all_nodes[index+1:resume_index])
            organized_nodes.append(all_nodes[index]+(children,))
            # resume, after retrieving children, from the next non child node
            index = resume_index
    return organized_nodes


    

def r(line, pattern):
    return re.findall(pattern, line)

main()
