from .chuncks import PngChunck, PngIHDR, PngPLTE, PngIDAT, PngIEND


class PngImage:
    SIGNATURE_PNG =  bytes([137, 80, 78, 71, 13, 10, 26, 10])
    CHUNCK_PARTS = {
        'lenght': 4,
        'type': 4,
        'data': None,
        'crc': 4,
    }
    CRITICAL_CHUNCKS = {
        'IHDR': PngIHDR,
        'PLTE': PngPLTE,
        'IDAT': PngIDAT,
        'IEND': PngIEND,
    }

    def __init__(self, image_data: bytes) -> None:
        self.chuncks = []
        if image_data[:len(self.SIGNATURE_PNG)] != self.SIGNATURE_PNG:
            raise IOError("File ins't signed as png")
        image_unsigned_data = image_data[8:]
        cursor = 0
        while True:
            chunck_data = dict()
            for part, size in self.CHUNCK_PARTS.items() :
                if not size:
                    size = int.from_bytes(chunck_data['lenght'], byteorder='big')
                part_data = image_unsigned_data[cursor: cursor + size]
                chunck_data[part] = part_data
                cursor += size
            chunck = self.CRITICAL_CHUNCKS.get(str(chunck_data['type'])[2:-1], PngChunck)(
                chunck_data['lenght'], chunck_data['type'],
                chunck_data['data'], chunck_data['crc']
            )
            self.chuncks.append(chunck)
            if type(chunck) == self.CRITICAL_CHUNCKS['IEND']:
                break
        self.IHDR = self.chuncks[0]
        self.IEND = self.chuncks[-1]
    
    @property
    def width(self):
        return self.IHDR.width
    
    @property
    def height(self):
        return self.IHDR.height

    @property
    def bit_depth(self):
        return self.IHDR.bit_depth
    
    @property
    def color_type(self):
        return self.IHDR.color_type

    @property
    def compression_method(self):
        return self.IHDR.compression_method
    
    @property
    def filter_method(self):
        return self.IHDR.filter_method

    @property
    def interlace_method(self):
        return self.IHDR.interlace_method
