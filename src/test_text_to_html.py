import unittest
from text_to_html import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = [
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, nodes)

    def test_single_delimiter(self):
        nodes = [
            TextNode("hello", TextType.TEXT),
            TextNode("**", TextType.TEXT),
            TextNode("world", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result[1].text, "**")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[0], nodes[0])
        self.assertEqual(result[2], nodes[2])

    def test_multiple_delimiters(self):
        nodes = [
            TextNode("**", TextType.TEXT),
            TextNode("foo", TextType.TEXT),
            TextNode("**", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual(result[0].text, "**")
        self.assertEqual(result[0].text_type, TextType.ITALIC)
        self.assertEqual(result[1], nodes[1])
        self.assertEqual(result[2].text, "**")
        self.assertEqual(result[2].text_type, TextType.ITALIC)

    def test_empty_list(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_delimiter_at_end(self):
        nodes = [
            TextNode("foo", TextType.TEXT),
            TextNode("**", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result[1].text, "**")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[0], nodes[0])

if __name__ == "__main__":
    unittest.main()