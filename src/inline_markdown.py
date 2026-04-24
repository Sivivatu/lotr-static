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
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches: list[Any] = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # this needs to return a list of tuples of the form (link text, url)
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches: list[Any] = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        split_nodes: list[TextNode] = []
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for alt_text, url in matches:
            start_index = node.text.find(f"![{alt_text}]({url})", last_index)
            if start_index == -1:
                continue
            if start_index > last_index:
                split_nodes.append(
                    TextNode(node.text[last_index:start_index], TextType.TEXT)
                )
            split_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt_text}]({url})")
        if last_index < len(node.text):
            split_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        split_nodes: list[TextNode] = []
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        last_index = 0
        for link_text, url in matches:
            markdown = f"[{link_text}]({url})"
            start_index = node.text.find(markdown, last_index)
            if start_index == -1:
                continue
            if start_index > last_index:
                split_nodes.append(
                    TextNode(node.text[last_index:start_index], TextType.TEXT)
                )
            split_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = start_index + len(markdown)
        if last_index < len(node.text):
            split_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes
