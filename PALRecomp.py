
import sys
import argparse
import struct
import os
import csv
import codecs 
import CustomCodec
from hanziconv import HanziConv
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

class dialog:
    def __init__(self, TL, parameters):
        self.TL = TL
        self.params = []
        for i in range(0, len(parameters)):
            if (parameters[i]!= ""):
                self.params.append(int(parameters[i]))

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
        index_row = 0
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                TL = dialog(row[1].replace("\n", "%N"), row[2:])
                translations.append(TL)
                index_row += 1
        
        
        idx_current_ptr = 0
        idx_current_evptr = 0
        if len(PalDec.text_addrs) != len(translations):
            raise Exception("CSV and dat file texts don't match")
        idx_text = 0
        offset_event_ptr = 0x200
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
            new_text_bytes = codecs.encode(translations[idx_text].TL, "pal_custom_codec", "backslashreplace")
            
            globaloffset = globaloffset + len(new_text_bytes) - sz 
            idx_text = idx_text + 1
            
        globaloffset = 0    
        idx_text = 0        
        #then we insert the new bytes
        for text_addr in PalDec.text_addrs:
            text_addr = text_addr + globaloffset
            sz = count_text_bytes(text_addr, out) 
            new_text_bytes = codecs.encode(translations[idx_text].TL, "pal_custom_codec", "backslashreplace")
            
            out[text_addr:text_addr+sz] = []
            #print("Removing " + hex(sz) + " bytes at addr " + hex(text_addr))
            #print("Adding " + hex(len(new_text_bytes)) + " bytes at addr " + hex(text_addr) + "global offset " + hex(globaloffset))
            for idx_param in range(0, len(translations[idx_text].params)):
                param_value = translations[idx_text].params[idx_param]
                param_bytes = struct.pack('H',param_value)
                offset = 2 * (len(translations[idx_text].params) - idx_param)
                
                out[text_addr - offset:text_addr - offset + 2] = param_bytes
                
            out[text_addr:text_addr] = new_text_bytes
            
            
            globaloffset = globaloffset + len(new_text_bytes) - sz 
            idx_text = idx_text + 1
        with open("out.dat", "wb") as binary_file:
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
