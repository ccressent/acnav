import unittest

from struct import error
from DAT.Block import Block, BlockChain


class TestBlock(unittest.TestCase):

    def test_parse_valid_blob(self):
        blob  = "\xEF\xBE\xAD\xDE"
        blob += 'A' * 252
        block = Block.from_blob(blob)

        self.assertEqual(block.size,              256)
        self.assertEqual(block.next_block_offset, 0xdeadbeef)
        self.assertEqual(block.data,              'A' * 252)

    def test_parse_invalid_blob(self):
        with self.assertRaises(error):
            Block.from_blob('A')


class TestBlockChain(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
