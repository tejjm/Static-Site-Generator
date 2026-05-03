import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_link

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

    def test_split_code_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                  TextNode("code block", TextType.CODE),
                  TextNode(" word", TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE),expected)

        
    def test_split_bold_delimeter(self):
        node = TextNode("This is a text with a **bold words right here,**which ended now",TextType.TEXT)
        expected = [TextNode("This is a text with a ",TextType.TEXT),
                    TextNode("bold words right here,",TextType.BOLD),
                    TextNode("which ended now",TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node],"**",TextType.BOLD),expected)
        
    def test_split_code_italic_delimeter(self):
        node = TextNode("This is a text with a _italic words right here,_which ended now",TextType.TEXT)
        expected = [TextNode("This is a text with a ",TextType.TEXT),
                    TextNode("italic words right here,",TextType.ITALIC),
                    TextNode("which ended now",TextType.TEXT),]
        self.assertEqual(split_nodes_delimiter([node],"_",TextType.ITALIC),expected)

    def test_split_code_inavlid(self):
        node = TextNode("This is a text with a _italic words right here,which ended now",TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node],"_",TextType.ITALIC)

    def test_split_code_non_text(self):
        node = TextNode("_This is a text with a italic words right here,which ended now_",TextType.ITALIC)
        expected = [TextNode("_This is a text with a italic words right here,which ended now_",TextType.ITALIC)]
        self.assertEqual(split_nodes_delimiter([node],"_",TextType.ITALIC),expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_text_miltiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual([("to boot dev","https://www.boot.dev"),("to youtube","https://www.youtube.com/@bootdotdev")],matches)


    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![uwu](https://uwu.com/uwu.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("uwu","https://uwu.com/uwu.png")], matches)


    def test_extract_invalid_with_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_images(text)
        self.assertEqual([],matches)



    def test_extract_invalid_with_text(self):
        text =  "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![uwu](https://uwu.com/uwu.png)"
        matches = extract_markdown_links(text)
        self.assertEqual([],matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot.dev](https://boot.dev) and to [youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and to ", TextType.TEXT),
                TextNode(
                    "youtube", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_split_no_image(self):
            node = TextNode(
            "This is just a text",
            TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is just a text", TextType.TEXT),
                ],new_nodes)
            
    def test_split_no_link(self):
            node = TextNode(
            "This is just a text",
            TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is just a text", TextType.TEXT),
                ],new_nodes)
            
    def test_split_links_no_before(self):
        node = TextNode(
            "[to boot.dev](https://boot.dev) and to [youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and to ", TextType.TEXT),
                TextNode(
                    "youtube", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )


    def test_split_images_no_before(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_split_images_back_to_back(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_non_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.LINK,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.LINK,
        )]
        ,
        new_nodes,
        )

