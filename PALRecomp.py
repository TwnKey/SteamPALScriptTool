
import sys
import argparse
import struct
import os
import csv
import codecs 
import CustomCodec
from pathlib import Path
from lib.parser import readint, readintoffset, readtextoffset, count_text_bytes
import PALInstructionsSet   
from PALDecomp import parse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [CSV FILE] [BASE_DAT_FILE]...",
        description="Reinsert text into Chinese Paladin Steam ver (2001)"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('csv_file')
    parser.add_argument('dat_file')
    return parser


def recompile(csv_file, dat_file):
        filename = Path(csv_file).stem
        filesize = os.path.getsize(csv_file)
        PalDec = parse(dat_file)
        events = PalDec.events
        
        fh = open(dat_file, 'rb')
        out = bytearray(fh.read())
        start_addr = events[0].addr
        globaloffset = 0
        translations = []
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                dialog = row[2].replace("\n", "%N")
                lines = dialog.split("%N")
                
                
                TL = ""
                for i_l in range(0, len(lines)):
                    l = lines[i_l]
                    
                    if len(l)>32:
                        #if one line is too long, we will automatically put newlines in the remaining lines
                        
                        remaining = l
                        while (len(remaining) > 32):
                            l32 = remaining[0:31]
                            last_space_idx = l32.rindex(' ')
                            TL = TL + l32[0:last_space_idx] + "%N"
                            remaining = remaining[last_space_idx+1:len(remaining)]
                            
                        TL = TL + remaining
                        
                        
                    else:
                        TL = TL + l
                    if i_l < len(lines)-1:
                            TL = TL + "%N"
                translations.append(TL)
        
        
        idx_current_ptr = 0
        idx_current_evptr = 0
        if len(PalDec.text_addrs) != len(translations):
            raise Exception("CSV and dat file texts don't match")
        idx_text = 0
        offset_event_ptr = 0x200 #start_addr - len(PalDec.events) * 4
        #first we update with the pointers without inserting new bytes
        for text_addr in PalDec.text_addrs:
            for i in range(idx_current_ptr, len(PalDec.code_pointers)):
                ptr = PalDec.code_pointers[i]
                if (ptr.to > text_addr):
                    break
                idx_current_ptr += 1
                new_ptr_value = struct.pack('I',ptr.to + globaloffset)
                out[ptr.from_:ptr.from_+4] = new_ptr_value
                
            for i in range(idx_current_evptr, len(PalDec.events_pointers)):
                ptr = PalDec.events_pointers[i]
               
                if (ptr.to > text_addr):
                    break
                idx_current_evptr += 1
                new_ptr_value = struct.pack('I',ptr.to + globaloffset - offset_event_ptr )
                out[ptr.from_:ptr.from_+4] = new_ptr_value
            sz = count_text_bytes(text_addr, out) 
            text_addr = text_addr + globaloffset
            new_text_bytes = codecs.encode(translations[idx_text], "pal_custom_codec", "backslashreplace")
            globaloffset = globaloffset + len(new_text_bytes) - sz 
            idx_text = idx_text + 1
            
        globaloffset = 0    
        idx_text = 0        
        #then we insert the new bytes
        for text_addr in PalDec.text_addrs:
            
            text_addr = text_addr + globaloffset
            sz = count_text_bytes(text_addr, out) 
            new_text_bytes = codecs.encode(translations[idx_text], "pal_custom_codec", "backslashreplace")
            out[text_addr:text_addr+sz] = []
            out[text_addr:text_addr] = new_text_bytes
            
            globaloffset = globaloffset + len(new_text_bytes) - sz 
            idx_text = idx_text + 1
        with open("test.dat", "wb") as binary_file:
            # Write bytes to file
            binary_file.write(out)
        
        

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
    	
    if not args.dat_file or not args.csv_file:
        raise Exception("PALRecomp needs a file to recompile!")
    else:
        file = recompile(args.csv_file,args.dat_file)
        
        


if __name__ == "__main__":
    main()
