import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    return extract_markdown(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"[^!]\[(.*?)\]\((.*?)\)"
    return extract_markdown(link_pattern, text)


def extract_markdown(pattern, text):
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for node in old_nodes:
        # split on the delimiter
        old_text_type = node.text_type
        if old_text_type == text_type:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) == 1:
            new_nodes.append(node)
        elif len(split_text) % 2 == 0:
            raise ValueError("Invalid Markdown; unmatched delimiter found")
        else:
            for i, s in enumerate(split_text):
                if s == "":
                    continue
                elif i % 2 == 0:
                    new_nodes.append(TextNode(s, old_text_type))
                else:
                    new_nodes.append(TextNode(s, text_type))

    return new_nodes
