
import sys
import argparse
import struct
import os
from pathlib import Path
from lib.parser import readint, readintoffset, readtextoffset
import PALInstructionsSet
import operator

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Extract text from Chinese Paladin Steam ver (2001)"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('file')
    return parser

class PALDecompiler:
    def __init__(self, pointers, addr_texts, events, ev_ptrs):
        self.events = events
        self.text_addrs = addr_texts
        self.code_pointers = pointers
        self.events_pointers = ev_ptrs
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
        second_part_pointers.append(PALInstructionsSet.pointer(stream.tell() - 4, first_ptr))
        list_event_ptrs = []
        while (stream.tell() < first_ptr):
            dest = readint(stream, 4) + 0x200
            second_part_pointers.append(PALInstructionsSet.pointer(stream.tell()-4, dest))
            list_event_ptrs.append(dest)
        #the first section has pointers but likely located before any code, so it is fine to keep them as is.
        #second part likely contains pointers to events (didn't make sure though). those need to be edited.
        events = []
        current_event = PALInstructionsSet.event(stream.tell(), [])
        while (stream.tell() < filesize):
            
            addr = stream.tell() 
            instr = PALInstructionsSet.instruction(stream, readint(stream, 2))
            if list_event_ptrs.count(addr) > 0:
                instr.pointed_to = True 
                if (len(current_event.instructions)>0):
                    events.append(current_event)
                    current_event = PALInstructionsSet.event(addr, [])
            else:
                instr.pointed_to = False
            current_event.instructions.append(instr)
            
        PALInstructionsSet.pointers.sort(key=operator.attrgetter('to'))
        
        second_part_pointers = second_part_pointers + PALInstructionsSet.pointers_avec_offset
        second_part_pointers.sort(key=operator.attrgetter('to'))
        
        events.sort(key=operator.attrgetter('addr'))
        return PALDecompiler(PALInstructionsSet.pointers, PALInstructionsSet.text_addrs, events, second_part_pointers)

def write(filename, PALDec):
    file_str = ""
    idx_ev = 0
    for event in PALDec.events:
        #file_str = file_str + str(idx_ev) + "\"EVENT\";\n"
        idx_ev += 1
        for instr in event.instructions:
            file_str = file_str + instr.to_string()
    with open(filename +".csv",'w', encoding="utf-8") as f:
        f.write(file_str)

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
    	
    if not args.file:
        raise Exception("PALDecomp needs a file to decompile!")
    else:
        
        Paldec = parse(args.file)
        filename = Path(args.file).stem
        write(filename, Paldec)
        
        


if __name__ == "__main__":
    main()
