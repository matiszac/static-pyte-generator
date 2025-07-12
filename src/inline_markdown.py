import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def extract_text_link_tuple(text):
    if text.startswith('!['):
        prefix = '!['
    elif text.startswith('['):
        prefix = '['
    else:
        raise ValueError('invalid prefix')
    return (*text.lstrip(prefix).rstrip(')').split(']('),)

def extract_markdown_images(text):
    ptn_image = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    return re.findall(ptn_image, text)

def extract_markdown_links(text):
    ptn_link = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    return re.findall(ptn_link, text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_images(text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        match_length = len(matches)
        for index in range(match_length):
            alt, url = matches[index][0], matches[index][1]
            original = f'![{alt}]({url})'
            splits = text.split(original, 1)
            if splits[0] != '':
                new_nodes.append(TextNode(splits[0],text_type_text))
            new_nodes.append(TextNode(alt, text_type_image, url))
            if index == match_length-1:
                new_nodes.append(TextNode(splits[1],text_type_text))
                continue
            if len(splits) > 1:
                text = splits[1]
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_links(text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        match_length = len(matches)
        for index in range(match_length):
            anchor_text, url = matches[index][0], matches[index][1]
            original = f'[{anchor_text}]({url})'
            splits = text.split(original, 1)
            if splits[0] != '':
                new_nodes.append(TextNode(splits[0], text_type_text))
            new_nodes.append(TextNode(anchor_text, text_type_link, url))
            if index == match_length-1:
                new_nodes.append(TextNode(splits[1],text_type_text))
                continue
            if len(splits) > 1:
                text = splits[1]
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '__', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '_', text_type_italic)
    return nodes




