from splitdelimiter import split_nodes_delimiter
from extract import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_textnodes(text: str):
    first_node = [TextNode(text, TextType.TEXT)]
    image_split = split_nodes_image(first_node)
    link_split = split_nodes_link(image_split)
    bold_split = split_nodes_delimiter(link_split, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    return split_nodes_delimiter(italic_split, "`", TextType.CODE)
