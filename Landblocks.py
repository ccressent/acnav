from struct import unpack_from, calcsize

class SurfaceObjectsBlock:
    """
    These entries contain a list of the objects located on the surface world.
    Their ID is always of the form xxyyFFFE.

    Format:
    uint32_t id
    uint32_t unknown (related to number of dungeon blocks?)
    uint32_t number of objects
    Object   objects[number of objects]
    uint32_t number of other objects
    ???????? other_objects[number of other objects]
    """

    def __init__(self, blob):
        pos = 0

        (
        self.id,
        self.unk1,
        self.number_objects
        ) = unpack_from("III", blob)
        pos += calcsize("III")

        self.objects = []
        for i in range(0, self.number_objects):
            self.objects.append(Object(blob[pos:pos + calcsize("Ifffffff")]))
            pos += calcsize("Ifffffff")

        self.number_other_objects = unpack_from("I", blob[pos:])[0]
        pos += calcsize("I")

        self.other_objects = []
        for i in range(0, self.number_other_objects):
            self.other_objects.append(Object(blob[pos:pos + calcsize("Ifffffff")]))
            pos += calcsize("Ifffffff")

    def __repr__(self):
        s  = "{id: "             + str(hex(self.id))
        s += ", unk1: "          + str(hex(self.unk1))
        s += ", objects: "       + str(self.number_objects)
        s += " "                 + str([o for o in self.objects])
        s += ", other objects: " + str(self.number_other_objects)
        s += " "                 + str([o for o in self.other_objects])
        s += "}"

        return s


class Object:
    """
    Cell.dat object.

    The id is the id of the file describing that object in portal.dat.
    (x,y,z) is the translation (position) of the specified object in the
    landblock.
    (a,b,c,d) is the unit quaternion a + bi + cj + dk specifying the rotation
    of the object.

    The first 8 words of the other objects in the file start the same way as
    regular objects but have a bunch of other information afterwards, of
    varying length. It may have something to do with visibility.

    Format:
    uint32_t id
    float x
    float y
    float z
    float a
    float b
    float c
    float d
    """

    def __init__(self, blob):
        (
        self.id,
        self.x,
        self.y,
        self.z,
        self.a,
        self.b,
        self.c,
        self.d
        ) = unpack_from("Ifffffff", blob)

    def __repr__(self):
        s  = "{id: " + str(hex(self.id))
        s += ", x: " + str(self.x)
        s += ", y: " + str(self.y)
        s += ", z: " + str(self.z)
        s += ", a: " + str(self.a)
        s += ", b: " + str(self.b)
        s += ", c: " + str(self.c)
        s += ", d: " + str(self.d)
        s += "}"

        return s


class DungeonBlock:
    """
    Contains information for one block in the dungeon.
    Their ID is in the form xxyynnnn where nnnn starts at 0x0100 and increments
    for each block of the dungeon.

    Format:
    uint32_t id
    uint32_t type
    uint32_t id (why repeated?)
    uint8_t  number of textures
    uint8_t  number of connections
    uint16_t number of visible dungeon blocks?
    uint16_t texture_id[number of textures]
    uint16_t pad if number of textures is odd?
    uint32_t dungeon block geometry id
    float    x
    float    y
    float    z
    float    a
    float    b
    float    c
    float    d
    uint64_t connectivity_info[number of connections]
    uint16_t visible_blocks[number of visible blocks]?
    uint16_t pad if the number of visible blocks is off?
    uint32_t number of objects
    Object   objects[number of objects]

    If bit 1 of type is set then the dungeon is a surface stucture.
    If bit 2 of type is set then the dungeon block contains objects.
    If bit 2 of type is not set then the number of objects and the object
    fields are not present.

    The texture IDs are actually 0x08000000 + texture ID.
    They reference texture information files in portal.dat.

    The dungeon block geometry IDs are actually 0x0d000000 + geometry ID.
    They reference files in portal.dat.

    (x,y,z) is the translation of the dungeon block.
    (a,b,c,d) is its rotation.
    """

    def __init__(self, blob):

        pos = 0

        (
        self.id,
        self.type,
        self.id,
        self.number_textures,
        self.number_connections,
        self.number_visible_blocks,
        ) = unpack_from("IIIBBH", blob)
        pos += calcsize("IIIBBH")

        self.texture_id = []
        for i in range(0, self.number_textures):
            texture_id = 0x8000000 + unpack_from("H", blob[pos:])[0]
            self.texture_id.append(texture_id)
            pos += calcsize("H")

        self.geometry_id = 0xd000000 + unpack_from("I", blob[pos:])[0]
        pos += calcsize("I")

        (
        self.x,
        self.y,
        self.z,
        self.a,
        self.b,
        self.c,
        self.d
        ) = unpack_from("fffffff", blob[pos:])
        pos += calcsize("fffffff")

        self.connectivity_info = []
        for i in range(0, self.number_connections):
            info = unpack_from("Q", blob[pos:])[0]
            self.connectivity_info.append(info)
            pos += calcsize("Q")

        self.visible_blocks = []
        for i in range(0, self.number_visible_blocks):
            block_id = (self.id & 0xffff0000) + unpack_from("H", blob[pos:])[0]
            self.visible_blocks.append(block_id)
            pos += calcsize("H")

        self.number_objects = 0
        self.objects = []

        if (self.type & 0x2):
            self.number_objects = unpack_from("I", blob[pos:])[0]
            pos += calcsize("I")

            self.Object = []
            for i in range(0, self.number_objects):
                self.objects.append(Object(blob[pos:pos + calcsize("Ifffffff")]))
                pos += calcsize("Ifffffff")

    def __repr__(self):
        s  = "{id: "              + str(hex(self.id))
        s += ", type: "           + str(hex(self.type))
        s += ", geometry_id: "    + str(hex(self.geometry_id))
        s += ", translation: "    + str([self.x, self.y, self.z])
        s += ", rotation: "       + str([self.a, self.b, self.c, self.d])
        s += ", textures: "       + str(int(self.number_textures))
        s += " "                  + str([hex(x) for x in self.texture_id])
        s += ", connections: "    + str(int(self.number_connections))
        s += " "                  + str(self.connectivity_info)
        s += ", visible_blocks: " + str(int(self.number_visible_blocks))
        s += " "                  + str([hex(x) for x in self.visible_blocks])
        s += ", objects: "        + str(self.number_objects)
        s += " "                  + str([o for o in self.objects])
        s += "}"

        return s


class TopographyBlock:
    """
    Contains the surface topography of a landblock.
    Their ID is of the form xxyyFFFF.
    """
    def __init__(self, blob):
        pos = 0

        (
        self.id,
        self.hasObjects,
        ) = unpack_from("II", blob)
        pos += calcsize("II")

        self.hasObjects = bool(self.hasObjects)

        self.topography = []
        for i in range(0, 81):
            self.topography.append(Topography(blob[pos:pos+2]))
            pos += 2

        self.z = []
        for i in range(0, 9*9):
            z = unpack_from("B", blob[pos:])[0]
            self.z.append(z)
            pos += calcsize("B")

    def __repr__(self):
        s  = "{id: "          + str(hex(self.id))
        s += ", hasObjects: " + str(self.hasObjects)
        s += ", topography: " + str([t for t in self.topography])
        s += ", z: "          + str([z for z in self.z])
        s += "}"

        return s


class Topography:
    """
    Contains road information, terrain type and vegetation.

    Format:
    uint8_t:1 Set if this cell is a road
    uint8_t:1 Very rare, but if set, this cell is a road
    uint8_t:6 Terrain type
    uint8_t   Vegetation
    """
    def __init__(self, blob):
        topography = unpack_from("H", blob)[0]
        self.isRoad = bool(topography & 0x8000)
        self.isRareRoad = bool(topography & 0x4000)
        self.terrain = topography & 0x3F00
        self.vegetation = topography & 0x00FF

    def __repr__(self):
        s  = "{isRoad: "      + str(self.isRoad)
        s += ", isRareRoad: " + str(self.isRareRoad)
        s += ", terrain: "    + str(hex(self.terrain))
        s += ", vegetation: " + str(hex(self.vegetation))
        s += "}"

        return s
