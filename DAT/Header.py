"""
Parse DAT file headers and perform various operations on them.
"""

from struct import unpack_from

HEADER_OFFSET = 320
HEADER_SIZE = 36
HEADER_MAGIC = 0x5442

class Header:
    """
    The header found at the beginning of a DAT file.
    """

    def __init__(self, filename=None, magic=None,
                       block_size=None, file_size=None,
                       file_version=None, file_version2=None,
                       first_free_block=None, last_free_block=None,
                       root_offset=None):
        self.filename         = filename
        self.magic            = magic
        self.block_size       = block_size
        self.file_size        = file_size
        self.file_version     = file_version
        self.file_version2    = file_version2
        self.first_free_block = first_free_block
        self.last_free_block  = last_free_block
        self.root_offset      = root_offset

    def parse(self, blob):
        """
        Try to parse a header structure out of the first HEADER_SIZE bytes of
        the given binary blob.
        """
        (
        self.magic,
        self.block_size,
        self.file_size,
        self.file_version,
        self.file_version2,
        self.first_free_block,
        self.last_free_block,
        self.free_block_count,
        self.root_offset
        ) = unpack_from(9 * "I", blob)

    @classmethod
    def from_blob(cls, blob):
        """
        Return a new Header instance initialized with the result of parsing the
        given binary blob.
        """
        h = cls()
        h.parse(blob)
        return h

    @classmethod
    def from_file(cls, filename):
        """
        Return a new Header instance initialized with the result of parsing the
        HEADER_SIZE bytes at HEADER_OFFSET in the given file
        """
        with open(filename, 'rb') as fp:
            fp.seek(HEADER_OFFSET)
            blob = fp.read(HEADER_SIZE)

        h = cls.from_blob(blob)
        h.filename = filename
        return h

    def is_valid(self):
        """
        Check if various details of the header make sense: magic, free blocks,
        root offset, ...
        """
        if self.magic != HEADER_MAGIC:
            return False

        if (self.root_offset         > self.file_size
            or self.first_free_block > self.file_size
            or self.last_free_block  > self.file_size):
            return False

        return True

    def __str__(self):
        s  = "{filename: "          + str(self.filename)
        s += ", magic: "            + str(hex(self.magic))
        s += ", block_size: "       + str(hex(self.block_size))
        s += ", file_size: "        + str(hex(self.file_size))
        s += ", file_version: "     + str(hex(self.file_version))
        s += ", file_version2: "    + str(hex(self.file_version2))
        s += ", first_free_block: " + str(hex(self.first_free_block))
        s += ", last_free_block: "  + str(hex(self.last_free_block))
        s += ", free_block_count: " + str(hex(self.free_block_count))
        s += ", root_offset: "      + str(hex(self.root_offset))
        s += "}"

        return s
