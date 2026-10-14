
import re

from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    pattern = r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        match_images = extract_markdown_images(old_node.text)
        if not match_images:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text

        for alt_text, url in match_images:
            image_markdown = f"![{alt_text}]({url})"
            sections = remaining_text.split(image_markdown, 1)
            if len(sections[0]) > 0:
                before_text = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(before_text)
            image_textnode = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(image_textnode)
            remaining_text = sections[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes
        
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        match_links = extract_markdown_links(old_node.text)
        if not match_links:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text

        for text, href in match_links:
            link_markdown = f"[{text}]({href})"
            sections = remaining_text.split(link_markdown, 1)
            if len(sections) != 2:
                raise IndexError("list index out of range")
            if len(sections[0]) > 0:
                before_text = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(before_text)
            link_textnode = TextNode(text, TextType.LINK, href)
            new_nodes.append(link_textnode)
            remaining_text = sections[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes