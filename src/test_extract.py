import unittest

from extract import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "![first image](first.png) and ![second image](second.png)"
        )
        self.assertListEqual(
            [("first image", "first.png"), ("second image", "second.png")],
            matches,
        )

    def test_extract_images_returns_empty_list_when_none_exist(self):
        matches = extract_markdown_images("There are no images here")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)")
        self.assertListEqual([("link", "https://www.google.com")], matches) 

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "Read [the docs](https://docs.example.com) or [the guide](guide.html)"
        )
        self.assertListEqual(
            [("the docs", "https://docs.example.com"), ("the guide", "guide.html")],
            matches,
        )

    def test_extract_links_does_not_include_images(self):
        matches = extract_markdown_links(
            "Visit [the site](https://example.com) and see ![the logo](logo.png)"
        )
        self.assertListEqual([("the site", "https://example.com")], matches)

    def test_extract_links_returns_empty_list_when_none_exist(self):
        matches = extract_markdown_links("There are no links here")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_link(self):
            node = TextNode(
                "This is text with an [link](https://google.com) and another [second link](https://twitch.tv)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://google.com"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second link", TextType.LINK, "https://twitch.tv"),
                ],
                new_nodes,
            )
    def test_link_no_starttest(self):
        node = TextNode(
             "[link](https://example.com) and some text",
             TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual([
             TextNode("link", TextType.LINK, "https://example.com"),
             TextNode(" and some text", TextType.TEXT)
        ],
        new_nodes
        )

    def test_image_no_starttest(self):
        node = TextNode(
            "![image](https://example.com) and some text",
            TextType.TEXT,
        )
    
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "https://example.com"),
            TextNode(" and some text", TextType.TEXT)
        ],
        new_nodes
        )
    def test_image_no_image(self):
        node = TextNode(
            "Only some text",
            TextType.TEXT,
        )
        
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Only some text", TextType.TEXT)
        ],
        new_nodes
        )

    def test_link_no_link(self):
        node = TextNode(
            "Only some text",
            TextType.TEXT,
        )
            
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Only some text", TextType.TEXT)
        ],
        new_nodes
        )

    def test_image_no_text(self):
        node = TextNode(
            "already bold [link](url)",
            TextType.BOLD,
        )
            
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("already bold [link](url)",TextType.BOLD,)
        ],
        new_nodes
        )

    def test_link_no_text(self):
        node = TextNode(
            "already bold [link](url)",
            TextType.BOLD,
        )
            
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("already bold [link](url)",TextType.BOLD,)
        ],
        new_nodes
        )

    def test_link_two_no_text_between(self):
        node = TextNode(
            "[first](https://a.com)[second](https://b.com)",
            TextType.TEXT,
        )
            
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("first",TextType.LINK,"https://a.com"),
            TextNode("second",TextType.LINK,"https://b.com")
        ],
        new_nodes
        )
    

if __name__ == "__main__":
	unittest.main()