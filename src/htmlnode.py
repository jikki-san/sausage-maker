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
