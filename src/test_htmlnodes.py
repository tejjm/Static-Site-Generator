import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_different_sites(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
        })
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_v_t(self):
        node = LeafNode("a",
                        "Google",
                        props={
            "href": "https://www.google.com",
        })
        result = node.to_html()
        self.assertEqual(result, '<a href="https://www.google.com">Google</a>') 

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None,"No Tag Test")
        result = node.to_html()
        self.assertEqual(result,"No Tag Test")

    def test_leaf_to_html_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p",None)
            result = node.to_html()

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
    def test_to_html_with_no_tag(self):
        child_node = LeafNode("p","BAHAHAHA")
        parent_node = ParentNode(None,[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_child(self):
        child_node = None
        parent_node = ParentNode("p",child_node)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_textnode_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_textnode_code(self):
        node = TextNode("This is a code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code")

    def test_textnode_link(self):
        node = TextNode("This is a link", TextType.LINK,"www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props,{"href":"www.boot.dev"})
