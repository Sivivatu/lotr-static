from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

def split_nodes_delimiter(old_nodes, dlimiter, text_type):
    """
    Splits a list of text nodes into two lists based on a delimiter.
    The first list contains nodes before the delimiter, and the second list contains nodes after the delimiter.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text == dlimiter:
            new_nodes.append(TextNode(node.text, text_type))
        else:
            new_nodes.append(node)
    return new_nodes