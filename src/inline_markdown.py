import re
from typing import Any

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        split_nodes: list[TextNode] = []   
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown: formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    # this needs to return a list of tuples of the form (alt text, url)
    pattern =  r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches: list[Any] = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # this needs to return a list of tuples of the form (link text, url)
    pattern =  r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches: list[Any] = re.findall(pattern, text)
    return matches