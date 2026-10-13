import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_multiple_props(self):
        node = HTMLNode("h1", "IT WORKS", [HTMLNode("h1", "IT WORKS")], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node = HTMLNode("h1", "IT WORKS", [HTMLNode("h1", "IT WORKS")])
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_one_prop(self):
        node = HTMLNode("h1", "IT WORKS", [HTMLNode("h1", "IT WORKS")],{
            "href": "https://www.google.com",
        })
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!",{
            "href": "https://www.google.com",
        })
        self.assertEqual(node.to_html(), '<p href="https://www.google.com">Hello, world!</p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "https://boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">Click here</a>'
        )
    def test_leaf_repr(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(repr(node), "LeafNode(b, bold text, None)")

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

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = ParentNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>child</p></div>")

    def test_to_html_with_props(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("p", "child")
        parent_node = ParentNode("div", [child_node1, child_node2], {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(parent_node.to_html(), '<div href="https://www.google.com" target="_blank"><span>child</span><p>child</p></div>')


if __name__ == "__main__":
    unittest.main()