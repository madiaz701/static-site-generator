from textnode import TextNode, TextType


def main():
    dummy_node = TextNode('Dummy text', TextType.LINK, 'https://www.boot.dev')
    print(dummy_node)

if __name__ == "__main__":
    main()