import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_italic(self):
        node = TextNode("This is a test node",TextType.ITALIC)
        node2 = TextNode("This is a test node",TextType.ITALIC)
        self.assertEqual(node,node2)
    
    def test_text_type(self):
        node = TextNode("This is a test node",TextType.ITALIC)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertNotEqual(node,node2)
    
    def test_url(self):
        node = TextNode("This is also a test node",TextType.LINK,"wwww.boot.dev")
        node2 = TextNode("This is also a test node",TextType.LINK,"wwww.boot.dev")
        self.assertEqual(node,node2)

    def test_different_url(self):
        node = TextNode("This is also a test node",TextType.LINK,"wwww.boot.dev")
        node2 = TextNode("This is also a test node",TextType.LINK,"wwww.fakeboot.dev")
        self.assertNotEqual(node,node2)

    def test_not_eq_url(self):
        node = TextNode("This is a test node",TextType.LINK)
        node2 = TextNode("This is a test node",TextType.LINK,"wwww.fakeboot.dev")
        self.assertNotEqual(node, node2)
if __name__ == "__main__":
    unittest.main()