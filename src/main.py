from textnode import TextNode,TextType

def main():
    tn = TextNode("This is a text",TextType.LINK,"www.projectu.com")
    print(tn)

main()