
import codecs
import struct

codec_name = 'pal_custom_codec'

map = { 'è' : 0xA940, 
        'é' : 0xA941, 
        'à' : 0xA942, 
        'ù' : 0xA943,
        'ê' : 0xA944,
        'ô' : 0xA945,
        'À' : 0xA946,
        'ç' : 0xA947,
        'î' : 0xA948,
        'ï' : 0xA949,
        'û' : 0xA94A,
        'œ' : 0xA94B,
        'É' : 0xA94C,
        'â' : 0xA94D,
        'Î' : 0xA94E,
        'Ê' : 0xA94F,
        '～' : 0xA950,
        'Ç': 0xA951,
        ' ​​': ' '
        #​0x200b : ' '
        }

class Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        output = bytearray()
        
        for char in input:
            if char in map.keys():
                if (map[char]>255):
                    output.extend(struct.pack('<H', map[char]))
                else:
                    output.extend(struct.pack('<B', map[char]))
            else:
                output.extend(char.encode("big5"))

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