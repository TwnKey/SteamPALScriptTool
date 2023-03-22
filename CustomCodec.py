
import codecs
import struct

codec_name = 'pal_custom_codec'

map = { 'è' : 0x40A9, 
        'é' : 0x41A9, 
        'à' : 0x42A9, 
        'ù' : 0x43A9,
        'ê' : 0x44A9,
        'ô' : 0x45A9,
        'À' : 0x46A9,
        'ç' : 0x47A9,
        'î' : 0x48A9,
        'ï' : 0x49A9,
        'û' : 0x4AA9,
        'œ' : 0x4BA9,
        'É' : 0x4CA9,
        'â' : 0x4DA9,
        'Î' : 0x4EA9,
        'Ê' : 0x4FA9,
        '～' : 0x50A9,
        'Ç': 0x51A9,
        ' ​​': ' ',
        '»': 0x52A9,
        '«': 0x53A9,
        #​0x200b : ' '
        }

class Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        output = bytearray()
        
        for char in input:
            try:
                if char in map.keys():
                    if (map[char]>255):
                        output.extend(struct.pack('<H', map[char]))
                    else:
                        output.extend(struct.pack('<B', map[char]))
                else:
                    output.extend(char.encode("big5"))
            except Exception as inst:
                print(input)
                print(inst)
                #bytes([20]), len(output)
                raise
        return bytes(output), len(output)
        #return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors='strict'):
        return codecs.charmap_decode(input, errors, decoding_map)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_map)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return codecs.charmap_decode(input, self.errors, decoding_map)[0]


class StreamReader(Codec, codecs.StreamReader):
    pass

class StreamWriter(Codec, codecs.StreamWriter):
    pass


def _register(encoding):
    if encoding == codec_name:
        return codecs.CodecInfo(
            name=codec_name,
            encode=Codec().encode,
            decode=Codec().decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamreader=StreamReader,
            streamwriter=StreamWriter)

codecs.register(_register)