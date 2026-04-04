from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        # Check if tag is missing
        if self.tag is None:
            raise ValueError('Tag required to render HTML')
        
        # Check if children is missing
        if self.children is None or len(self.children) == 0:
            raise ValueError('Children required to render HTML')
            
        # Build the full string in HTML
        html_string = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html_string += child.to_html()
        return f'{html_string}</{self.tag}>'