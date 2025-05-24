import os

from block_markdown import extract_title
from markdown_to_html import markdown_to_htmlnode
from util import dir_copy


SOURCE = "static"
DEST = "public"


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page {dest_path} from {from_path} using {template_path}")
    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    title, content = extract_title(markdown), markdown_to_htmlnode(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content.to_html())

    dest_path_dir = os.path.dirname(dest_path)
    if dest_path_dir != "":
        os.makedirs(dest_path_dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


def main():
    dir_copy(SOURCE, DEST)
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
