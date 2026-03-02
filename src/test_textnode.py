import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_enum_values(self):
        self.assertEqual(TextType.NORMAL.value, "normal")
        self.assertEqual(TextType.BOLD.value, "bold")
        self.assertEqual(TextType.ITALIC.value, "italic")
        self.assertEqual(TextType.CODE.value, "code")
        self.assertEqual(TextType.LINK.value, "link")
        self.assertEqual(TextType.IMAGE.value, "image")

    def test_text_node_initialization(self):
        node = TextNode("Hello, World!", TextType.NORMAL, "http://example.com")
        self.assertEqual(node.text, "Hello, World!")
        self.assertEqual(node.text_type, TextType.NORMAL)
        self.assertEqual(node.url, "http://example.com")

    def test_text_node_equality(self):
        node1 = TextNode("Hello", TextType.BOLD, "http://example.com")
        node2 = TextNode("Hello", TextType.BOLD, "http://example.com")
        node3 = TextNode("Goodbye", TextType.NORMAL, "http://example.com")
        node4 = TextNode("Hello", TextType.BOLD)

        self.assertEqual(node1, node2)  # Should be equal
        self.assertNotEqual(node1, node3)  # Should not be equal
        self.assertNotEqual(node1, node4)  # Should not be equal

    def test_text_node_repr(self):
        node = TextNode("Sample Text", TextType.ITALIC, "http://example.com")
        self.assertEqual(repr(node), "TextNode(Sample Text, italic, http://example.com)")

    def test_text_node_default_url(self):
        node = TextNode("Sample Text", TextType.LINK)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()