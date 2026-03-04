import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(node.children, None)
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
        expected_repr = "HTMLNode(tag=p, value=Hello, children=None, props={'class': 'text'})"
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

    def test_leaf_to_html_a(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a Link", {"href": "http://example.com", "target": "_blank"})
        expected_html = '<a href="http://example.com" target="_blank">This is a Link</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_to_html_no_value(self):
        node = LeafNode("div", "") 
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_tag_no_props(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_tag_multiple_props(self):
        node = LeafNode("a", "This is a link", {"href": "http://example.com", "target": "_blank"})
        expected_html = '<a href="http://example.com" target="_blank">This is a link</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        # Test with no tag set — should raise ValueError
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        # Test with None children — should raise ValueError
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children(self):
        # Test with an empty children list
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")  # Should return empty tags

    def test_to_html_with_no_props(self):
        # Test for a tag with no props and one child
        child_node = LeafNode("p", "Hello")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_with_multiple_children(self):
        # Test with multiple children
        child_node1 = LeafNode("p", "Child 1")
        child_node2 = LeafNode("span", "Child 2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Child 1</p><span>Child 2</span></div>"
        )

if __name__ == "__main__":
    unittest.main()
