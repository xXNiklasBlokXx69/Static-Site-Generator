import unittest

from splitdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
	def test_split_bold_text(self):
		old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]

		result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

		self.assertEqual(
			result,
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("bold", TextType.BOLD),
				TextNode(" text", TextType.TEXT),
			],
		)

	def test_split_multiple_formatted_sections(self):
		old_nodes = [TextNode("**bold** and **more bold**", TextType.TEXT)]

		result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

		self.assertEqual(
			result,
			[
				TextNode("bold", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("more bold", TextType.BOLD),
			],
		)

	def test_preserves_non_text_nodes(self):
		old_node = TextNode("already italic", TextType.ITALIC)

		result = split_nodes_delimiter([old_node], "**", TextType.BOLD)

		self.assertEqual(result, [old_node])

	def test_raises_for_unclosed_delimiter(self):
		old_nodes = [TextNode("This is **unclosed", TextType.TEXT)]

		with self.assertRaises(ValueError):
			split_nodes_delimiter(old_nodes, "**", TextType.BOLD)


if __name__ == "__main__":
	unittest.main()
