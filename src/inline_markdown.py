from textnode import TextNode, TextType
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split = node.text.split(delimiter)
            if len(split)%2 == 0:
                raise ValueError("No closing delimeter")
            for index,value in enumerate(split):
                if index %2 !=0:
                    new_nodes.append(TextNode(value,text_type))
                else:
                    new_nodes.append(TextNode(value,TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
        else:
            image = extract_markdown_images(node.text)
            image_delims = [f"![{i[0]}]({i[1]})" for i in image]
            if image == []:
                split_nodes.append(TextNode(node.text,TextType.TEXT))
            else:
                remaining = node.text
                for delim, (alt,link) in zip(image_delims,image):
                    before,after = remaining.split(delim,1)
                    if before != "":
                        split_nodes.append(TextNode(before,TextType.TEXT))
                    split_nodes.append(TextNode(alt,TextType.IMAGE,link))
                    remaining = after
                if remaining != "":
                    split_nodes.append(TextNode(remaining,TextType.TEXT))
    return split_nodes




def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            link_delims = [f"[{link[0]}]({link[1]})" for link in links]
            if links == []:
                split_nodes.append(TextNode(node.text,TextType.TEXT))     
            else:
                remaining = node.text
                for delim, (alt,link) in zip(link_delims,links):
                    before,after = remaining.split(delim,1)
                    if before != "":
                        split_nodes.append(TextNode(before,TextType.TEXT))
                    split_nodes.append(TextNode(alt,TextType.LINK,link))
                    remaining = after
                if remaining != "":
                    split_nodes.append(TextNode(remaining,TextType.TEXT))
    return split_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    bold_done = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    italic_done = split_nodes_delimiter(bold_done,"_",TextType.ITALIC)
    code_done = split_nodes_delimiter(italic_done,"`",TextType.CODE)
    images_done = split_nodes_image(code_done)
    links_done = split_nodes_link(images_done)
    return links_done
