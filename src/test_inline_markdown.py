import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images,extract_markdown_links,split_nodes_image,split_nodes_link,text_to_textnodes





class TestHTMLNode(unittest.TestCase):


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



    def test_text_textnode_regular(self):
        text = "This is **bold** and _italic_ and `code` with a ![cat](https://example.com/cat.png) and a [site](https://example.com)"
        expected = [TextNode("This is ",TextType.TEXT),
                    TextNode("bold",TextType.BOLD),
                    TextNode(" and ",TextType.TEXT),
                    TextNode("italic",TextType.ITALIC),
                    TextNode(" and ",TextType.TEXT),
                    TextNode("code",TextType.CODE),
                    TextNode(" with a ",TextType.TEXT),
                    TextNode("cat",TextType.IMAGE,"https://example.com/cat.png"),
                    TextNode(" and a ",TextType.TEXT),
                    TextNode("site",TextType.LINK,"https://example.com")
                    ]   
        self.assertEqual(text_to_textnodes(text),expected)

    def test_text_just_text(self):
        text = "This is a text"
        expected = [TextNode(text,TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text),expected)

