from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type:str, url:str | None = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        eq_text = self.text == other.text
        eq_type = self.text_type == other.text_type
        eq_url = self.url == other.url
        return eq_text and eq_type and eq_url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid texttype")

#text (plain)
#**Bold text**
#_Italic text_
#`Code text`
#Links, in this format: [anchor text](url)
#Images, in this format: ![alt text](url)