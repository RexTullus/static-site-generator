class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return_string = ""
        for key, value in self.props.items():
            return_string += f' {key}="{value}"'

        return return_string
    
    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, " 
                f"children={self.children}, props={self.props})")

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented  # Not comparable
        
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag}, value={self.value}, " 
                f", props={self.props})")

    def to_html(self):
        if self.value == None:
            raise ValueError("No value set")

        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag set")

        if self.children is None:
            raise ValueError("No children set")

        return_string = ""
        for child in self.children:
            return_string += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{return_string}</{self.tag}>"
    
