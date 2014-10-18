import unittest

from struct import error
from DAT.Header import Header, HEADER_OFFSET


class TestParse(unittest.TestCase):

    def setUp(self):
        self.header = Header()

    def test_parse_valid_blob0(self):
        fp = open("tests/data/headers/header0.bin", "rb")
        fp.seek(HEADER_OFFSET)
        self.header.parse(fp.read())

        self.assertEqual(self.header.magic,            0x5442)
        self.assertEqual(self.header.block_size,       0x100)
        self.assertEqual(self.header.file_size,        0x14900000)
        self.assertEqual(self.header.file_version,     0x2)
        self.assertEqual(self.header.file_version2,    0x1)
        self.assertEqual(self.header.first_free_block, 0x14822b00)
        self.assertEqual(self.header.last_free_block,  0x14822900)
        self.assertEqual(self.header.free_block_count, 0xde1)
        self.assertEqual(self.header.root_offset,      0x1b77400)

    def test_parse_valid_blob1(self):
        fp = open("tests/data/headers/header1.bin", "rb")
        fp.seek(HEADER_OFFSET)
        self.header.parse(fp.read())

        self.assertEqual(self.header.magic,            0x5442)
        self.assertEqual(self.header.block_size,       0x400)
        self.assertEqual(self.header.file_size,        0x7f00000)
        self.assertEqual(self.header.file_version,     0x1)
        self.assertEqual(self.header.file_version2,    0x69466948)
        self.assertEqual(self.header.first_free_block, 0x7eac400)
        self.assertEqual(self.header.last_free_block,  0x7eabc00)
        self.assertEqual(self.header.free_block_count, 0x16b)
        self.assertEqual(self.header.root_offset,      0x6811800)

    def test_parse_valid_blob2(self):
        fp = open("tests/data/headers/header2.bin", "rb")
        fp.seek(HEADER_OFFSET)
        self.header.parse(fp.read())

        self.assertEqual(self.header.magic,            0x5442)
        self.assertEqual(self.header.block_size,       0x400)
        self.assertEqual(self.header.file_size,        0x100000)
        self.assertEqual(self.header.file_version,     0x3)
        self.assertEqual(self.header.file_version2,    0x1)
        self.assertEqual(self.header.first_free_block, 0x93400)
        self.assertEqual(self.header.last_free_block,  0xb8800)
        self.assertEqual(self.header.free_block_count, 0x113)
        self.assertEqual(self.header.root_offset,      0x2b000)

    def test_parse_valid_blob3(self):
        fp = open("tests/data/headers/header3.bin", "rb")
        fp.seek(HEADER_OFFSET)
        self.header.parse(fp.read())

        self.assertEqual(self.header.magic,            0x5442)
        self.assertEqual(self.header.block_size,       0x400)
        self.assertEqual(self.header.file_size,        0x35d00000)
        self.assertEqual(self.header.file_version,     0x1)
        self.assertEqual(self.header.file_version2,    0x0)
        self.assertEqual(self.header.first_free_block, 0x35cf7400)
        self.assertEqual(self.header.last_free_block,  0x35cf2400)
        self.assertEqual(self.header.free_block_count, 0x6d8)
        self.assertEqual(self.header.root_offset,      0x232d400)

    def test_parse_invalid_blob(self):
        with self.assertRaises(error):
            self.header.parse('A' * 10)


if __name__ == "__main__":
    unittest.main()
