import sys


from gen_pages import generate_pages_recursive
from util import dir_copy


STATIC_SOURCE = "static"
CONTENT_SOURCE = "content"
DEST = "docs"
TEMPLATE_FILE = "template.html"


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    dir_copy(STATIC_SOURCE, DEST)
    generate_pages_recursive(base_path, CONTENT_SOURCE,
                             TEMPLATE_FILE, DEST)


if __name__ == "__main__":
    main()
