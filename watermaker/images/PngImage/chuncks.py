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

class PngIHDR(PngChunck):
    IHDR_FIELDS = {
        'width': 4, 'height': 4,
        'bit_depth': 1, 'color_type': 1,
        'compression_method': 1, 'filter_method': 1,
        'interlace_method': 1
    }
    def __init__(self, lenght: bytes, chunck_type: bytes, data: bytes, crc: bytes) -> None:
        super().__init__(lenght, chunck_type, data, crc)
        cursor = 0
        for field, size in self.IHDR_FIELDS.items():
            setattr(self,'_'+field, self.data[cursor: cursor+size])
            cursor += size

    @property
    def width(self):
        return int.from_bytes(self._width, byteorder='big')
    
    @property
    def height(self):
        return int.from_bytes(self._height, byteorder='big')

    @property
    def bit_depth(self):
        return int.from_bytes(self._bit_depth, byteorder='big')
    
    @property
    def color_type(self):
        return int.from_bytes(self._color_type, byteorder='big')

    @property
    def compression_method(self):
        return int.from_bytes(self._compression_method, byteorder='big')
    
    @property
    def filter_method(self):
        return int.from_bytes(self._filter_method, byteorder='big')

    @property
    def interlace_method(self):
        return int.from_bytes(self._interlace_method, byteorder='big')

    def __repr__(self) -> str:
        return super().__repr__().replace('PngChunck', 'PngIHDRChunck')


class PngPLTE(PngChunck):
    def __init__(self, lenght: bytes, chunck_type: bytes, data: bytes, crc: bytes) -> None:
        super().__init__(lenght, chunck_type, data, crc)
    
    def __repr__(self) -> str:
        return super().__repr__().replace('PngChunck', 'PngPLTEChunck')


class PngIDAT(PngChunck):
    def __init__(self, lenght: bytes, chunck_type: bytes, data: bytes, crc: bytes) -> None:
        super().__init__(lenght, chunck_type, data, crc)
    
    def __repr__(self) -> str:
        return super().__repr__().replace('PngChunck', 'PngIDATChunck')


class PngIEND(PngChunck):
    def __init__(self, lenght: bytes, chunck_type: bytes, data: bytes, crc: bytes) -> None:
        super().__init__(lenght, chunck_type, data, crc)
    
    def __repr__(self) -> str:
        return super().__repr__().replace('PngChunck', 'PngIENDChunck')
