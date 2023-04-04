
import sys
import argparse
import struct
import os
from pathlib import Path
from lib.parser import readint, readintoffset, readtextoffset
import PALInstructionsSet
import operator
from hanziconv import HanziConv
def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Extract text from items table"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('file')
    return parser

class Item:
    def __init__(self, name):
        self.events = events
        self.text_addrs = addr_texts
        self.code_pointers = pointers
        self.events_pointers = ev_ptrs
        
        
def to_signed(unsigned):
    signed_value = unsigned
    if(signed_value & 0x80000000):
        signed_value = -0x100000000 + signed_value
    return signed_value
def parse(act_file):
        fh = open(act_file, 'rb')
        item_data = bytearray(fh.read())
        filesize = len(item_data)
        current_addr = 0x200
        count = 0
        while(current_addr < filesize):
            current_int = struct.unpack('I',item_data[current_addr : current_addr + 4])[0]
            current_int_signed = to_signed(current_int)
            #print(hex(current_addr) , " " ,hex(current_int))
            #print(hex(current_addr), " ", hex(current_int))
            #if (current_addr > 0x2000):
            #    break
            if ((0x7effffff < current_int_signed) and ((current_int & 0xfff) != 0)):
                #print("AT : ", hex(current_addr))
                pass
            #    current_addr += 12
            #el
            if (current_int_signed < 0x7f000000):
                current_addr += 4
            elif (current_int == 0x7f00ffff):
                current_addr += 4
            elif ((((current_int & 0xffff) < 0xf000) or ((current_int_signed & 0xf0000) >> 0x10 == 0)) or
         (current_int == 0x7f00ffff)):
                current_addr += 4
                current_int = struct.unpack('I',item_data[current_addr : current_addr + 4])[0]
                local_3c = current_int
                signed_value = to_signed(local_3c)
                
                if (signed_value < 0x7f000000):
                    iVar1 = -1
                elif (local_3c == 0):
                    iVar1 = 0
                else:
                    iVar1 = (local_3c & 0xffff) >> 0xc
                        
                while (local_3c != 0x7f00ffff) and (iVar1 == -1):
                    current_addr += 4
                    local_3c = struct.unpack('I',item_data[current_addr : current_addr + 4])[0]
                    signed_value = to_signed(local_3c)
                    
                    if (signed_value < 0x7f000000):
                        iVar1 = -1
                    elif (local_3c == 0):
                        iVar1 = 0
                    else:
                        iVar1 = (local_3c & 0xffff) >> 0xc
  
                    
         
            else:
                current_addr += 4
                offset = 0
                #if current_int == 0x7FF2F000:
                #    offset = 0
                if current_int == 0x7FF2F027:
                    offset = 0x12
                current_addr += offset
                start = current_addr
                b1 = item_data[current_addr]
                b2 = item_data[current_addr + 1]
                str_ = []
                #print(hex(current_addr),"reading text at ", hex(current_addr))
                while((b1 != 0x25) or (b2 != 0x25)):
                    
                    current_addr += 1
                    b1 = item_data[current_addr]
                    b2 = item_data[current_addr + 1]
                    
                current_addr += 2    
                str_ = item_data[start : current_addr-2]    
                CN = HanziConv.toSimplified(str_.decode("big5",errors='replace')).replace("%N","\n")
                print(hex(current_addr), " ", CN)
                
            
            
            
            
            
            
        

def write(filename, PALDec):
    file_str = ""
    for event in PALDec.events:
        for instr in event.instructions:
            file_str = file_str + instr.to_string()
    with open(filename +".csv",'w', encoding="utf-8") as f:
        f.write(file_str)

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
    	
    if not args.file:
        raise Exception("PalItem needs a file to decompile!")
    else:
        
        parse(args.file)
        
        
        


if __name__ == "__main__":
    main()
