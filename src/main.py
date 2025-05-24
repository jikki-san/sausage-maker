from gen_pages import generate_pages_recursive
from util import dir_copy


SOURCE = "static"
DEST = "public"


def main():
    dir_copy(SOURCE, DEST)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
