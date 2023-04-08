
import sys
import argparse
import struct
import os
from pathlib import Path
from lib.parser import readint, readintoffset, readtextoffset, count_text_bytes
import PALInstructionsSet
import operator
from hanziconv import HanziConv
from PALRecomp import dialog
import csv
import codecs 
import CustomCodec
from pathlib import Path
from GFileExtract import parse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Extract text from items table"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 0.0"
    )
    
    parser.add_argument('csv_file')
    parser.add_argument('g_dat_file')
    parser.add_argument('geindex_file')
    return parser

    return signed_value
 


file_ids = {
"gitem" : 7,
"gfight1" : 0,
"gfight2" : 1,
"gfight3" : 2,
"gfight4" : 3,
"ghero" : 4,
"gmon" : 5,
"glevel" : 6,
"gitem" : 7,
"gmagic" : 8,
"gmap" : 9,
}
 
reverse_file_ids = {v: k for k, v in file_ids.items()}

def parse_geindex(content):
    current_addr = 0
    count = struct.unpack('I',content[current_addr : current_addr + 4])[0]
    current_addr+=4
    ukn = {} #Je sais pas ce que c'est.
    for i in range(0, count):
        uk = struct.unpack('I',content[current_addr : current_addr + 4])[0]
        current_addr+=4
        id_ = struct.unpack('I',content[current_addr : current_addr + 4])[0]
        current_addr+=4
        ukn[id_] = uk
        
    current_addr += 4
    cnt = struct.unpack('I',content[current_addr : current_addr + 4])[0]
   
    current_addr += 8
    ptr_by_files = {
    }
    while (current_addr < len(content)):
        
        if (cnt == 1):
            
            current_int = struct.unpack('I',content[current_addr : current_addr + 4])[0]
            
            size = 4
            
            current_addr += (4 * size)
            cnt = struct.unpack('I',content[current_addr : current_addr + 4])[0]
            if (cnt == 0):
                break
            current_addr += 8
        current_int = struct.unpack('I',content[current_addr : current_addr + 4])[0]
        current_addr+=4    
        
        size = 4
        current_addr += 4
        addr_ptr = current_addr
        ptr = struct.unpack('I',content[current_addr : current_addr + 4])[0]
        current_addr += 4
        file_id = struct.unpack('I',content[current_addr : current_addr + 4])[0]
        if (file_id not in ptr_by_files.keys()):
            ptr_by_files[file_id] = []
        ptr_by_files[file_id].append(PALInstructionsSet.pointer(addr_ptr, ptr))
        current_addr += (4 * (size-2))
        
        cnt-=1
    for file in ptr_by_files.keys():
        ptr_by_files[file].sort(key=operator.attrgetter('to'))
    return ptr_by_files

def recompile(csv_file, dat_file, geindex):
        dat_key = filename = Path(dat_file).stem
        [out_str, text_addresses] = parse(dat_file)


        filename = Path(csv_file).stem
        filesize = os.path.getsize(csv_file)
        
        fh = open(dat_file, 'rb')
        out = bytearray(fh.read())
        
        fh2 = open(geindex, 'rb')
        out_idx = bytearray(fh2.read())
        ptr_by_files = parse_geindex(out_idx)
        
        ptrs_in_file = ptr_by_files[file_ids[dat_key]]
       
        translations = []
        index_row = 0
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                TL = dialog(row[1].replace("\n", "%N"), row[2:])
                translations.append(TL)
                index_row += 1
        
        if len(text_addresses) != len(translations):
            raise Exception("CSV and dat file texts don't match")
        
        globaloffset = 0    
        idx_text = 0 
        current_idx_geindex = 0        
        #then we insert the new bytes
        for text_addr in text_addresses:
            if (current_idx_geindex < len(ptrs_in_file)):
                
                while(ptrs_in_file[current_idx_geindex].to < text_addr):
                    new_ptr = ptrs_in_file[current_idx_geindex].to + globaloffset
                    new_ptr_bytes = struct.pack('I',new_ptr)
                    out_idx[ptrs_in_file[current_idx_geindex].from_:ptrs_in_file[current_idx_geindex].from_+4] = new_ptr_bytes
                    current_idx_geindex += 1
                    if (current_idx_geindex >= len(ptrs_in_file)): 
                        break
            text_addr = text_addr + globaloffset
            sz = count_text_bytes(text_addr, out, b'%%') 
            new_text_bytes = codecs.encode(translations[idx_text].TL, "pal_custom_codec", "backslashreplace")
            if (len(new_text_bytes) > 0):
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
        with open("geindex.dat", "wb") as binary_file:
            # Write bytes to file
            binary_file.write(out_idx)
            

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
    	
    if not args.csv_file or not args.g_dat_file or not args.geindex_file:
        raise Exception("GFileInsert needs a csv file, a geindex file and a g dat file!")
    else:
        
        recompile(args.csv_file,args.g_dat_file,args.geindex_file)
        
        
        


if __name__ == "__main__":
    main()
