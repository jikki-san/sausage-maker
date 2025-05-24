class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[str] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(
            list(
                map(lambda key: f'{key}="{self.props[key]}"',
                    self.props)
            )
        )


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        if not self.tag:
            raise ValueError("all parent nodes must have a tag")
        if self.children is None:
            raise ValueError("all parent nodes must have children")
        child_tags = [node.to_html() for node in self.children]
        return f"<{self.tag}>{''.join(child_tags)}</{self.tag}>"
