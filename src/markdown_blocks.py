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
        if not line.startswith('> '):
            return False
    return True

def is_unordered_list(block):
    lines = block.split('\n')
    for line in lines:
        if not line.startswith('* '):
            return False
    return True

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