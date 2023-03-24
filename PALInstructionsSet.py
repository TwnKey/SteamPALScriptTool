import sys
from lib.parser import readint, readintoffset, readtextoffset, readtextascii,readtextbig5
from hanziconv import HanziConv
from deep_translator import GoogleTranslator


#Pas terrible, mais bon
text_addrs = []
pointers = []
pointers_avec_offset = []



def add_normal_ptr(instr, stream):
    global pointers
    to = readint(stream, 4)
    if (to != 0xFF00FF00):
        pointers.append(pointer(stream.tell() - 4, to))
        instr.operands.append(operand(to, "pointeur"))
        return True
    else:
        #stream.seek(stream.tell()-4)
        return False
def add_offset_ptr(instr, stream): #regular pointer but with an unexplainable offset of 0x200
    global pointers_avec_offset
    to = readint(stream, 4)
    if (to != 0xFF00FF00):
        pointers_avec_offset.append(pointer(stream.tell() - 4, to + 0x200))
        instr.operands.append(operand(to, "pointeur"))
        return True
    else:
        #stream.seek(stream.tell()-4)
        return False

def OP_0(instr, stream):
    global text_addrs
    
    addr = stream.tell()
    
    offset = 0
    if ((instr.op_code + 1) < 3):
        offset = 4
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
    elif ((instr.op_code + 1) < 7):
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
    elif (((instr.op_code + 1) == 0x59) or ((instr.op_code + 1) == 0x5A)):
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
    
    text_addrs.append(stream.tell())
    text = readtextbig5(stream, raw = True)
    instr.operands.append(operand(text,"text"))
    

def OP_9(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_DE(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_3C(instr, stream):
    pass 
def OP_42(instr, stream):
    pass 
def OP_401(instr, stream):
    pass      
def OP_C3(instr, stream):
    pass   
def OP_33(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))

def OP_42(instr, stream):
    value1 = readint(stream, 2)
    instr.operands.append(operand(value1))
def OP_44(instr, stream):
    value1 = readint(stream, 2)
    instr.operands.append(operand(value1))
def OP_1A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_1B(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))

def OP_C1(instr, stream):
    txt = readtextascii(stream)
    instr.operands.append(operand(txt))
def OP_C2(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_DF(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_3A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_3D(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_64(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_D(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_B1(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_13(instr, stream):
    count = readint(stream, 2) & 0x3FFF
    for i in range(0, count): 
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
def OP_12(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_26(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_4C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_4D(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_15(instr, stream):
    
    instr.operands.append(operand(readint(stream, 2)))
    add_offset_ptr(instr, stream)
def OP_14(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    add_offset_ptr(instr, stream)
def OP_46(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_47(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_75(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_74(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_39(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_D7(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_50(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_D8(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_4F(instr, stream):
    pass
def OP_30F(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_63(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_91(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_77(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_CD(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_C9(instr, stream):
    global pointers_avec_offset
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    
    add_offset_ptr(instr, stream)
    
def OP_18(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_4B(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_FFFE(instr, stream):
    pass
def OP_11(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_6A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_7F(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_8(instr, stream):
    pass
def OP_7(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_2C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_DD(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_308(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_309(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_71(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_27(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_DC(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_A2(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_CB(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_30A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_6F(instr, stream):
    pass
def OP_1C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_88(instr, stream):
    pass
def OP_6(instr, stream):
    pass
def OP_68(instr, stream):
    pass
def OP_67(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_A8(instr, stream):
    count = readint(stream, 2) & 0x3FFF
    for i in range(0, count): 
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
def OP_73(instr, stream):
    count = readint(stream, 2)
    for i in range(0, count): 
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
        instr.operands.append(operand(readint(stream, 2)))
def OP_19(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_9F(instr, stream):
    pass
def OP_36(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_7A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_45(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))

    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_31(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))

    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_48(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))

    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_32(instr, stream):
    pass
def OP_5E(instr, stream):
    pass
def OP_35(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_5D(instr, stream):
    pass
def OP_8A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_30B(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_40(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_41(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_10(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_30C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_CE(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_17(instr, stream):
    current = readint(stream, 2) 
    while current != 0xFF00:
        instr.operands.append(operand(current))
        current = readint(stream, 2)
        
    add_offset_ptr(instr, stream)

def OP_69(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_80(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_3E(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    current = readint(stream, 2)
    while current != 0xFF00:
        instr.operands.append(operand(current))
        current = readint(stream, 2)
def OP_3F(instr, stream):
    pass
def OP_34(instr, stream):
    pass
def OP_83(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_E(instr, stream):
    add_offset_ptr(instr, stream)
def OP_4E(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))

def OP_4A(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_C5(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_30E(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_20(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_CA(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    res = add_offset_ptr(instr, stream)
    while res:
        res = add_offset_ptr(instr, stream)
def OP_B5(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_B7(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_CF(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_28(instr, stream):
    res = add_offset_ptr(instr, stream)
    while res:
        res = add_offset_ptr(instr, stream)
def OP_311(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_F(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_16(instr, stream):
    current = readint(stream, 2) 
    while current != 0xFF00:
        instr.operands.append(operand(current))
        current = readint(stream, 2)
    add_offset_ptr(instr, stream)
def OP_8C(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_A4(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_1F(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    add_offset_ptr(instr, stream)
def OP_82(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_8F(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_56(instr, stream):
    res = add_offset_ptr(instr, stream)
    while res:
        res = add_offset_ptr(instr, stream)
def OP_B0(instr, stream):
    pass
def OP_D6(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
def OP_89(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_8E(instr, stream):
    pass
def OP_8D(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_7D(instr, stream):
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
    instr.operands.append(operand(readint(stream, 2)))
def OP_D3(instr, stream):
    pass
instruction_set = {0 : OP_0,
                   1 : OP_0,
                   2 : OP_0,
                   3 : OP_0,
                   4 : OP_0,
                   5 : OP_0,
                   6 : OP_6,
                   7 : OP_7,
                   8 : OP_8,
                   9 : OP_9,
                   10 : OP_A,
                   0x0C : OP_C,
                   0x0D : OP_D,
                   0x0E : OP_E,
                   0x0F : OP_F,
                   0x10 : OP_10,
                   0x12 : OP_12,
                   0x13 : OP_13,
                   0x14 : OP_14,
                   0x15 : OP_15,
                   0x16 : OP_16,
                   0x17 : OP_17,
                   0x18 : OP_18,
                   0x1C : OP_1C,
                   0x1D : OP_1C,
                   0x1E : OP_1C,
                   0x1F : OP_1F,
                   0x20 : OP_20,
                   0xE4 : OP_A,
                   0xDF : OP_DF,
                   0xE3 : OP_9,
                   0xDE : OP_DE,
                   0x59 : OP_0,
                   0x58 : OP_0,
                   0x401 : OP_401,
                   0x402 : OP_401,
                   0x92 : OP_401,
                   0x11 : OP_11,
                   0x19 : OP_19,
                   0x1A : OP_1A,
                   0x1B : OP_1B,
                   0x25 : OP_42,
                   0x26 : OP_26,
                   0x27 : OP_27,
                   0x28 : OP_28,
                   0x2C : OP_2C,
                   0x31 : OP_31,
                   0x32 : OP_32,
                   0x33 : OP_33,
                   0x34 : OP_34,
                   0x35 : OP_35,
                   0x36 : OP_36,
                   0x37 : OP_36,
                   0x38 : OP_36,
                   0x39 : OP_39,
                   0x3D : OP_3D,
                   0x3E : OP_3E,
                   0x3F : OP_3F,
                   0x40 : OP_40,
                   0x41 : OP_41,
                   0x42 : OP_42,
                   0x43 : OP_42,
                   0x44 : OP_44,
                   0x45 : OP_45,
                   0x46 : OP_46,
                   0x47 : OP_47,
                   0x48 : OP_48,
                   0x4A : OP_4A,
                   0x4B : OP_4B,
                   0x4C : OP_4C,
                   0x4D : OP_4D,
                   0x4E : OP_4E,
                   0x4F : OP_4F,
                   0x50 : OP_50,
                   0x56 : OP_56,
                   0x5D : OP_5D,
                   0x5E : OP_5E,
                   0x63 : OP_63,
                   0x64 : OP_64,
                   0x69 : OP_69,
                   0x74 : OP_74,
                   0x75 : OP_75,
                   0x7F : OP_7F,
                   0x98 : OP_39,
                   0x3A : OP_3A,

                   0x3B : OP_3C,
                   0x3C : OP_3C,
                   0xA8 : OP_A8,
                   0xB0 : OP_B0,
                   0xB1 : OP_B1,
                   0xB4 : OP_1C,
                   0xB5 : OP_B5,
                   0xB6 : OP_B5,
                   0xB7 : OP_B7,
                   0xB8 : OP_20,
                   0xC1 : OP_C1,
                   0xC2 : OP_C2,
                   0xC3 : OP_C3,
                   0xC4 : OP_C2,
                   0xD7 : OP_D7,
                   0xD8 : OP_D8,
                   
                   0x63 : OP_63,
                   0x65: OP_91,
                   0x66: OP_91,
                   0x67: OP_67,
                   0x68: OP_68,
                   0x69: OP_69,
                   0x6A: OP_6A,
                   0x6F: OP_6F,
                   0x71: OP_71,
                   0x73: OP_73,
                   0x74: OP_91,
                   0x76: OP_8A,
                   0x7A: OP_7A,
                   0x7D: OP_7D,
                   0x7E: OP_7D,
                   0x80: OP_80,
                   0x81: OP_80,
                   0x82: OP_82,
                   0x83: OP_83,
                   0x87: OP_91,
                   0x88: OP_88,
                   0x89: OP_89,
                   0x8A: OP_8A,
                   0x8b: OP_91,
                   0x8c: OP_8C,
                   0x8D: OP_8D,
                   0x8E: OP_8E,
                   0x8F: OP_8F,
                   0x90: OP_91,
                   0x91: OP_91,
                   0x99 : OP_69,
                   0xad: OP_91,
                   0x77: OP_77,
                   0x9F: OP_9F,
                   0xA2: OP_A2,
                   0xA3: OP_A2,
                   0xA4: OP_A4,
                   0xA5: OP_A4,
                   0xA6: OP_80,
                   0xA7: OP_80,
                   
                   0xC5: OP_C5,
                   0xC6: OP_C5,
                   0xC7: OP_C9,
                   0xC8: OP_C9,
                   0xC9: OP_C9,
                   0xCA: OP_CA,
                   0xCB: OP_CB,
                   0xCD: OP_CD,
                   0xCE: OP_CE,
                   0xCF: OP_CF,
                   0xD2 : OP_D3,
                   0xD3 : OP_D3,
                   0xD6 : OP_D6,
                   0xDC : OP_DC,
                   0xDD: OP_DD,
                   0xE2: OP_2C,
                   0xE1 : OP_27,
                   0xE7 : OP_27,
                   0xFFFE: OP_FFFE,
                   0x308 : OP_308,
                   0x309 : OP_309,
                   0x30A : OP_30A,
                   0x30B : OP_30B,
                   0x30C : OP_30C,
                   0x30E : OP_30E,
                   0x30F : OP_30F,
                   0x311 : OP_311,
                   
}
class operand:
    def __init__(self, value, type = "u16"):
        self.value = value
        self.type = type
        
class pointer:
    def __init__(self, addr_from, addr_to):
        self.from_ = addr_from
        self.to = addr_to
        
class event:
    def __init__(self, addr, instrs):
        self.instructions = instrs
        self.addr = addr


class instruction(object):
    """description of class"""
    def __init__(self, stream, op_code):
        self.addr = stream.tell() - 2 #minus opcode
        self.op_code = op_code - 1
        self.operands = []
        self.name = ""

        #print(hex(self.op_code ), " ", hex(stream.tell()-2))
        instruction_set[self.op_code](self, stream)
    def to_string(self):
        result = ""
        #result = str(self.addr) + " " + hex(self.op_code) + " "
        
        for op in self.operands:
            if op.type == "text":
                
                CN = HanziConv.toSimplified(op.value.decode("big5",errors='replace')).replace("%N","\n")
                FR = ""#GoogleTranslator(source='zh-CN', target='fr').translate(CN)
                text_ = "\"" + CN + "\"" + "," + "\"" + FR + "\"" 
                parameters = ""
                if len(self.operands)-1 == 6:
                    parameters += str(self.operands[0].value) + ", "
                    parameters += str(self.operands[1].value) + ", "
                    parameters += str(self.operands[2].value) + ", "
                    parameters += str(self.operands[3].value) + ", "
                    parameters += str(self.operands[4].value) + ", "
                    parameters += str(self.operands[5].value)
                elif len(self.operands)-1 == 4:
                    parameters += str(self.operands[0].value) + ", "
                    parameters += str(self.operands[1].value) + ", "
                    parameters += str(self.operands[2].value) + ", "
                    parameters += str(self.operands[3].value)
                elif len(self.operands)-1 == 2:
                    parameters += str(self.operands[0].value) + ", "
                    parameters += str(self.operands[1].value)
                result = result + text_ + "," + parameters + "\n"
            #else:
            #    result = result + str(op.value) + " "
        #result = result + ",\n"
        return result 
      
