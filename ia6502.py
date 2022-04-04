#!/usr/bin/env python3

#TODO: Kowalski cant do LDA 3+(4)
#TODO: SET and XSET
#TODO: double check all debug_msgs removed
#TODO: more comments
#TODO: array.insert to clean up code
#TODO: screen refresh very noticeable
#TODO: highight whole expression if out of range?
#TODO: generate byte for LDA #
#TODO; partial effects on flags even if unknown - blank better than ?

#Start here:
#TODO: ZPR
#TODO: labels
#TODO: branches
#TODO: .set
from sys import path, argv
from sys import exit
import curses

#Generated from spreadsheet - edit there and copy here
OP_INFO={

0x0:("BRK","IMP",1,7,"","","","","BDI","none"),
0x1:("ORA","IZX",2,6,"","","","","NZ","none"),
0x4:("TSB","ZP",2,5,"Yes","","","","Z","none"),
0x5:("ORA","ZP",2,3,"","","","","NZ","none"),
0x6:("ASL","ZP",2,5,"","","","","NZC","none"),
0x7:("RMB0","ZP",2,5,"Yes","","","","none","none"),
0x8:("PHP","IMP",1,3,"","","","","none","none"),
0x9:("ORA","IMMED",2,2,"","","","","NZ","none"),
0xA:("ASL","IMP",1,2,"","","","","NZC","none"),
0xC:("TSB","ABS",3,6,"Yes","","","","Z","none"),
0xD:("ORA","ABS",3,4,"","","","","NZ","none"),
0xE:("ASL","ABS",3,6,"","","","","NZC","none"),
0xF:("BBR0","ZPR",3,5,"Yes","","","","none","none"),
0x10:("BPL","REL",2,2,"","Yes","Yes","","none","N"),
0x11:("ORA","IZY",2,5,"","Yes","","","NZ","none"),
0x12:("ORA","IZP",2,5,"Yes","","","","NZ","none"),
0x14:("TRB","ZP",2,5,"Yes","","","","Z","none"),
0x15:("ORA","ZPX",2,4,"","","","","NZ","none"),
0x16:("ASL","ZPX",2,6,"","","","","NZC","none"),
0x17:("RMB1","ZP",2,5,"Yes","","","","none","none"),
0x18:("CLC","IMP",1,2,"","","","","C","none"),
0x19:("ORA","ABSY",3,4,"","Yes","","","NZ","none"),
0x1A:("INC","IMP",1,2,"Yes","","","","NZ","none"),
0x1C:("TRB","ABS",3,6,"Yes","","","","Z","none"),
0x1D:("ORA","ABSX",3,4,"","Yes","","","NZ","none"),
0x1E:("ASL","ABSX",3,6,"","Yes","","","NZC","none"),
0x1F:("BBR1","ZPR",3,5,"Yes","","","","none","none"),
0x20:("JSR","ABS",3,6,"","","","","none","none"),
0x21:("AND","IZX",2,6,"","","","","NZ","none"),
0x24:("BIT","ZP",2,3,"","","","","NVZ","none"),
0x25:("AND","ZP",2,3,"","","","","NZ","none"),
0x26:("ROL","ZP",2,5,"","","","","NZC","C"),
0x27:("RMB2","ZP",2,5,"Yes","","","","none","none"),
0x28:("PLP","IMP",1,4,"","","","","NVBDIZC","none"),
0x29:("AND","IMMED",2,2,"","","","","NZ","none"),
0x2A:("ROL","IMP",1,2,"","","","","NZC","C"),
0x2C:("BIT","ABS",3,4,"","","","","NVZ","none"),
0x2D:("AND","ABS",3,4,"","","","","NZ","none"),
0x2E:("ROL","ABS",3,6,"","","","","NZC","C"),
0x2F:("BBR2","ZPR",3,5,"Yes","","","","none","none"),
0x30:("BMI","REL",2,2,"","Yes","Yes","","none","N"),
0x31:("AND","IZY",2,5,"","Yes","","","NZ","none"),
0x32:("AND","IZP",2,5,"Yes","","","","NZ","none"),
0x34:("BIT","ZPX",2,4,"Yes","","","","NVZ","none"),
0x35:("AND","ZPX",2,4,"","","","","NZ","none"),
0x36:("ROL","ZPX",2,6,"","","","","NZC","C"),
0x37:("RMB3","ZP",2,5,"Yes","","","","none","none"),
0x38:("SEC","IMP",1,2,"","","","","C","C"),
0x39:("AND","ABSY",3,4,"","Yes","","","NZ","none"),
0x3A:("DEC","IMP",1,2,"Yes","","","","NZ","none"),
0x3C:("BIT","ABSX",3,4,"Yes","Yes","","","NVZ","none"),
0x3D:("AND","ABSX",3,4,"","Yes","","","NZ","none"),
0x3E:("ROL","ABSX",3,6,"","Yes","","","NZC","C"),
0x3F:("BBR3","ZPR",3,5,"Yes","","","","none","none"),
0x40:("RTI","IMP",1,6,"","","","","NVDIZC","none"),
0x41:("EOR","IZX",2,6,"","","","","NZ","none"),
0x45:("EOR","ZP",2,3,"","","","","NZ","none"),
0x46:("LSR","ZP",2,5,"","","","","NZC","none"),
0x47:("RMB4","ZP",2,5,"Yes","","","","none","none"),
0x48:("PHA","IMP",1,3,"","","","","none","none"),
0x49:("EOR","IMMED",2,2,"","","","","NZ","none"),
0x4A:("LSR","IMP",1,2,"","","","","NZC","none"),
0x4C:("JMP","ABS",3,3,"","","","","none","none"),
0x4D:("EOR","ABS",3,4,"","","","","NZ","none"),
0x4E:("LSR","ABS",3,6,"","","","","NZC","none"),
0x4F:("BBR4","ZPR",3,5,"Yes","","","","none","none"),
0x50:("BVC","REL",2,2,"","Yes","Yes","","none","V"),
0x51:("EOR","IZY",2,5,"","Yes","","","NZ","none"),
0x52:("EOR","IZP",2,5,"Yes","","","","NZ","none"),
0x55:("EOR","ZPX",2,4,"","","","","NZ","none"),
0x56:("LSR","ZPX",2,6,"","","","","NZC","none"),
0x57:("RMB5","ZP",2,5,"Yes","","","","none","none"),
0x58:("CLI","IMP",1,2,"","","","","I","none"),
0x59:("EOR","ABSY",3,4,"","Yes","","","NZ","none"),
0x5A:("PHY","IMP",1,3,"Yes","","","","none","none"),
0x5D:("EOR","ABSX",3,4,"","Yes","","","NZ","none"),
0x5E:("LSR","ABSX",3,6,"","Yes","","","NZC","none"),
0x5F:("BBR5","ZPR",3,5,"Yes","","","","none","none"),
0x60:("RTS","IMP",1,6,"","","","","none","none"),
0x61:("ADC","IZX",2,6,"","","","Yes","NVZC","C"),
0x64:("STZ","ZP",2,3,"Yes","","","","none","none"),
0x65:("ADC","ZP",2,3,"","","","Yes","NVZC","C"),
0x66:("ROR","ZP",2,5,"","","","","NZC","C"),
0x67:("RMB6","ZP",2,5,"Yes","","","","none","none"),
0x68:("PLA","IMP",1,4,"","","","","NZ","none"),
0x69:("ADC","IMMED",2,2,"","","","Yes","NVZC","C"),
0x6A:("ROR","IMP",1,2,"","","","","NZC","C"),
0x6C:("JMP","IND",3,6,"","","","","none","none"),
0x6D:("ADC","ABS",3,4,"","","","Yes","NVZC","C"),
0x6E:("ROR","ABS",3,6,"","","","","NZC","C"),
0x6F:("BBR6","ZPR",3,5,"Yes","","","","none","none"),
0x70:("BVS","REL",2,2,"","Yes","Yes","","none","V"),
0x71:("ADC","IZY",2,5,"","Yes","","Yes","NVZC","C"),
0x72:("ADC","IZP",2,5,"Yes","","","Yes","NVZC","C"),
0x74:("STZ","ZPX",2,4,"Yes","","","","none","none"),
0x75:("ADC","ZPX",2,4,"","","","Yes","NVZC","C"),
0x76:("ROR","ZPX",2,6,"","","","","NZC","C"),
0x77:("RMB7","ZP",2,5,"Yes","","","","none","none"),
0x78:("SEI","IMP",1,2,"","","","","I","none"),
0x79:("ADC","ABSY",3,4,"","Yes","","Yes","NVZC","C"),
0x7A:("PLY","IMP",1,4,"Yes","","","","NZ","none"),
0x7C:("JMP","IAX",3,6,"Yes","","","","none","none"),
0x7D:("ADC","ABSX",3,4,"","Yes","","Yes","NVZC","C"),
0x7E:("ROR","ABSX",3,6,"","Yes","","","NZC","C"),
0x7F:("BBR7","ZPR",3,5,"Yes","","","","none","none"),
0x80:("BRA","REL",2,3,"Yes","Yes","","","none","none"),
0x81:("STA","IZX",2,6,"","","","","none","none"),
0x84:("STY","ZP",2,3,"","","","","none","none"),
0x85:("STA","ZP",2,3,"","","","","none","none"),
0x86:("STX","ZP",2,3,"","","","","none","none"),
0x87:("SMB0","ZP",2,5,"Yes","","","","none","none"),
0x88:("DEY","IMP",1,2,"","","","","NZ","none"),
0x89:("BIT","IMMED",2,2,"Yes","","","","Z","none"),
0x8A:("TXA","IMP",1,2,"","","","","NZ","none"),
0x8C:("STY","ABS",3,4,"","","","","none","none"),
0x8D:("STA","ABS",3,4,"","","","","none","none"),
0x8E:("STX","ABS",3,4,"","","","","none","none"),
0x8F:("BBS0","ZPR",3,5,"Yes","","","","none","none"),
0x90:("BCC","REL",2,2,"","Yes","Yes","","none","C"),
0x91:("STA","IZY",2,6,"","","","","none","none"),
0x92:("STA","IZP",2,5,"Yes","","","","none","none"),
0x94:("STY","ZPX",2,4,"","","","","none","none"),
0x95:("STA","ZPX",2,4,"","","","","none","none"),
0x96:("STX","ZPY",2,4,"","","","","none","none"),
0x97:("SMB1","ZP",2,5,"Yes","","","","none","none"),
0x98:("TYA","IMP",1,2,"","","","","NZ","none"),
0x99:("STA","ABSY",3,5,"","","","","none","none"),
0x9A:("TXS","IMP",1,2,"","","","","none","none"),
0x9C:("STZ","ABS",3,4,"Yes","","","","none","none"),
0x9D:("STA","ABSX",3,5,"","","","","none","none"),
0x9E:("STZ","ABSX",3,5,"Yes","","","","none","none"),
0x9F:("BBS1","ZPR",3,5,"Yes","","","","none","none"),
0xA0:("LDY","IMMED",2,2,"","","","","NZ","none"),
0xA1:("LDA","IZX",2,6,"","","","","NZ","none"),
0xA2:("LDX","IMMED",2,2,"","","","","NZ","none"),
0xA4:("LDY","ZP",2,3,"","","","","NZ","none"),
0xA5:("LDA","ZP",2,3,"","","","","NZ","none"),
0xA6:("LDX","ZP",2,3,"","","","","NZ","none"),
0xA7:("SMB2","ZP",2,5,"Yes","","","","none","none"),
0xA8:("TAY","IMP",1,2,"","","","","NZ","none"),
0xA9:("LDA","IMMED",2,2,"","","","","NZ","none"),
0xAA:("TAX","IMP",1,2,"","","","","NZ","none"),
0xAC:("LDY","ABS",3,4,"","","","","NZ","none"),
0xAD:("LDA","ABS",3,4,"","","","","NZ","none"),
0xAE:("LDX","ABS",3,4,"","","","","NZ","none"),
0xAF:("BBS2","ZPR",3,5,"Yes","","","","none","none"),
0xB0:("BCS","REL",2,2,"","Yes","Yes","","none","C"),
0xB1:("LDA","IZY",2,5,"","Yes","","","NZ","none"),
0xB2:("LDA","IZP",2,5,"Yes","","","","NZ","none"),
0xB4:("LDY","ZPX",2,4,"","","","","NZ","none"),
0xB5:("LDA","ZPX",2,4,"","","","","NZ","none"),
0xB6:("LDX","ZPY",2,4,"","","","","NZ","none"),
0xB7:("SMB3","ZP",2,5,"Yes","","","","none","none"),
0xB8:("CLV","IMP",1,2,"","","","","V","V"),
0xB9:("LDA","ABSY",3,4,"","Yes","","","NZ","none"),
0xBA:("TSX","IMP",1,2,"","","","","NZ","none"),
0xBC:("LDY","ABSX",3,4,"","Yes","","","NZ","none"),
0xBD:("LDA","ABSX",3,4,"","Yes","","","NZ","none"),
0xBE:("LDX","ABSY",3,4,"","Yes","","","NZ","none"),
0xBF:("BBS3","ZPR",3,5,"Yes","","","","none","none"),
0xC0:("CPY","IMMED",2,2,"","","","","NZC","none"),
0xC1:("CMP","IZX",2,6,"","","","","NZC","none"),
0xC4:("CPY","ZP",2,3,"","","","","NZC","none"),
0xC5:("CMP","ZP",2,3,"","","","","NZC","none"),
0xC6:("DEC","ZP",2,5,"","","","","NZ","none"),
0xC7:("SMB4","ZP",2,5,"Yes","","","","none","none"),
0xC8:("INY","IMP",1,2,"","","","","NZ","none"),
0xC9:("CMP","IMMED",2,2,"","","","","NZC","none"),
0xCA:("DEX","IMP",1,2,"","","","","NZ","none"),
0xCB:("WAI","IMP",1,3,"","","","","none","none"),
0xCC:("CPY","ABS",3,4,"","","","","NZC","none"),
0xCD:("CMP","ABS",3,4,"","","","","NZC","none"),
0xCE:("DEC","ABS",3,6,"","","","","NZ","none"),
0xCF:("BBS4","ZPR",3,5,"Yes","","","","none","none"),
0xD0:("BNE","REL",2,2,"","Yes","Yes","","none","Z"),
0xD1:("CMP","IZY",2,5,"","Yes","","","NZC","none"),
0xD2:("CMP","IZP",2,5,"Yes","","","","NZC","none"),
0xD5:("CMP","ZPX",2,4,"","","","","NZC","none"),
0xD6:("DEC","ZPX",2,6,"","","","","NZ","none"),
0xD7:("SMB5","ZP",2,5,"Yes","","","","none","none"),
0xD8:("CLD","IMP",1,2,"","","","","D","none"),
0xD9:("CMP","ABSY",3,4,"","Yes","","","NZC","none"),
0xDA:("PHX","IMP",1,3,"Yes","","","","none","none"),
0xDB:("STP","IMP",1,3,"","","","","none","none"),
0xDD:("CMP","ABSX",3,4,"","Yes","","","NZC","none"),
0xDE:("DEC","ABSX",3,7,"","","","","f","none"),
0xDF:("BBS5","ZPR",3,5,"Yes","","","","none","none"),
0xE0:("CPX","IMMED",2,2,"","","","","NZC","none"),
0xE1:("SBC","IZX",2,6,"","","","Yes","NVZC","C"),
0xE4:("CPX","ZP",2,3,"","","","","NZC","none"),
0xE5:("SBC","ZP",2,3,"","","","Yes","NVZC","C"),
0xE6:("INC","ZP",2,5,"","","","","NZ","none"),
0xE7:("SMB6","ZP",2,5,"Yes","","","","none","none"),
0xE8:("INX","IMP",1,2,"","","","","NZ","none"),
0xE9:("SBC","IMMED",2,2,"","","","Yes","NVZC","C"),
0xEA:("NOP","IMP",1,2,"","","","","none","none"),
0xEC:("CPX","ABS",3,4,"","","","","NZC","none"),
0xED:("SBC","ABS",3,4,"","","","Yes","NVZC","C"),
0xEE:("INC","ABS",3,6,"","","","","NZ","none"),
0xEF:("BBS6","ZPR",3,5,"Yes","","","","none","none"),
0xF0:("BEQ","REL",2,2,"","Yes","Yes","","none","Z"),
0xF1:("SBC","IZY",2,5,"","Yes","","Yes","NVZC","C"),
0xF2:("SBC","IZP",2,5,"Yes","","","Yes","NVZC","C"),
0xF5:("SBC","ZPX",2,4,"","","","Yes","NVZC","C"),
0xF6:("INC","ZPX",2,6,"","","","","NZ","none"),
0xF7:("SMB7","ZP",2,5,"Yes","","","","none","none"),
0xF8:("SED","IMP",1,2,"","","","","D","none"),
0xF9:("SBC","ABSY",3,4,"","Yes","","Yes","NVZC","C"),
0xFA:("PLX","IMP",1,4,"Yes","","","","NZ","none"),
0xFD:("SBC","ABSX",3,4,"","Yes","","Yes","NVZC","C"),
0xFE:("INC","ABSX",3,7,"","","","","NZ","none"),
0xFF:("BBS7","ZPR",3,5,"Yes","","","","none","none")

}


#Instruction information list indexes
INDEX_NAME=0
INDEX_MODE=1
INDEX_SIZE=2
INDEX_CYCLES=3
INDEX_6502_ONLY=4
INDEX_BOUNDARY_CYCLE=5
INDEX_BRANCH_CYCLE=6
INDEX_BCD_CYCLE=7
INDEX_FLAGS=8
INDEX_AFFECTS=9

#Generate dictionaries based on op dictionary
OP_INFO_NAME={}
OP_INFO_MODE={}
for k,v in OP_INFO.items():

    #Dictionary by instruction name
    if v[INDEX_NAME] not in OP_INFO_NAME:
        OP_INFO_NAME[v[INDEX_NAME]]=[(k,)+v]
    else:
        OP_INFO_NAME[v[INDEX_NAME]]+=[(k,)+v]

    #Dictionary by addressing mode
    if v[INDEX_MODE] not in OP_INFO_MODE:
        OP_INFO_MODE[v[INDEX_MODE]]=[(k,)+v]
    else:
        OP_INFO_MODE[v[INDEX_MODE]]+=[(k,)+v]

#Assembly directives
DIRECTIVE_LIST=[
    ".ORG",
    ".SET",
    ".XSET",
    ".BYTE",".DB",".ASCII",     #Equivalent
    ".DW",".WORD",              #Equivalent
    ".DS",".RS"                 #Equivalent
    ]

#Text colors for curses
COLOR_NAMES={
    "blue":curses.COLOR_BLUE,
    "green":curses.COLOR_GREEN,
    "cyan":curses.COLOR_CYAN,
    "yellow":curses.COLOR_YELLOW,
    "red":curses.COLOR_RED,
    "magenta":curses.COLOR_MAGENTA,
    "white":curses.COLOR_WHITE,
    "black":curses.COLOR_BLACK
    }

TEXT_COLORS=(
    ("op",              ("blue","black")),      #Instruction
    ("dir",             ("magenta","black")),   #Assembly directive
    ("alpha",           ("white","black")),     #Symbol, ie defined with .SET
    ("label",           ("cyan","black")),
    ("number",          ("magenta","black")),
    ("character",       ("green","black")),
    ("string",          ("green","black")),
    ("reg",             ("blue","black")),      #X or Y register
    ("comment",         ("cyan","black")),
    ("paren selected",  ("white","magenta")),   #Matching parenthesis when cursor on parenthesis
    ("symbol",          ("white","black")),     #Any symbol #,$,&,etc
    ("symbol unknown",  ("black","yellow")),    #Unknown alpha symbol like "foo"
    ("symbol error",    ("white","red")),       #Syntax error like LDA ) or LDA $$
    ("neutral",         ("white","black")),     #Symbol at end of line - not recognized but don't flag as unknown
    ("line current",    ("black","green")),     #Highlight address to show current line
    ("line unknown",    ("black","yellow")),    #Highlight address if contains unknown symbols
    ("line error",      ("white","red")),       #Highlight address if contains syntax error
    ("line breakpoint", ("red","white")),       #Highlight address if contains breakpoint
    ("bytes unknown",   ("yellow","black")),    #Color of ?? in assembled bytes if value unknown
    ("bytes error",     ("red","black")),       #Color of "Not found" or "Range error" from byte generation
    ("flag untouched",  ("cyan","black")),
    ("flag changed",    ("magenta","black"))
    )

#Filled in programmatically below from TEXT_COLORS
COLOR_DICT={}

#Global variables
global_symbols={}

#Class declarations
class ProcessorClass:
    def __init__(self):
        self.A=0
        self.X=0
        self.Y=0
        self.SP=0
        self.N=0
        self.V=0
        self.B=0
        self.D=0
        self.I=0
        self.Z=0
        self.C=0
        self.regs_valid=False

class LineClass:
    def __init__(self):
        self.raw_str=""
        self.raw_str_ptr=0
        self.breakpoint=False
        self.CPU=ProcessorClass()
        self.__reset()

    #Reset status before parsing
    def __reset(self):
        self.line_type="unknown"
        self.line_type_symbol_val=""
        self.index_first=-1
        self.index_second=-1
        self.index_selected=-1
        self.symbol_list=[]
        self.simplified_symbol_list=[]
        self.text_symbol_list=[]
        self.pattern=""
        self.debug_pattern_reason=""
        self.symbol_unknown=False
        self.symbol_unknown_last=False
        self.symbol_error=False
        self.parentheses_balanced=False
        self.bytes=[]
        self.mode_not_found=False
        self.range_error=False

        self.debug_msgs=[]

    #Split text input into symbols and classify them
    def __parse_symbols(self):
        ALPHA_SYMBOLS="._"
        symbol=""
        new_symbols=[]
        symbol_type="none"

        for i,char in enumerate(self.raw_str):
            #Add character to existing symbol
            last_character=(i==len(self.raw_str)-1)
            add_symbol=False

            if symbol_type=="alpha":
                if char.isalnum() or char in ALPHA_SYMBOLS:
                    symbol+=char
                else:
                    add_symbol=True
            elif symbol_type=="number":
                if char.isnumeric():
                    symbol+=char
                elif char.isalnum() or char in ALPHA_SYMBOLS:
                    symbol+=char
                    symbol_type="error"
                else:
                    add_symbol=True
            elif symbol_type=="hex":
                if char.isnumeric() or char in "abcdefABCDEF":
                    symbol+=char
                elif char.isalpha() or char in ALPHA_SYMBOLS:
                    symbol+=char
                    symbol_type="error"
                else:
                    add_symbol=True
            elif symbol_type=="character":
                symbol+=char
                if char=="'":
                    add_symbol=True 
                    char=""
            elif symbol_type=="string":
                symbol+=char
                if char=='"':
                    add_symbol=True 
                    char=""
            elif symbol_type=="comment":
                symbol+=char
            elif symbol_type=="error":
                if char.isalnum() or char in ALPHA_SYMBOLS:
                    symbol+=char
                else:
                    add_symbol=True

            #Add completed symbol to list of new symbols
            if add_symbol:
                new_symbols+=[(symbol,symbol_type)]
                symbol_type="none"
                symbol=""

            if i==self.raw_str_ptr:
                self.index_selected=len(self.symbol_list)+len(new_symbols)

            #Start new symbol
            add_symbol=False
            if symbol_type=="none":
                if char=="":
                    #For character or string, closing ' or " ends symbols without starting new one
                    pass
                elif char.isalpha() or char in ALPHA_SYMBOLS:
                    symbol_type="alpha"
                    symbol=char
                elif char.isnumeric():
                    symbol_type="number"
                    symbol=char
                elif char=="$":
                    symbol_type="hex"
                    symbol="$"
                elif char=="'":
                    symbol_type="character"
                    symbol="'"
                elif char=='"':
                    symbol_type="string"
                    symbol='"'
                elif char=="#":
                    symbol_type="hash"
                    symbol="#"
                    add_symbol=True
                elif char==";":
                    symbol_type="comment"
                    symbol=";"
                else:
                    #All other chars are symbols even space
                    symbol_type="symbol"
                    symbol=char
                    add_symbol=True
           
            #Last symbol on line classified also
            if last_character:
                add_symbol=True
            
            #Add symbol to list of new symbols
            if add_symbol and symbol_type!="none":
                new_symbols+=[(symbol,symbol_type)]
                symbol_type="none"
                symbol=""

            #Add new symbols to class object
            for new_val, new_type in new_symbols:
                self.symbol_list+=[(new_val,new_type)]
            new_symbols=[]

#State machine for verifying syntax - edit in spreadsheet, not here
    _verification_state_machine={
        ('','n'):'n',
        ('~','n'):'n',
        ('(','n'):'n',
        ('m','n'):'n',
        ('#','n'):'n',
        ('+','n'):'n',
        (',','n'):'n',
        ('','~'):'~',
        ('~','~'):'~',
        ('(','~'):'~',
        ('#','~'):'~',
        ('+','~'):'~',
        (',','~'):'~',
        ('','('):'(',
        ('~','('):'(',
        ('(','('):'(',
        ('m','('):'(',
        ('#','('):'(',
        ('+','('):'(',
        (',','('):'(',
        ('n',')'):')',
        (')',')'):')',
        ('X',')'):')',
        ('n','+'):'+',
        (')','+'):'+',
        ('n',','):',',
        (')',','):',',
        ('d',','):',',
        ('s',','):',',
        ('','-'):'m',
        ('n','-'):'+',
        ('~','-'):'m',
        ('(','-'):'m',
        ('m','-'):'m',
        ('#','-'):'m',
        (')','-'):'+',
        ('+','-'):'m',
        (',','-'):'m',
        ('','#'):'#',
        (',','X'):'X',
        (',','Y'):'Y',
        ('','d'):'d',
        ('','s'):'s',
        (',','s'):'s'
        }

    #Syntax patterns for assembly directives - no spreadsheet entry so edit here
    _dir_patterns={
        #(new symbol count, comma count (-1 being unlimited), string allowed?)
        ".ORG":     (0,0,False),
        ".SET":     (1,1,True),
        ".XSET":    (1,1,True),
        ".BYTE":    (0,-1,True),
        ".DB":      (0,-1,True),
        ".ASCII":   (0,-1,True),
        ".DW":      (0,-1,False),
        ".WORD":    (0,-1,False),
        ".DS":      (0,0,False),
        ".RS":      (0,0,False)
        }

    #Classify symbols and check for errors - unknown symbols, mismatched parentheses, unallowed characters
    def __process_symbols(self):
        global global_symbols

        ALLOWED_SYMBOLS="~(),+-*/&|^%<> "
        new_symbol_list=[]
        paren_level=0
        previous_symbol=""
        found_first=False
        found_second=False
        comma_count=0
        for i,symbol in enumerate(self.symbol_list):
            symbol_val,symbol_type=symbol
            #Recognize instructions, assembly directives, and registers
            if symbol_type=="alpha":
                if symbol_val.upper() in OP_INFO_NAME:
                    #Instruction
                    symbol_type="op"
                elif symbol_val.upper() in DIRECTIVE_LIST:
                    #Assembly directive
                    symbol_type="dir"
                elif symbol_val.upper() in ["X","Y"]:
                    #Register
                    symbol_type="reg"
                symbol=(symbol_val,symbol_type)
            next_symbol=""
            new_symbol=symbol
            
            #Don't count space as first symbol
            if not found_first and symbol!=(" ","symbol"):
                first_symbol=True
                found_first=True
                self.index_first=i
            else:
                first_symbol=False

            #Also, don't count space as second symbol
            if not first_symbol and found_first and not found_second and symbol!=(" ","symbol"):
                second_symbol=True
                found_second=True
                self.index_second=i
            else:
                second_symbol=False
            last_symbol=(i==len(self.symbol_list)-1)
            
            #Look for syntax errors
            if first_symbol:
                if symbol_type in ["dir","op"]:
                    self.line_type=symbol_type
                    self.line_type_symbol_val=symbol_val
                    if symbol_type=="dir":
                        dir_symbol_count=self._dir_patterns[symbol_val.upper()][0]
                        dir_comma_count=self._dir_patterns[symbol_val.upper()][1]
                        dir_string_allowed=self._dir_patterns[symbol_val.upper()][2]
                elif not last_symbol:
                    new_symbol=(symbol_val,"error")
                    self.symbol_error=True
            else:
                if self.line_type=="dir" and second_symbol and dir_symbol_count==1:
                    #First word after .SET or .XSET is name of new symbol
                    if symbol_type=="alpha":
                        symbol_type="definition"
                        new_symbol=(symbol_val,"definition")
                        next_symbol="d"
                    else:
                        #Only textual objects can be assigned a value
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                if symbol_type=="alpha":
                    if symbol_val not in global_symbols:
                        #Unrecognized word - textual symbol or label not yet defined
                        if self.line_type_symbol_val.upper()!=".XSET":
                            #Don't mark symbols in .XSET statement as unknown
                            new_symbol=(symbol_val,"unknown")
                            if last_symbol and not self.symbol_unknown:
                                self.symbol_unknown_last=True
                            self.symbol_unknown=True
                    next_symbol="n"
                elif symbol_type=="error":
                    self.symbol_error=True
                elif symbol_type in ["op","dir"]:
                    #Not first symbol - first symbol checked above
                    new_symbol=(symbol_val,"error")
                    self.symbol_error=True
                elif symbol_type=="hash":
                    if self.line_type=="dir":
                        #Hash mark not allowed in assembly directive
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    next_symbol="#"
                elif symbol_type=="number":
                    next_symbol="n"
                elif symbol_type=="hex":
                    if symbol_val=="$" and not last_symbol:
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    next_symbol="n"
                elif symbol_type=="character":
                    if symbol_val=="''" or \
                    len(symbol_val)>3 or \
                    (len(symbol_val)==3 and symbol_val[-1]!="'"):
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    next_symbol="n"
                elif symbol_type=="string":
                    if self.line_type=="op":
                        #String not allowed in instruction
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    elif self.line_type=="dir" and not dir_string_allowed:
                        #Only some directives allow strings
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    next_symbol="s"
                elif symbol_type=="reg":
                    if self.line_type=="dir":
                        #Registers not allowed in assembly directive
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    next_symbol=symbol_val.upper()
                elif symbol_type in ["comment","definition"]:
                    #No errors to check for
                    pass
                elif symbol_type=="symbol":
                    if symbol_val in "()":
                        if symbol_val==")":
                            paren_level-=1
                        if paren_level<0:
                            new_symbol=(symbol_val,"error")
                            self.symbol_error=True
                        if symbol_val=="(":
                            paren_level+=1
                        next_symbol=symbol_val
                    elif symbol_val in "-":
                        next_symbol=symbol_val
                    elif symbol_val in ",":
                        comma_count+=1
                        if self.line_type=="dir":
                            if paren_level!=0:
                                #Comma inside parentheses not allowed in assembly directive
                                new_symbol=(symbol_val,"error")
                                self.symbol_error=True
                            elif dir_comma_count!=-1 and comma_count>dir_comma_count:
                                #Allowed number of commas for given assembly directive in table above
                                new_symbol=(symbol_val,"error")
                                self.symbol_error=True
                        elif self.line_type=="op":
                            if comma_count>1:
                                #No instructions have two commas
                                new_symbol=(symbol_val,"error")
                                self.symbol_error=True
                        next_symbol=symbol_val
                    elif symbol_val in "+*/%&|^":
                        next_symbol="+"
                    elif symbol_val in "~<>":
                        next_symbol="~"
                    elif symbol_val not in ALLOWED_SYMBOLS:
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                else:
                    #TODO: better error handling
                    exit(1)
                
            #Check for valid expression with state machine
            if self.symbol_error==False:
                if next_symbol:
                    if (previous_symbol,next_symbol) not in self._verification_state_machine:
                        new_symbol=(symbol_val,"error")
                        self.symbol_error=True
                    else:
                        previous_symbol=self._verification_state_machine[(previous_symbol,next_symbol)]

            #Add updated symbol to list
            new_symbol_list+=[new_symbol]
            
        self.symbol_list=new_symbol_list
        self.parentheses_balanced=(paren_level==0)

    #Generate colored text symbols to output to screen
    def __assign_text_symbols(self):  
        paren_highlight=False
        paren_stack=[]
        paren_index=len(self.symbol_list)-1 if self.index_selected==-1 else self.index_selected
        for i,symbol in enumerate(self.symbol_list):
            symbol_val,symbol_type=symbol
            last_symbol=(i==(len(self.symbol_list)-1))
            if symbol_type in ["alpha","op","dir","reg"]:
                #TODO: combine with list below if not processing here
                self.text_symbol_list+=[(symbol_val,symbol_type)]
            elif symbol_type=="unknown":
                if last_symbol:
                    #Don't color last alpha symbol on line as unknown since may still be typing
                    self.text_symbol_list+=[(symbol_val,"neutral")]
                else:
                    self.text_symbol_list+=[(symbol_val,"symbol unknown")]
            elif symbol_type=="error":
                self.text_symbol_list+=[(symbol_val,"symbol error")]
            elif symbol_type in ["hash","number","hex"]:
                self.text_symbol_list+=[(symbol_val,"number")]
            elif symbol_type in ["number","character","string","comment"]:
                #No special handling to color
                self.text_symbol_list+=[(symbol_val,symbol_type)]
            elif symbol_type=="symbol":
                #Parentheses highlighting
                if symbol_val in "()":
                    if i==paren_index:
                        if symbol_val=="(":
                            paren_counter=0
                            paren_target=(i,(symbol_val,"paren selected"))
                            paren_highlight=True
                        else:
                            paren_counter=1
                            for paren_val,paren_index in paren_stack:
                                paren_counter+=paren_val
                                if paren_counter==0:
                                    self.text_symbol_list[paren_index]=("(","paren selected")
                                    symbol_type="paren selected"
                                    break
                    if paren_highlight:
                        paren_counter+=(1 if symbol_val=="(" else -1)
                        if paren_counter==0:
                            self.text_symbol_list[paren_target[0]]=paren_target[1]
                            symbol_type="paren selected"
                            paren_highlight=False
                    else:
                        paren_stack.insert(0,(1 if symbol_val==")" else -1,i))
                self.text_symbol_list+=[(symbol_val,symbol_type)]
            else:
                #Other - should all be caught above but just in case
                self.text_symbol_list+=[(symbol_val,"symbol")]
                        
    #State machine for pattern matching - edit in spreadsheet, not here
    _pattern_state_machine={
        ('','*'):'*',
        ('*','*'):'*',
        ('#','*'):'#*',
        ('(','*'):'(*',
        ('*,','*'):'*,*',
        ('#*','*'):'#*',
        ('(*','*'):'(*',
        ('*,*','*'):'*,*',
        ('(*)','*'):'*',
        ('','#'):'#',
        ('','('):'(',
        ('*','('):'*',
        ('#','('):'#*',
        ('*,','('):'*,*',
        ('#*','('):'#*',
        ('*,*','('):'*,*',
        ('*',','):'*,',
        ('(*',','):'(*,',
        ('(*)',','):'(*),',
        ('*',')'):'*',
        ('#*',')'):'#*',
        ('(*',')'):'(*)',
        ('*,*',')'):'*,*',
        ('(*,X',')'):'(*,X)',
        ('*,','X'):'*,X',
        ('(*,','X'):'(*,X',
        ('(*),','X'):'*,X',
        ('*,','Y'):'*,Y',
        ('(*),','Y'):'(*),Y'
        }

    #Generate a pattern matching parsed symbols that can be matched to addressing mode:
    #LDA 5      => O* ie absolute/zp addressing
    #LDA 5+FOO  => O* ie absolute/zp addressing
    #LDA (5)    => O(*) ie indirect addressing
    #LDA (5)+1  => O* ie absolute/zp addressing
    def __assign_pattern(self):
        #If any symbol is an error, set pattern to "E"
        if self.symbol_error:
            self.pattern="E"
            self.debug_pattern_reason="Symbol error"
            return

        #Abbreviated process for assembly directives - only check for problems then return
        if self.line_type=="dir":
            for symbol in self.symbol_list:
                symbol_val,symbol_type=symbol
                if symbol_type=="hex":
                    #Treat as error here but not elsewhere since may be last character of input
                    if symbol_val=="$":
                        #Hex value of $ with no numbers - error
                        self.pattern="E"
                        self.debug_pattern_reason="Incomplete hex"
                        return
                elif symbol_type=="character":
                    #Treat as error here but not elsewhere since may be last character of input
                    if len(symbol_val)<3: 
                        #Unclosed character
                        self.pattern="E"
                        self.debug_pattern_reason="Unclosed character"
                        return
            #No errors found
            self.pattern="D"
            return

        #Full pattern generation process for instructions
        self.pattern=""
        new_symbol=""
        paren_level=0
        content=False
        line_type=""
        #Loop through symbols that specify pattern
        for i,symbol in enumerate(self.symbol_list):
            symbol_val,symbol_type=symbol
            last_symbol=(i==len(self.symbol_list)-1)
            #Symbols beyond first symbol
            if symbol_type in ["alpha","unknown","number"]:
                #Number, alpha (label, alias, etc), or unknown
                content=True
            elif symbol_type=="hex":
                #Treat as error here but not elsewhere since may be last character of input
                if symbol_val=="$":
                    #Hex value of $ with no numbers - error
                    self.pattern="E"
                    self.debug_pattern_reason="Incomplete hex"
                    return
                content=True
            elif symbol_type=="character":
                #Treat as error here but not elsewhere since may be last character of input
                if len(symbol_val)<3: 
                    #Unclosed character
                    self.pattern="E"
                    self.debug_pattern_reason="Unclosed character"
                    return
                content=True
            elif symbol_type=="hash":
                new_symbol="#"
            elif symbol_type=="reg":
                new_symbol=symbol_val.upper()
            elif symbol_type=="symbol":
                if symbol_val==",":
                    new_symbol=","
                elif symbol_val=="(":
                    paren_level+=1
                    if paren_level==1:
                        new_symbol="("
                    else:
                        content=True
                elif symbol_val==")":
                    paren_level-=1
                    if paren_level==0:
                        new_symbol=")"
                    else:
                        content=True
                elif symbol_val!=" ":
                    content=True

            #Process new symbol to add to pattern
            if new_symbol or last_symbol: 
                new_content=[]
                if content:
                    #Part of an expression (ie 2 or foo+2, etc) encountered before symbol. Mark as * in pattern.
                    new_content+=["*"]
                    content=False
                if new_symbol:
                    #New symbol to add to pattern found parsing above - ie # or , or ( or )
                    new_content+=[new_symbol]
                    new_symbol=""
                #Loop through up to two symbols to add to pattern: * for expression or new_symbol
                for symbol in new_content:
                    #Dictionary lookup for pattern state machine - pattern thus far plus new symbol
                    state_search=(self.pattern,symbol)
                    if state_search in self._pattern_state_machine:
                        #Dictionary contains new pattern only if pattern and new symbol valid combo
                        self.pattern=self._pattern_state_machine[state_search]
                    else:
                        #Pattern plus new symbol combo not found in dictionary - not valid input for pattern
                        self.pattern="E"
                        self.debug_pattern_reason="Invalid pattern"
                        return
        
        #Add type to pattern
        if self.line_type=="op":
            self.pattern="O"+self.pattern
        else:
            #Unrecognized line type should be caught above but just in case
            self.pattern="E"
            self.debug_pattern_reason="Unrecognized line type"

    #Precedence and functionality for arithmetic operations
    _arithmetic_info={
        #precedence, arg count, associativity, function
        "~":(6,1,"left",lambda x:(x&0xFF)^0xFF if abs(x)<0x100 else (x&0xFFFF)^0xFFFF),
        ">":(6,1,"left",lambda x:(x&0xFF00)>>8),
        "<":(6,1,"left",lambda x:x&0xFF),
        #Minus sign - converted from leading subtraction sign
        "m":(6,1,"left",lambda x:-x),
        "*":(5,2,"left",lambda x,y:x*y),
        "/":(5,2,"left",lambda x,y:0 if y==0 else x/y),
        "%":(5,2,"left",lambda x,y:0 if y==0 else x%y),
        "+":(4,2,"left",lambda x,y:x+y),
        "-":(4,2,"left",lambda x,y:x-y),
        "&":(3,2,"left",lambda x,y:x&y),
        "^":(2,2,"left",lambda x,y:x^y),
        "|":(1,2,"left",lambda x,y:x|y)
        }        

    #Simplify expressions in symbol list: LDA (2+3)*4 => LDA 20
    def __simplify_symbols(self):
        global global_symbols

        #Don't simplify if error in symbol list
        if self.pattern=="E":
            return

        #Don't simplify if unclosed parenthesis
        if not self.parentheses_balanced:
            return

        #Don't simplify if unresolved symbols
        if self.symbol_unknown:
            return

        #Don't simplify if .XSET - wait until symbol invoked
        if self.line_type_symbol_val.upper()==".XSET":
            return

        #Try to replace any textual symbols
        source_symbol_list=self.symbol_list
        new_symbol_list=[]
        for symbol in source_symbol_list:
            symbol_val,symbol_type=symbol
            new_symbol=[symbol]
            if symbol_type=="alpha":
                if symbol_val in global_symbols:
                    #Replace alpha/textual symbol with lookup value
                    #TODO: don't let string into instruction
                    new_symbol=[global_symbols[symbol_val]]
                else:
                    #Unknown symbol!
                    self.symbol_unknown=True
                    return
            new_symbol_list+=new_symbol
        source_symbol_list=new_symbol_list
        
        #Convert leading subtraction sign to minus sign and remove spaces
        new_symbol_list=[]
        last_symbol=""
        for symbol in source_symbol_list:
            new_symbol=symbol
            if symbol==("-","symbol"):
                if last_symbol in ["op","symbol"]:
                    #Minus at beginning of expression or before qualifying symbol: ~<>(+*/%&|^,
                    new_symbol=("m","symbol")
                elif last_symbol=="m":
                    #Two leading minus signs cancel out - pop last minus sign
                    new_symbol_list=new_symbol_list[:-1]
                    new_symbol=("","none")
                elif last_symbol=="-":
                    #Two subtraction signs become addition
                    new_symbol_list=new_symbol_list[:-1]
                    new_symbol=("+","symbol")
                    while new_symbol_list[-1]==("+","symbol"):
                        new_symbol_list=new_symbol_list[:-1]
            
            #Add symbol to list
            if new_symbol not in [("","none"),(" ","symbol")]:
                new_symbol_list+=[new_symbol]

            #Classify added symbol for next iteration
            if new_symbol!=(" ","symbol"):
                #Track symbol if not space
                last_symbol="x"
                if new_symbol==("","none"):
                    #If double minus cancels out, use symbol added before that
                    new_symbol_val,new_symbol_type=new_symbol_list[-1]
                else:
                    new_symbol_val,new_symbol_type=new_symbol
                if new_symbol_type=="op":
                    last_symbol="op"
                elif new_symbol_type=="symbol":
                    if new_symbol_val in "~<>(+*/%&|^,":
                        last_symbol="symbol"
                    elif new_symbol_val in ["m","-"]:
                        last_symbol=new_symbol_val
                elif new_symbol_type=="hash":
                    last_symbol="symbol"
        
        #Set modified list to input for RPN converion below
        source_symbol_list=new_symbol_list
        new_symbol_list=[]

        #Convert argument to RPN format
        operator_list=[]
        output_list=[]
        for i,symbol in enumerate(source_symbol_list):
            symbol_val,symbol_type=symbol
            first_symbol=(i==0)
            second_symbol=(i==1)
            last_symbol=(i==len(source_symbol_list)-1)
            if first_symbol:
                new_symbol_list+=[symbol]
            else:
                if symbol_type=="definition":
                    new_symbol_list+=[symbol]
                elif symbol_type=="number":
                    output_list+=[(int(symbol_val),"number")]
                elif symbol_type=="hex":
                    output_list+=[(int(symbol_val[1:],16),"number")]
                elif symbol_type=="character":
                    output_list+=[(ord(symbol_val[1]),"number")]
                elif symbol_type in ["hash","reg","string"]:
                    #__assign_pattern above ensures hash, reg, and string appear in correct place 
                    new_symbol_list+=[symbol]
                elif symbol_type=="comment":
                    #Ignore comments
                    pass 
                elif symbol_type=="symbol":
                    if symbol_val in "m~<>*/+-&^|":
                        prec,argc,assoc,func=self._arithmetic_info[symbol_val]
                        looping=True
                        while looping:
                            if len(operator_list)==0:
                                looping=False
                            elif operator_list[-1]=="(":
                                looping=False
                            else:
                                prec_TOS=self._arithmetic_info[operator_list[-1]][0]
                                if prec_TOS>prec or (prec==prec_TOS and assoc=="left"):
                                    output_list+=[(operator_list[-1],"symbol")]
                                    operator_list=operator_list[:-1]
                                else:
                                    looping=False
                        operator_list+=[symbol_val] 
                    elif symbol_val=="(":
                        operator_list+=[symbol_val]
                    elif symbol_val==")":
                        looping=True
                        while looping:
                            #__verify_symbols above ensures matching parentheses always exists
                            if operator_list[-1]=="(":
                                looping=False
                            else:
                                output_list+=[(operator_list[-1],"symbol")]           
                            operator_list=operator_list[:-1]
                    elif symbol_val==",":
                        #Skip handling here and handle below the same as end of input
                        pass
                    else:
                        #Ignore any other characters such as space
                        pass

            #Calculate expression and add to output
            if last_symbol or symbol==(",","symbol"):
                #Add any operators left in operator list
                while operator_list:
                    operator=operator_list[-1]
                    if operator=="(":
                        break
                    output_list+=[(operator,"symbol")]
                    operator_list=operator_list[:-1]

                #Calculate expression
                failed=False
                number_list=[]
                for output in output_list:
                    output_val,output_type=output
                    if output_type=="number":
                        number_list+=[output_val]
                    elif output_type=="symbol":
                        argc=self._arithmetic_info[output_val][1]
                        if len(number_list)<argc:
                            failed=True
                            break
                        func=self._arithmetic_info[output_val][3]
                        if argc==1:
                            new_val=int(func(number_list[-1]))
                            number_list=number_list[:-1]+[new_val]
                        elif argc==2:
                            new_val=int(func(number_list[-2],number_list[-1]))
                            number_list=number_list[:-2]+[new_val]
                output_list=[]

                #Error if multiple numbers left on stack
                if len(number_list)>1:
                    failed=True

                #Problem parsing - empty simplified_symbol_list indicates error
                if failed:
                    return
                
                #Add calculated number to final output
                if number_list!=[]:
                    new_symbol_list+=[(number_list[0],"number")]

                #Comma is added after calculated value
                if symbol==(",","symbol"):
                   new_symbol_list+=[symbol] 

        #TODO: remove
        self.debug_msgs+=["Final: "+str(new_symbol_list)]

        self.simplified_symbol_list=new_symbol_list

    
    #List of addressing modes for generating bytes
    _pattern_list={
        #Preferred variant listed first if argument unresolved
        #ie assume ABS instead of ZP for LDA foo if foo unresolved
        "O*":       ("ABS","ZP","REL"),
        "O*,X":     ("ABSX","ZPX"),
        "O*,Y":     ("ABSY","ZPY"),
        "O(*,X)":   ("IAX","IZX"),
        "O#*":      ("IMMED",),
        "O":        ("IMP",),
        "O(*)":     ("IND","IZP"),
        "O(*),Y":   ("IZY",),
        "O*,*":     ("ZPR",)
        }

    #Make sure pattern generated from input matches simplified symbol list
    #(Mostly a sanity check since all syntax errors should be caught above)
    def __verify_pattern(self):
        #TODO: use line type instead?
        
        #Do not verify assembly directives or instructions with syntax errors
        if self.pattern in ["E","D"]:
            return

        #Do not verify if unresolved symbols since symbol list is still unsimplified
        if self.symbol_unknown:
            return

        #Generate pattern if pattern exists for instruction
        if self.pattern[0]=="O":
            gen_pattern=""
            for symbol in self.simplified_symbol_list:
                symbol_val,symbol_type=symbol
                if symbol_type=="op":
                    gen_pattern+="O"
                elif symbol_type=="number":
                    gen_pattern+="*"
                elif symbol_type==("#","hash"):
                    gen_pattern+="#"
                elif symbol==(",","symbol"):
                    gen_pattern+=","
                elif symbol_type=="reg":
                    gen_pattern+=symbol_val.upper()
            
            #Ensure pattern of simplified symbols matches an addressing mode
            #Searches modes like O(*),Y also that can't exist in simplified symbols though doesn't hurt anything 
            if gen_pattern not in self._pattern_list:
                #Addressing mode not found - probably incomplete like O*,
                self.pattern="E"
                self.debug_pattern_reason="Pattern doesn't match symbol list"
                return
            
    #List of information about addressing modes
    _addressing_mode_list={
        #Argument sizes, ZP alternative
        "ABS":  (2, "ZP"),
        "ABSX": (2, "ZPX"),
        "ABSY": (2, "ZPY"),
        "IAX":  (2, ""),
        "IMMED":(1, ""),
        "IMP":  (0, ""),
        "IND":  (1, ""),
        "IZP":  (1, ""),
        "IZX":  (1, ""),
        "IZY":  (1, ""),
        "REL":  (1, ""),
        "ZP":   (1, ""),
        "ZPR":  (2, ""),    #Actually, two one-byte arguments but handled as special case below
        "ZPX":  (1, ""),
        "ZPY":  (1, "")
        }

    #Assign bytes for instruction or directive. Assign only op code if instruction argument contains unresolved symbol.
    def __assign_bytes(self):
        if self.pattern=="E":
            return
        elif self.pattern=="D":
            return
        elif self.pattern[0]=="O":
            if self.pattern in self._pattern_list:
                if self.symbol_unknown:
                    #Addressing mode found but symbols unresolved - match op code only
                    op_name=self.line_type_symbol_val.upper()
                    for mode in self._pattern_list[self.pattern]:
                        for op in OP_INFO_NAME[op_name]:
                            op_mode=op[2]
                            if mode==op_mode: 
                                op_code=op[0]
                                self.bytes=[op_code]
                                arg_size=self._addressing_mode_list[mode][0]
                                self.bytes+=[[]]*arg_size
                                return
                    #Instruction does not have matching addressing mode
                    self.mode_not_found=True
                else:
                    #TODO: Addressing mode exists - try to generate full instruction
                    op_name=self.line_type_symbol_val.upper()
                    for mode in self._pattern_list[self.pattern]:
                        for op in OP_INFO_NAME[op_name]:
                            op_mode=op[2]
                            if mode==op_mode: 
                                #Matching addressing mode found!

                                #Check argument ranges and generate bytes
                                op_code=op[0]
                                temp_bytes=[op_code]
                                arg_size=self._addressing_mode_list[mode][0]
                                if mode=="IMMED":
                                    arg_val=self.simplified_symbol_list[2][0]
                                    #Valid range for immediates
                                    if arg_val<-128 or arg_val>255:
                                        self.range_error=True
                                    elif arg_val<0:
                                        #Two's compliment for negative immediates
                                        arg_val=0x100+arg_val
                                    temp_bytes+=[arg_val]
                                elif mode=="IMP":
                                    #Implied addressing - no arguments to check or generate bytes for
                                    pass
                                else:
                                    arg_val=self.simplified_symbol_list[1][0]

                                    #Check if shorter zero page addressing mode exists and address in range
                                    zp_mode=self._addressing_mode_list[mode][1]
                                    if zp_mode and arg_val in range(0x100):
                                        #Check that zero page addressing exists for instruction, ie LDA $1234,Y doesn't have LDA $34,Y
                                        zp_op_code=[v[0] for v in OP_INFO_NAME[op_name] if v[INDEX_MODE+1]==zp_mode]
                                        if zp_op_code!=[]:
                                            arg_size=self._addressing_mode_list[zp_mode][0]
                                            mode=zp_mode
                                            temp_bytes=[zp_op_code[0]]
                                    if arg_val<0:
                                        #Negative addresses not allowed
                                        self.range_error=True
                                    elif arg_size==1:
                                        if arg_val>0xFF:
                                            #Address too large for addressing mode
                                            self.range_error=True
                                        else:
                                            temp_bytes+=[arg_val] 
                                    elif arg_size==2:
                                        if arg_val>0xFFFF:
                                            #Address too large for addressing mode
                                            self.range_error=True
                                        else:
                                            temp_bytes+=[arg_val&0xFF]
                                            temp_bytes+=[arg_val>>8]

                                if self.range_error:
                                    #Immediate or address out of range above - return without generating any bytes 
                                    return
                            
                                #Finished generating bytes successfully - add bytes to object
                                self.bytes=temp_bytes
                                return

                    #Finished looping and no matching addressing mode found for instruction
                    self.mode_not_found=True
                    return
            else:
                #TODO: Addressing mode not found - ie O*, since stil typing
                pass

    def update(self):
        self.__reset()
        self.__parse_symbols()
        if self.symbol_list==[]:
            return
        self.__process_symbols()
        self.__assign_text_symbols()
        self.__assign_pattern()
        self.__simplify_symbols()
        self.__verify_pattern()
        self.__assign_bytes()

    #Outputs to text file - run explicitly if needed
    def pattern_test():
        test_list=[
            "adc a-b",
            "adc (a)",
            "adc (a)-b",
            "adc (a)-(b)",
            "adc a-b,y",
            "adc (a),y",
            "adc (a)-b,y",
            "adc (a)-(b),y",
            "adc )a(",
            "adc )a(,y"
            ]

        temp_obj=LineClass()

        with open("pattern-debug.txt","wt") as f:
            for test in test_list:
                temp_obj.raw_str=test
                temp_obj.update()
                f.write(test+" - "+temp_obj.pattern+"\n")

#Screen output constants
MAX_INPUT_LEN=20

ADDRESS_WIDTH=7
BYTES_WIDTH=16
INPUT_WIDTH=21
REG_A_WIDTH=7
REG_X_WIDTH=4
REG_Y_WIDTH=4
REG_SP_WIDTH=4+1    #+1 spacing between sections
FLAGS_WIDTH=9+1     #+1 spacing between sections
SOURCE_WIDTH=len("$C000: $AB ")
DEST_WIDTH=len("$C000: $AB ")

START_X=0
ADDRESS_X=START_X
BYTES_X=ADDRESS_X+ADDRESS_WIDTH
INPUT_X=BYTES_X+BYTES_WIDTH
REG_A_X=INPUT_X+INPUT_WIDTH
REG_X_X=REG_A_X+REG_A_WIDTH
REG_Y_X=REG_X_X+REG_X_WIDTH
REG_SP_X=REG_Y_X+REG_Y_WIDTH
FLAGS_X=REG_SP_X+REG_SP_WIDTH

#TODO: Source twice in headers?
#TODO: Add cycles column
HEADER_TEXT="Source               A      X   Y   SP   Flags     Source    Dest"
HEADER_X=INPUT_X
HEADER_Y=0

LINES_START_Y=1

#Emulator constants
EMU_START_ADDRESS=0xC000    #Default start address if no .ORG

#Functions
def Hex2(num):
    return ("00"+hex(num)[2:])[-2:].upper()

def Hex4(num):
    return ("0000"+hex(num)[2:])[-4:].upper()

def CursesText(screen,draw_x,draw_y,text,color="none"):
    screen.addstr(draw_y,draw_x,text,COLOR_DICT[color])
    return draw_x+len(text)

def InteractiveAssembler(screen):
    #Initialize color pairs
    global COLOR_DICT
    for i,color in enumerate(TEXT_COLORS):
        curses.init_pair(i+1,COLOR_NAMES[color[1][0]],COLOR_NAMES[color[1][1]])
        COLOR_DICT[color[0]]=curses.color_pair(i+1)
    COLOR_DICT["none"]=curses.color_pair(0)

    #Editor variables
    current_line=0
    line_offset=0
    key=""
    input_str=""
    input_ptr=0
    program_lines=[LineClass()]
   
    #Initialize global symbols
    #TODO: remove after testing
    global_symbols["foo"]=("123","number")

    #Main loop
    while(True):
        screen.clear() 

        #Draw headers
        CursesText(screen,HEADER_X,HEADER_Y,HEADER_TEXT)

        #Draw lines
        line_address=EMU_START_ADDRESS
        for i,line in enumerate(program_lines):
            #Calculate Y offset once
            draw_y=LINES_START_Y+i

            #Address
            color="none"
            if line.symbol_error:
                color="line error"
            elif line.symbol_unknown and not line.symbol_unknown_last:
                color="line unknown"
            else:
                color="none"
            CursesText(screen,ADDRESS_X,draw_y,Hex4(line_address),color)
            CursesText(screen,ADDRESS_X+5,draw_y,":")

            #Assembled bytes
            if line.bytes!=[]:
                draw_x=BYTES_X
                for byte in line.bytes:
                    if byte==[]:
                        CursesText(screen,draw_x,draw_y,"??","bytes unknown")
                        CursesText(screen,draw_x+2,draw_y," ")
                    else:
                        CursesText(screen,draw_x,draw_y,Hex2(byte)+" ")
                    draw_x+=3
            else:
                #Byte list empty - syntax error (handled above), blank line (ignore) or instruction with wrong addressing mode like SEC 5
                if line.mode_not_found:
                    #Don't warn if only instruction since probably about to type argument 
                    if len(line.simplified_symbol_list)!=1:
                        CursesText(screen,BYTES_X,draw_y,"Mode not found!","bytes error")
                elif line.range_error:
                    CursesText(screen,BYTES_X,draw_y,"Range error!","bytes error")

            #TODO: change
            CursesText(screen,BYTES_X,draw_y+3,line.pattern+" - "+line.debug_pattern_reason)
            CursesText(screen,BYTES_X,draw_y+4,str(line.symbol_list))
            for i,msg in enumerate(line.debug_msgs):
                CursesText(screen,BYTES_X,draw_y+i*3+6,msg)
           
            #Text input
            draw_x=INPUT_X
            for obj in line.text_symbol_list:
                text,color=obj
                CursesText(screen,draw_x,draw_y,text,color)
                draw_x+=len(text)
            
            #Registers
            reg_A=line.CPU.A
            if reg_A<32 or (reg_A>=127 and reg_A<=160):
                reg_A_char=" "
            else:
                reg_A_char=chr(reg_A)
            CursesText(screen,REG_A_X,draw_y,"$"+Hex2(line.CPU.A)+"("+reg_A_char+")")
            CursesText(screen,REG_X_X,draw_y,"$"+Hex2(line.CPU.X))
            CursesText(screen,REG_Y_X,draw_y,"$"+Hex2(line.CPU.Y))
            CursesText(screen,REG_SP_X,draw_y,"$"+Hex2(line.CPU.SP))
            
            #Flags
            if line.CPU.regs_valid:
                flag_output=""
                flag_output+="N" if line.CPU.N==1 else "n"
                flag_output+="V" if line.CPU.V==1 else "v"
                flag_output+="-B"
                flag_output+="D" if line.CPU.D==1 else "d"
                flag_output+="I" if line.CPU.I==1 else "i"
                flag_output+="Z" if line.CPU.Z==1 else "z"
                flag_output+="C" if line.CPU.C==1 else "c"
                CursesText(screen,FLAGS_X,draw_y,flag_output)

        #Place cursor on input line
        screen.move(LINES_START_Y+current_line,INPUT_X+input_ptr)
        screen.refresh()
        
        #Process keys
        try:
            key=screen.getkey()
        except KeyboardInterrupt:
            #User pressed Ctrl+C
           
            #TODO: remove
            #with open("debug.txt","wt") as f:
            #    for symbol in program_lines[current_line].symbol_list:
            #        f.write(str(symbol)+"\n")
            #    for symbol in program_lines[current_line].text_symbol_list:
            #        f.write(str(symbol)+"\n")

            exit(0)
        #TODO: decide if only update on changed string or update on left/right to get parentheses highlighting
        #update_input=False
        update_input=True
        if key=="KEY_RESIZE":
            #Redraw whole screen every time so shouldn't be needed
            pass
        elif key=="KEY_BACKSPACE":
            if input_ptr!=0:
                input_str=input_str[:input_ptr-1]+input_str[input_ptr:]
                input_ptr-=1
                update_input=True
        elif key=="KEY_LEFT":
            if input_ptr>0:
                input_ptr-=1
        elif key=="KEY_RIGHT":
            if input_ptr<len(input_str):
                input_ptr+=1
        elif key=="KEY_HOME":
            input_ptr=0
        elif key=="KEY_END":
            input_ptr=len(input_str)
        elif key=="KEY_DC":
            if input_ptr!=len(input_str):
                input_str=input_str[:input_ptr]+input_str[input_ptr+1:]
                update_input=True
        elif len(key)==1 and len(input_str)<MAX_INPUT_LEN:
            input_str=input_str[:input_ptr]+key+input_str[input_ptr:]
            input_ptr+=1
            update_input=True

        #Update program line
        if update_input:
            program_lines[current_line].raw_str=input_str
            program_lines[current_line].raw_str_ptr=input_ptr
            program_lines[current_line].update()

#Check arguments
if len(argv)==1:
    #No arguments - proceed to interactive mode
    pass
elif len(argv)==2:
    #One argument - filename to load
    #TODO: load file
    pass
else:
    #More than one argument - error
    #TODO: argument error
    pass

#Enter interactive assembler 
curses.wrapper(InteractiveAssembler)
exit(0)