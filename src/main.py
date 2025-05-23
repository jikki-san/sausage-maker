from textnode import TextNode, TextType

from util import dir_copy


SOURCE = "static"
DEST = "public"


def main():
    dir_copy(SOURCE, DEST)


if __name__ == "__main__":
    main()
