import unittest

from blocknode import BlockNode, BlockType

class TestBlockNode(unittest.TestCase):
    def test_blocknode_creation(self):
        block = BlockNode("Hello world", BlockType.PARAGRAPH)
        self.assertEqual(block.text, "Hello world")
        self.assertEqual(block.block_type, BlockType.PARAGRAPH)

    def test_blocknode_repr(self):
        block = BlockNode("Heading 1", BlockType.HEADING)
        rep = repr(block)
        self.assertIn("Heading 1", rep)
        self.assertIn("BlockType.HEADING", rep)

    def test_different_blocktypes(self):
        for btype in BlockType:
            block = BlockNode(f"Test {btype.name}", btype)
            self.assertEqual(block.block_type, btype)
            self.assertIn(btype.name, block.text)

if __name__ == "__main__":
    unittest.main()
