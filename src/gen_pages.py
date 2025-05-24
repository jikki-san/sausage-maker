import os

from block_markdown import extract_title
from markdown_to_html import markdown_to_htmlnode


def generate_pages_recursive(base_path, content_path, template_path, dest_path):
    if os.path.isfile(content_path):
        _, file_name = os.path.split(content_path)
        file_name, ext = file_name.split(".")
        if ext != "md":
            raise ValueError("improper file format")
        dest_path, _ = os.path.split(dest_path)
        generate_page(base_path, content_path, template_path,
                      os.path.join(dest_path, f"{file_name}.html"))
        return
    for item in os.listdir(content_path):
        new_content_path = os.path.join(content_path, item)
        new_dest_path = os.path.join(dest_path, item)
        generate_pages_recursive(
            base_path, new_content_path, template_path, new_dest_path)


def generate_page(base_path, from_path, template_path, dest_path):
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
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    dest_path_dir = os.path.dirname(dest_path)
    if dest_path_dir != "":
        os.makedirs(dest_path_dir, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)
