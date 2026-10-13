from enum import Enum

class TextType(Enum):
    PLAIN = "plain"
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




#text (plain)
#**Bold text**
#_Italic text_
#`Code text`
#Links, in this format: [anchor text](url)
#Images, in this format: ![alt text](url)