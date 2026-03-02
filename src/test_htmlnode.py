import unittest

from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_initialization(self):
        # Test initialization with all parameters
        node = HTMLNode(tag="div", value="Hello World", 
                        children=[HTMLNode("span", "Nested")], 
                        props={"class": "container"})
        
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello World")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].value, "Nested")
        self.assertEqual(node.props, {"class": "container"})

    def test_default_initialization(self):
        # Test initialization with default parameters
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_eq(self):
        # Test equality between two identical nodes
        node1 = HTMLNode(tag="div", value="Hello")
        node2 = HTMLNode(tag="div", value="Hello")
        self.assertEqual(node1, node2)

        # Test equality between two different nodes
        node3 = HTMLNode(tag="p", value="Hello")
        self.assertNotEqual(node1, node3)

    def test_repr(self):
        # Test the string representation
        node = HTMLNode(tag="p", value="Hello", props={"class": "text"})
        expected_repr = "HTMLNode(tag=p, value=Hello, children=[], props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html(self):
        # Test props_to_html method with props
        node = HTMLNode(tag="a", props={"href": "http://example.com", "target": "_blank"})
        expected_props_html = ' href="http://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_props_html)

        # Test props_to_html method with no props
        node_empty_props = HTMLNode(tag="div")
        self.assertEqual(node_empty_props.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a Link", {"href": "http://example.com", "target": "_blank"})
        expected_html = '<a href="http://example.com" target="_blank">This is a Link</a>'
        self.assertEqual(node.to_html(), expected_html)
       
if __name__ == "__main__":
    unittest.main()
