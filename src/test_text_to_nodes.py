import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNode(unittest.TestCase):
    def test_many_texttypes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    
    def test_empty_text(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_plain_text(self):
        self.assertEqual(
            text_to_textnodes("Just plain text!"),
            [TextNode("Just plain text!", TextType.TEXT)],
        )

    def test_bold_text(self):
        self.assertEqual(
            text_to_textnodes("Before **bold** after"),
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_italic_text(self):
        self.assertEqual(
            text_to_textnodes("Before _italic_ after"),
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_code_text(self):
        self.assertEqual(
            text_to_textnodes("Run `print('hello')` now"),
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("print('hello')", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_link(self):
        self.assertEqual(
            text_to_textnodes("Visit [Boot.dev](https://boot.dev) today"),
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" today", TextType.TEXT),
            ],
        )

    def test_image(self):
        self.assertEqual(
            text_to_textnodes("Look at ![cat](https://example.com/cat.png)!"),
            [
                TextNode("Look at ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_adjacent_formatted_nodes(self):
        self.assertEqual(
            text_to_textnodes("**bold**_italic_`code`"),
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_repeated_bold_sections(self):
        self.assertEqual(
            text_to_textnodes("**first** between **second**"),
            [
                TextNode("first", TextType.BOLD),
                TextNode(" between ", TextType.TEXT),
                TextNode("second", TextType.BOLD),
            ],
        )

    def test_multiple_links_and_images(self):
        self.assertEqual(
            text_to_textnodes(
                "[one](https://one.test) ![first](https://img.test/1.png) "
                "[two](https://two.test) ![second](https://img.test/2.png)"
            ),
            [
                TextNode("one", TextType.LINK, "https://one.test"),
                TextNode(" ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://img.test/1.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://two.test"),
                TextNode(" ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://img.test/2.png"),
            ],
        )

    def test_unclosed_delimiters(self):
        for text in (
            "start **unclosed",
            "start _unclosed",
            "start `unclosed",
        ):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    text_to_textnodes(text)

    def test_whitespace_and_newlines(self):
        self.assertEqual(
            text_to_textnodes("Line 1\n**line 2**\n  line 3"),
            [
                TextNode("Line 1\n", TextType.TEXT),
                TextNode("line 2", TextType.BOLD),
                TextNode("\n  line 3", TextType.TEXT),
            ],
        )

    

if __name__ == "__main__":
    unittest.main()