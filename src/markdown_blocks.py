from htmlnode import (
    ParentNode,
    LeafNode
)
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_p = 'paragraph'
block_type_h = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_ul = 'unordered_list'
block_type_ol = 'ordered_list'

def markdown_to_blocks(markdown):
    splits = markdown.split('\n\n')
    if len(splits) == 0:
        return []
    blocks = []
    for block in splits:
        if block == '':
            continue
        blocks.append(block.strip())
    return blocks

def is_heading(block):
    if len(block) < 3 or block[0] != '#':
        return False
    count = 0
    splits = block.split('#')
    i = 0
    while splits[i] == '' and i < len(splits):
        count+= 1
        if i == len(splits)-1:
            break
        i += 1
    if count <= 6 and splits[count][0] == ' ':
        return True
    return False

def is_code_block(block):
    splits = block.split('\n')
    if len(splits) < 3:
        return False
    if splits[0].strip() == '```' and splits[-1].strip() == '```':
        return True
    return False

def is_quote(block):
    lines = block.split('\n')
    for line in lines:
        if not line.startswith('>'):
            return False
        if len(line) > 1 and not line.startswith('> '):
            return False
    return True

def is_unordered_list(block):
    lines = block.split('\n')
    for line in lines:
        if line.startswith('* ') or line.startswith('- '):
            return True
    return False

def is_ordered_list(block):
    if not '.' in block:
        return False
    lines = block.split('\n')
    for line in lines:
        split = line.split('.')
        if not split[0].isdigit() or not split[1].startswith(' '):
            return False
    return True

def block_to_block_type(block):
    if len(block) == 0:
        raise ValueError('invalid block')
    
    if is_heading(block):
        return block_type_h
    if is_code_block(block):
        return block_type_code
    if is_quote(block):
        return block_type_quote
    if is_unordered_list(block):
        return block_type_ul
    if is_ordered_list(block):
        return block_type_ol
    
    return block_type_p

def markdown_to_html_node(markdown):
    div = ParentNode('div', [], None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        html_node = block_to_html_node(block, type)
        div.children.append(html_node)
    return div

def block_to_html_node(block, type):
    if type == block_type_p:
        return paragraph_to_html_node(block)
    if type == block_type_h:
        return heading_to_html_node(block)
    if type == block_type_code:
        return code_to_html_node(block)
    if type == block_type_quote:
        return quote_to_html_node(block)
    if type == block_type_ul:
        return unordered_list_to_html_node(block)
    if type == block_type_ol:
        return ordered_list_to_html_node(block)
    
def text_to_children_nodes(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children
    
def heading_to_html_node(block):
    index = 0
    while block[index] == '#':
        index += 1
    tag = f'h{index}'
    leader = '#'*index+' '
    text = block.lstrip(leader)
    children = text_to_children_nodes(text)
    return ParentNode(tag, children, None)

def code_to_html_node(block):
    content = block.lstrip('```\n').rstrip('\n```')
    code = LeafNode('code', content, None)
    return ParentNode('pre', [code], None)

def quote_to_html_node(block):
    text = ''
    lines = block.split('\n')
    for line in lines:
        text += line.lstrip('> ')+'<br>'
    text = text.rstrip('<br>')
    children = text_to_children_nodes(text)
    return ParentNode('blockquote', children, None)
    
def unordered_list_to_html_node(block):
    ul = ParentNode('ul', [], None)
    lines = block.split('\n')
    symbol = '* '
    if lines[0].startswith('-'):
        symbol = '- '
    for line in lines:
        text = line.lstrip(symbol)
        children = text_to_children_nodes(text)
        ul.children.append(ParentNode('li', children, None))
    return ul


def ordered_list_to_html_node(block):
    ol = ParentNode('ol', [], None)
    lines = block.split('\n')
    for line in lines:
        text = line.partition('. ')[2]
        children = text_to_children_nodes(text)
        ol.children.append(ParentNode('li', children, None))
    return ol
        
def paragraph_to_html_node(block):
    children = text_to_children_nodes(block)
    return ParentNode('p', children, None)
