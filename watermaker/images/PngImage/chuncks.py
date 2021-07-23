class PngChunck:
    """
    Each chunk consists of four parts:

    Length:
        A 4-byte unsigned integer giving the number of bytes in the chunk's data field. The length counts only the data field.
    Chunk Type:
        A 4-byte chunk type code. For convenience in description and in examining PNG files.
    Chunk Data:
        The data bytes appropriate to the chunk type, if any. This field can be of zero length.
    CRC:
        A 4-byte CRC (Cyclic Redundancy Check) calculated on the preceding bytes in the chunk.
    """    
    def __init__(self, lenght: bytes, chunck_type: bytes, data: bytes, crc: bytes) -> None:
        self.lenght:bytearray = lenght
        self.type:bytearray = chunck_type
        self.data:bytearray = data
        self.crc:bytes = crc
    
    @property
    def int_lenght(self):
        return int.from_bytes(self.lenght, byteorder='big')
    
    @property
    def type_as_str(self):
        return str(self.type)[2:-1]
    
    @property
    def full_chunck(self):
        return self.lenght + self.type +  self.data  + self.crc


    def __repr__(self) -> str:
        return "<Class PngChunck lenght: %d, Type: %s, CRC: %s>" % (
            self.int_lenght, self.type_as_str, self.crc
        )

