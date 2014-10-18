"""
Parse DAT files blocks and traverse block chains.
"""

from binascii import hexlify
from struct import unpack_from

from DAT.Header import Header


class Block:
    """
    A block making up a chunk of a Directory in a DAT file.
    """

    def __init__(self, filename=None, offset=None, size=None, next_block_offset=None, data=None):
        self.filename          = filename
        self.offset            = offset
        self.size              = size
        self.next_block_offset = next_block_offset
        self.data              = data

    def parse(self, blob):
        """
        Try to parse a block structure out of the given binary blob.
        """
        self.data              = unpack_from(str(len(blob[4:])) + "s", blob[4:])[0]
        self.next_block_offset = unpack_from("I", blob)[0]

    @classmethod
    def from_blob(cls, blob):
        """
        Return a new Block instance initialized with the result of parsing the
        given binary blob.
        """
        b = cls()
        b.parse(blob)
        b.size = len(blob)
        return b

    @classmethod
    def from_file(cls, filename, offset):
        """
        Return a new Block instance initialized with the result of parsing the
        given file at the given offset.
        """
        with open(filename, "rb") as fp:
            h = Header.from_file(filename)
            fp.seek(offset)
            blob = fp.read(h.block_size)

        b = cls.from_blob(blob)
        b.filename = filename
        b.offset = offset
        return b

    def __iter__(self):
        return BlockIterator(self)

    def __str__(self):
        s  = "{filename: " + str(self.filename)
        s += ", offset: "  + str(hex(self.offset))
        s += ", size: "    + str(hex(self.size))
        s += ", next: "    + str(hex(self.next_block_offset))
        s += ", data: "    + hexlify(self.data)
        s += "}"

        return s


class BlockIterator:

    def __init__(self, first_block):
        self.current_block  = first_block
        self.no_more_blocks = False

    def __iter__(self):
        return self

    def next(self):
        if self.no_more_blocks:
            raise StopIteration()
        else:
            if self.current_block.next_block_offset == 0x0:
                self.no_more_blocks = True

            b = self.current_block
            filename = self.current_block.filename
            next_block_offset = self.current_block.next_block_offset
            self.current_block = Block.from_file(filename, next_block_offset)
            return b


class BlockChain:
    """
    The result of traversing a series of Block starting at the given Block.
    The data held by a BlockChain can be parsed into a Directory.
    """

    def __init__(self, start_block):
        self.size = 0
        self.data = ""

        for block in iter(start_block):
            self.size += block.size
            self.data += block.data

    def __str__(self):
        s  = "{size: "  + str(self.size)
        s += ", data: " + hexlify(self.data)
        s += "}"

        return s
