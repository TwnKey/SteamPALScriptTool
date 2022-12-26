
import sys
import argparse
import struct
import os
from pathlib import Path
from lib.parser import readint, readintoffset, readtextoffset
from PALInstructionsSet import instruction

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Disassembles and reassembles ED9 script files (EXPERIMENTAL)."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('file')
    return parser



def parse(path):
        filename = Path(path).stem
        filesize = os.path.getsize(path)

        stream = open(path, "rb")
        stream.seek(0x200)
        first_part_pointers = [];
        second_part_pointers = [];
        nb_first_part = readint(stream, 4)
        if (nb_first_part != 0xFFFFFFFF):
            for i in range(0,nb_first_part-1):
                first_part_pointers.append(readint(stream, 4))
        
        first_ptr = readint(stream, 4) + 0x200
        second_part_pointers.append(first_ptr)
        while (stream.tell() < first_ptr):
            second_part_pointers.append(readint(stream, 4) + 0x200)
        all_list = first_part_pointers + second_part_pointers 
        all_list.sort()
        #for the moment I'll parse everything in one go, not caring about the pointers at the beginning
        instructions = []
        while (stream.tell() < filesize):
            instr = instruction(stream, readint(stream, 2))
            instructions.append(instr)
        file_str = ""
        for instr in instructions:
            file_str = file_str + instr.to_string()
        with open(filename +".csv",'w', encoding="utf-8") as f:
            f.write(file_str)



def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
    	
    if not args.file:
        raise Exception("PALDecomp needs a file to decompile!")
    else:
        file = parse(args.file)
        
        


if __name__ == "__main__":
    main()
