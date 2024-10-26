from textnode import TextNode, TextType

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://google.com")
    print(text_node)

main()
