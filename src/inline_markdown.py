import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    return extract_markdown(image_pattern, text)


def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return extract_markdown(link_pattern, text)


def extract_markdown(pattern, text):
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for img_alt, img_url in images:
            first_text, rest = current_text.split(
                f"![{img_alt}]({img_url})", 1)
            if first_text != "":
                new_nodes.append(TextNode(first_text, old_node.text_type))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))
            current_text = rest
        if rest != "":
            new_nodes.append(TextNode(rest, old_node.text_type))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for text, url in links:
            first_text, rest = current_text.split(
                f"[{text}]({url})", 1)
            if first_text != "":
                new_nodes.append(TextNode(first_text, old_node.text_type))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = rest
        if rest != "":
            new_nodes.append(TextNode(rest, old_node.text_type))
    return new_nodes


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
