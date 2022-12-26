from io import BufferedReader
import struct
from typing import Any, Literal, Tuple, Union

def readint(
    stream: BufferedReader,
    size: int,
    endian: Literal["little", "big"] = "little",
    signed: bool = False,
) -> int:
    return int.from_bytes(stream.read(size), byteorder=endian, signed=signed)

def readintoffset(
    stream: BufferedReader,
    offset: int,
    size: int,
    endian: Literal["little", "big"] = "little",
    signed: bool = False,
) -> int:
    return_offset = stream.tell()
    stream.seek(offset)
    output = readint(stream, size, endian, signed)
    stream.seek(return_offset)
    return output


def readintoffset(
    stream: BufferedReader,
    offset: int,
    size: int,
    endian: Literal["little", "big"] = "little",
    signed: bool = False,
) -> int:
    return_offset = stream.tell()
    stream.seek(offset)
    output = readint(stream, size, endian, signed)
    stream.seek(return_offset)
    return output


def readfloat(stream: BufferedReader) -> float:
    return struct.unpack("<f", stream.read(4))[0]


def readtextascii(
    stream: BufferedReader, encoding: str = "big5", raw: bool = False
) -> str | bytes:
    output = b""
    char2 = stream.read(2)
    while char2 != b'%Q':
        stream.seek(stream.tell()-2)
        char = stream.read(1)
        output += char
        char2 = stream.read(2)

    if raw:
        return output
    else:
        return output.decode("ascii")

def readtextbig5(
    stream: BufferedReader, encoding: str = "big5", raw: bool = False
) -> str | bytes:
    output = b""
    char2 = stream.read(2)
    while char2 != b'%Q':
        stream.seek(stream.tell()-2)
        char = stream.read(1)
        output += char
        char2 = stream.read(2)

    if raw:
        return output
    else:
        return output.decode("big5")

def readtextoffset(stream: BufferedReader, offset: int, encoding: str = "big5") -> str:
    return_offset = stream.tell()
    stream.seek(offset)
    output = readtext(stream, raw=True)
    stream.seek(return_offset)
    return output.decode(encoding)