class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        text = f''
        if self.props is None or len(self.props) <= 0:
            return ""
        for key in self.props.keys():
            text += f' {key}="{self.props[key]}"'
        return text
    
    def __repr__(self):
        return f"Tag : {self.tag}\n Value: {self.value}\n Children: {self.children}\n Props: {self.props}"
