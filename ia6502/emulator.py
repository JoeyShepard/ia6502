#!/usr/bin/env python3

from ia6502.classes import *

#Constants
#=========
MAX_INSTRUCTIONS=100    #Max instructions to execute to prevent endless loop

#Globals
#======
emu_addresses={}
emu_mem=[]
program_lines=[LineClass()]

#Auto-generated functions for emulated instructions
#(See emu_generator/ for script. Don't edit here!)
#=================================================
def BRK_IMP(emu_line): #0x00
	address,data=mode_IMP(emu_line)
	address=op_BRK(emu_line,address,data,"IMP")
	return address+1

def ORA_IZX(emu_line): #0x01
	address,data=mode_IZX(emu_line)
	address=op_ORA(emu_line,address,data,"IZX")
	return address+2

def TSB_ZP(emu_line): #0x04
	address,data=mode_ZP(emu_line)
	address=op_TSB(emu_line,address,data,"ZP")
	return address+2

def ORA_ZP(emu_line): #0x05
	address,data=mode_ZP(emu_line)
	address=op_ORA(emu_line,address,data,"ZP")
	return address+2

def ASL_ZP(emu_line): #0x06
	address,data=mode_ZP(emu_line)
	address=op_ASL(emu_line,address,data,"ZP")
	return address+2

def RMB0_ZP(emu_line): #0x07
	address,data=mode_ZP(emu_line)
	address=op_RMB0(emu_line,address,data,"ZP")
	return address+2

def PHP_IMP(emu_line): #0x08
	address,data=mode_IMP(emu_line)
	address=op_PHP(emu_line,address,data,"IMP")
	return address+1

def ORA_IMMED(emu_line): #0x09
	address,data=mode_IMMED(emu_line)
	address=op_ORA(emu_line,address,data,"IMMED")
	return address+2

def ASL_IMP(emu_line): #0x0A
	address,data=mode_IMP(emu_line)
	address=op_ASL(emu_line,address,data,"IMP")
	return address+1

def TSB_ABS(emu_line): #0x0C
	address,data=mode_ABS(emu_line)
	address=op_TSB(emu_line,address,data,"ABS")
	return address+3

def ORA_ABS(emu_line): #0x0D
	address,data=mode_ABS(emu_line)
	address=op_ORA(emu_line,address,data,"ABS")
	return address+3

def ASL_ABS(emu_line): #0x0E
	address,data=mode_ABS(emu_line)
	address=op_ASL(emu_line,address,data,"ABS")
	return address+3

def BBR0_ZPR(emu_line): #0x0F
	address,data=mode_ZPR(emu_line)
	address=op_BBR0(emu_line,address,data,"ZPR")
	return address

def BPL_REL(emu_line): #0x10
	address,data=mode_REL(emu_line)
	address=op_BPL(emu_line,address,data,"REL")
	return address

def ORA_IZY(emu_line): #0x11
	address,data=mode_IZY(emu_line)
	address=op_ORA(emu_line,address,data,"IZY")
	return address+2

def ORA_IZP(emu_line): #0x12
	address,data=mode_IZP(emu_line)
	address=op_ORA(emu_line,address,data,"IZP")
	return address+2

def TRB_ZP(emu_line): #0x14
	address,data=mode_ZP(emu_line)
	address=op_TRB(emu_line,address,data,"ZP")
	return address+2

def ORA_ZPX(emu_line): #0x15
	address,data=mode_ZPX(emu_line)
	address=op_ORA(emu_line,address,data,"ZPX")
	return address+2

def ASL_ZPX(emu_line): #0x16
	address,data=mode_ZPX(emu_line)
	address=op_ASL(emu_line,address,data,"ZPX")
	return address+2

def RMB1_ZP(emu_line): #0x17
	address,data=mode_ZP(emu_line)
	address=op_RMB1(emu_line,address,data,"ZP")
	return address+2

def CLC_IMP(emu_line): #0x18
	address,data=mode_IMP(emu_line)
	address=op_CLC(emu_line,address,data,"IMP")
	return address+1

def ORA_ABSY(emu_line): #0x19
	address,data=mode_ABSY(emu_line)
	address=op_ORA(emu_line,address,data,"ABSY")
	return address+3

def INC_IMP(emu_line): #0x1A
	address,data=mode_IMP(emu_line)
	address=op_INC(emu_line,address,data,"IMP")
	return address+1

def TRB_ABS(emu_line): #0x1C
	address,data=mode_ABS(emu_line)
	address=op_TRB(emu_line,address,data,"ABS")
	return address+3

def ORA_ABSX(emu_line): #0x1D
	address,data=mode_ABSX(emu_line)
	address=op_ORA(emu_line,address,data,"ABSX")
	return address+3

def ASL_ABSX(emu_line): #0x1E
	address,data=mode_ABSX(emu_line)
	address=op_ASL(emu_line,address,data,"ABSX")
	return address+3

def BBR1_ZPR(emu_line): #0x1F
	address,data=mode_ZPR(emu_line)
	address=op_BBR1(emu_line,address,data,"ZPR")
	return address

def JSR_ABS(emu_line): #0x20
	address,data=mode_ABS(emu_line)
	address=op_JSR(emu_line,address,data,"ABS")
	return address

def AND_IZX(emu_line): #0x21
	address,data=mode_IZX(emu_line)
	address=op_AND(emu_line,address,data,"IZX")
	return address+2

def BIT_ZP(emu_line): #0x24
	address,data=mode_ZP(emu_line)
	address=op_BIT(emu_line,address,data,"ZP")
	return address+2

def AND_ZP(emu_line): #0x25
	address,data=mode_ZP(emu_line)
	address=op_AND(emu_line,address,data,"ZP")
	return address+2

def ROL_ZP(emu_line): #0x26
	address,data=mode_ZP(emu_line)
	address=op_ROL(emu_line,address,data,"ZP")
	return address+2

def RMB2_ZP(emu_line): #0x27
	address,data=mode_ZP(emu_line)
	address=op_RMB2(emu_line,address,data,"ZP")
	return address+2

def PLP_IMP(emu_line): #0x28
	address,data=mode_IMP(emu_line)
	address=op_PLP(emu_line,address,data,"IMP")
	return address+1

def AND_IMMED(emu_line): #0x29
	address,data=mode_IMMED(emu_line)
	address=op_AND(emu_line,address,data,"IMMED")
	return address+2

def ROL_IMP(emu_line): #0x2A
	address,data=mode_IMP(emu_line)
	address=op_ROL(emu_line,address,data,"IMP")
	return address+1

def BIT_ABS(emu_line): #0x2C
	address,data=mode_ABS(emu_line)
	address=op_BIT(emu_line,address,data,"ABS")
	return address+3

def AND_ABS(emu_line): #0x2D
	address,data=mode_ABS(emu_line)
	address=op_AND(emu_line,address,data,"ABS")
	return address+3

def ROL_ABS(emu_line): #0x2E
	address,data=mode_ABS(emu_line)
	address=op_ROL(emu_line,address,data,"ABS")
	return address+3

def BBR2_ZPR(emu_line): #0x2F
	address,data=mode_ZPR(emu_line)
	address=op_BBR2(emu_line,address,data,"ZPR")
	return address

def BMI_REL(emu_line): #0x30
	address,data=mode_REL(emu_line)
	address=op_BMI(emu_line,address,data,"REL")
	return address

def AND_IZY(emu_line): #0x31
	address,data=mode_IZY(emu_line)
	address=op_AND(emu_line,address,data,"IZY")
	return address+2

def AND_IZP(emu_line): #0x32
	address,data=mode_IZP(emu_line)
	address=op_AND(emu_line,address,data,"IZP")
	return address+2

def BIT_ZPX(emu_line): #0x34
	address,data=mode_ZPX(emu_line)
	address=op_BIT(emu_line,address,data,"ZPX")
	return address+2

def AND_ZPX(emu_line): #0x35
	address,data=mode_ZPX(emu_line)
	address=op_AND(emu_line,address,data,"ZPX")
	return address+2

def ROL_ZPX(emu_line): #0x36
	address,data=mode_ZPX(emu_line)
	address=op_ROL(emu_line,address,data,"ZPX")
	return address+2

def RMB3_ZP(emu_line): #0x37
	address,data=mode_ZP(emu_line)
	address=op_RMB3(emu_line,address,data,"ZP")
	return address+2

def SEC_IMP(emu_line): #0x38
	address,data=mode_IMP(emu_line)
	address=op_SEC(emu_line,address,data,"IMP")
	return address+1

def AND_ABSY(emu_line): #0x39
	address,data=mode_ABSY(emu_line)
	address=op_AND(emu_line,address,data,"ABSY")
	return address+3

def DEC_IMP(emu_line): #0x3A
	address,data=mode_IMP(emu_line)
	address=op_DEC(emu_line,address,data,"IMP")
	return address+1

def BIT_ABSX(emu_line): #0x3C
	address,data=mode_ABSX(emu_line)
	address=op_BIT(emu_line,address,data,"ABSX")
	return address+3

def AND_ABSX(emu_line): #0x3D
	address,data=mode_ABSX(emu_line)
	address=op_AND(emu_line,address,data,"ABSX")
	return address+3

def ROL_ABSX(emu_line): #0x3E
	address,data=mode_ABSX(emu_line)
	address=op_ROL(emu_line,address,data,"ABSX")
	return address+3

def BBR3_ZPR(emu_line): #0x3F
	address,data=mode_ZPR(emu_line)
	address=op_BBR3(emu_line,address,data,"ZPR")
	return address

def RTI_IMP(emu_line): #0x40
	address,data=mode_IMP(emu_line)
	address=op_RTI(emu_line,address,data,"IMP")
	return address+1

def EOR_IZX(emu_line): #0x41
	address,data=mode_IZX(emu_line)
	address=op_EOR(emu_line,address,data,"IZX")
	return address+2

def EOR_ZP(emu_line): #0x45
	address,data=mode_ZP(emu_line)
	address=op_EOR(emu_line,address,data,"ZP")
	return address+2

def LSR_ZP(emu_line): #0x46
	address,data=mode_ZP(emu_line)
	address=op_LSR(emu_line,address,data,"ZP")
	return address+2

def RMB4_ZP(emu_line): #0x47
	address,data=mode_ZP(emu_line)
	address=op_RMB4(emu_line,address,data,"ZP")
	return address+2

def PHA_IMP(emu_line): #0x48
	address,data=mode_IMP(emu_line)
	address=op_PHA(emu_line,address,data,"IMP")
	return address+1

def EOR_IMMED(emu_line): #0x49
	address,data=mode_IMMED(emu_line)
	address=op_EOR(emu_line,address,data,"IMMED")
	return address+2

def LSR_IMP(emu_line): #0x4A
	address,data=mode_IMP(emu_line)
	address=op_LSR(emu_line,address,data,"IMP")
	return address+1

def JMP_ABS(emu_line): #0x4C
	address,data=mode_ABS(emu_line)
	address=op_JMP(emu_line,address,data,"ABS")
	return address

def EOR_ABS(emu_line): #0x4D
	address,data=mode_ABS(emu_line)
	address=op_EOR(emu_line,address,data,"ABS")
	return address+3

def LSR_ABS(emu_line): #0x4E
	address,data=mode_ABS(emu_line)
	address=op_LSR(emu_line,address,data,"ABS")
	return address+3

def BBR4_ZPR(emu_line): #0x4F
	address,data=mode_ZPR(emu_line)
	address=op_BBR4(emu_line,address,data,"ZPR")
	return address

def BVC_REL(emu_line): #0x50
	address,data=mode_REL(emu_line)
	address=op_BVC(emu_line,address,data,"REL")
	return address

def EOR_IZY(emu_line): #0x51
	address,data=mode_IZY(emu_line)
	address=op_EOR(emu_line,address,data,"IZY")
	return address+2

def EOR_IZP(emu_line): #0x52
	address,data=mode_IZP(emu_line)
	address=op_EOR(emu_line,address,data,"IZP")
	return address+2

def EOR_ZPX(emu_line): #0x55
	address,data=mode_ZPX(emu_line)
	address=op_EOR(emu_line,address,data,"ZPX")
	return address+2

def LSR_ZPX(emu_line): #0x56
	address,data=mode_ZPX(emu_line)
	address=op_LSR(emu_line,address,data,"ZPX")
	return address+2

def RMB5_ZP(emu_line): #0x57
	address,data=mode_ZP(emu_line)
	address=op_RMB5(emu_line,address,data,"ZP")
	return address+2

def CLI_IMP(emu_line): #0x58
	address,data=mode_IMP(emu_line)
	address=op_CLI(emu_line,address,data,"IMP")
	return address+1

def EOR_ABSY(emu_line): #0x59
	address,data=mode_ABSY(emu_line)
	address=op_EOR(emu_line,address,data,"ABSY")
	return address+3

def PHY_IMP(emu_line): #0x5A
	address,data=mode_IMP(emu_line)
	address=op_PHY(emu_line,address,data,"IMP")
	return address+1

def EOR_ABSX(emu_line): #0x5D
	address,data=mode_ABSX(emu_line)
	address=op_EOR(emu_line,address,data,"ABSX")
	return address+3

def LSR_ABSX(emu_line): #0x5E
	address,data=mode_ABSX(emu_line)
	address=op_LSR(emu_line,address,data,"ABSX")
	return address+3

def BBR5_ZPR(emu_line): #0x5F
	address,data=mode_ZPR(emu_line)
	address=op_BBR5(emu_line,address,data,"ZPR")
	return address

def RTS_IMP(emu_line): #0x60
	address,data=mode_IMP(emu_line)
	address=op_RTS(emu_line,address,data,"IMP")
	return address+1

def ADC_IZX(emu_line): #0x61
	address,data=mode_IZX(emu_line)
	address=op_ADC(emu_line,address,data,"IZX")
	return address+2

def STZ_ZP(emu_line): #0x64
	address,data=mode_ZP(emu_line)
	address=op_STZ(emu_line,address,data,"ZP")
	return address+2

def ADC_ZP(emu_line): #0x65
	address,data=mode_ZP(emu_line)
	address=op_ADC(emu_line,address,data,"ZP")
	return address+2

def ROR_ZP(emu_line): #0x66
	address,data=mode_ZP(emu_line)
	address=op_ROR(emu_line,address,data,"ZP")
	return address+2

def RMB6_ZP(emu_line): #0x67
	address,data=mode_ZP(emu_line)
	address=op_RMB6(emu_line,address,data,"ZP")
	return address+2

def PLA_IMP(emu_line): #0x68
	address,data=mode_IMP(emu_line)
	address=op_PLA(emu_line,address,data,"IMP")
	return address+1

def ADC_IMMED(emu_line): #0x69
	address,data=mode_IMMED(emu_line)
	address=op_ADC(emu_line,address,data,"IMMED")
	return address+2

def ROR_IMP(emu_line): #0x6A
	address,data=mode_IMP(emu_line)
	address=op_ROR(emu_line,address,data,"IMP")
	return address+1

def JMP_IND(emu_line): #0x6C
	address,data=mode_IND(emu_line)
	address=op_JMP(emu_line,address,data,"IND")
	return address

def ADC_ABS(emu_line): #0x6D
	address,data=mode_ABS(emu_line)
	address=op_ADC(emu_line,address,data,"ABS")
	return address+3

def ROR_ABS(emu_line): #0x6E
	address,data=mode_ABS(emu_line)
	address=op_ROR(emu_line,address,data,"ABS")
	return address+3

def BBR6_ZPR(emu_line): #0x6F
	address,data=mode_ZPR(emu_line)
	address=op_BBR6(emu_line,address,data,"ZPR")
	return address

def BVS_REL(emu_line): #0x70
	address,data=mode_REL(emu_line)
	address=op_BVS(emu_line,address,data,"REL")
	return address

def ADC_IZY(emu_line): #0x71
	address,data=mode_IZY(emu_line)
	address=op_ADC(emu_line,address,data,"IZY")
	return address+2

def ADC_IZP(emu_line): #0x72
	address,data=mode_IZP(emu_line)
	address=op_ADC(emu_line,address,data,"IZP")
	return address+2

def STZ_ZPX(emu_line): #0x74
	address,data=mode_ZPX(emu_line)
	address=op_STZ(emu_line,address,data,"ZPX")
	return address+2

def ADC_ZPX(emu_line): #0x75
	address,data=mode_ZPX(emu_line)
	address=op_ADC(emu_line,address,data,"ZPX")
	return address+2

def ROR_ZPX(emu_line): #0x76
	address,data=mode_ZPX(emu_line)
	address=op_ROR(emu_line,address,data,"ZPX")
	return address+2

def RMB7_ZP(emu_line): #0x77
	address,data=mode_ZP(emu_line)
	address=op_RMB7(emu_line,address,data,"ZP")
	return address+2

def SEI_IMP(emu_line): #0x78
	address,data=mode_IMP(emu_line)
	address=op_SEI(emu_line,address,data,"IMP")
	return address+1

def ADC_ABSY(emu_line): #0x79
	address,data=mode_ABSY(emu_line)
	address=op_ADC(emu_line,address,data,"ABSY")
	return address+3

def PLY_IMP(emu_line): #0x7A
	address,data=mode_IMP(emu_line)
	address=op_PLY(emu_line,address,data,"IMP")
	return address+1

def JMP_IAX(emu_line): #0x7C
	address,data=mode_IAX(emu_line)
	address=op_JMP(emu_line,address,data,"IAX")
	return address

def ADC_ABSX(emu_line): #0x7D
	address,data=mode_ABSX(emu_line)
	address=op_ADC(emu_line,address,data,"ABSX")
	return address+3

def ROR_ABSX(emu_line): #0x7E
	address,data=mode_ABSX(emu_line)
	address=op_ROR(emu_line,address,data,"ABSX")
	return address+3

def BBR7_ZPR(emu_line): #0x7F
	address,data=mode_ZPR(emu_line)
	address=op_BBR7(emu_line,address,data,"ZPR")
	return address

def BRA_REL(emu_line): #0x80
	address,data=mode_REL(emu_line)
	address=op_BRA(emu_line,address,data,"REL")
	return address

def STA_IZX(emu_line): #0x81
	address,data=mode_IZX(emu_line)
	address=op_STA(emu_line,address,data,"IZX")
	return address+2

def STY_ZP(emu_line): #0x84
	address,data=mode_ZP(emu_line)
	address=op_STY(emu_line,address,data,"ZP")
	return address+2

def STA_ZP(emu_line): #0x85
	address,data=mode_ZP(emu_line)
	address=op_STA(emu_line,address,data,"ZP")
	return address+2

def STX_ZP(emu_line): #0x86
	address,data=mode_ZP(emu_line)
	address=op_STX(emu_line,address,data,"ZP")
	return address+2

def SMB0_ZP(emu_line): #0x87
	address,data=mode_ZP(emu_line)
	address=op_SMB0(emu_line,address,data,"ZP")
	return address+2

def DEY_IMP(emu_line): #0x88
	address,data=mode_IMP(emu_line)
	address=op_DEY(emu_line,address,data,"IMP")
	return address+1

def BIT_IMMED(emu_line): #0x89
	address,data=mode_IMMED(emu_line)
	address=op_BIT(emu_line,address,data,"IMMED")
	return address+2

def TXA_IMP(emu_line): #0x8A
	address,data=mode_IMP(emu_line)
	address=op_TXA(emu_line,address,data,"IMP")
	return address+1

def STY_ABS(emu_line): #0x8C
	address,data=mode_ABS(emu_line)
	address=op_STY(emu_line,address,data,"ABS")
	return address+3

def STA_ABS(emu_line): #0x8D
	address,data=mode_ABS(emu_line)
	address=op_STA(emu_line,address,data,"ABS")
	return address+3

def STX_ABS(emu_line): #0x8E
	address,data=mode_ABS(emu_line)
	address=op_STX(emu_line,address,data,"ABS")
	return address+3

def BBS0_ZPR(emu_line): #0x8F
	address,data=mode_ZPR(emu_line)
	address=op_BBS0(emu_line,address,data,"ZPR")
	return address

def BCC_REL(emu_line): #0x90
	address,data=mode_REL(emu_line)
	address=op_BCC(emu_line,address,data,"REL")
	return address

def STA_IZY(emu_line): #0x91
	address,data=mode_IZY(emu_line)
	address=op_STA(emu_line,address,data,"IZY")
	return address+2

def STA_IZP(emu_line): #0x92
	address,data=mode_IZP(emu_line)
	address=op_STA(emu_line,address,data,"IZP")
	return address+2

def STY_ZPX(emu_line): #0x94
	address,data=mode_ZPX(emu_line)
	address=op_STY(emu_line,address,data,"ZPX")
	return address+2

def STA_ZPX(emu_line): #0x95
	address,data=mode_ZPX(emu_line)
	address=op_STA(emu_line,address,data,"ZPX")
	return address+2

def STX_ZPY(emu_line): #0x96
	address,data=mode_ZPY(emu_line)
	address=op_STX(emu_line,address,data,"ZPY")
	return address+2

def SMB1_ZP(emu_line): #0x97
	address,data=mode_ZP(emu_line)
	address=op_SMB1(emu_line,address,data,"ZP")
	return address+2

def TYA_IMP(emu_line): #0x98
	address,data=mode_IMP(emu_line)
	address=op_TYA(emu_line,address,data,"IMP")
	return address+1

def STA_ABSY(emu_line): #0x99
	address,data=mode_ABSY(emu_line)
	address=op_STA(emu_line,address,data,"ABSY")
	return address+3

def TXS_IMP(emu_line): #0x9A
	address,data=mode_IMP(emu_line)
	address=op_TXS(emu_line,address,data,"IMP")
	return address+1

def STZ_ABS(emu_line): #0x9C
	address,data=mode_ABS(emu_line)
	address=op_STZ(emu_line,address,data,"ABS")
	return address+3

def STA_ABSX(emu_line): #0x9D
	address,data=mode_ABSX(emu_line)
	address=op_STA(emu_line,address,data,"ABSX")
	return address+3

def STZ_ABSX(emu_line): #0x9E
	address,data=mode_ABSX(emu_line)
	address=op_STZ(emu_line,address,data,"ABSX")
	return address+3

def BBS1_ZPR(emu_line): #0x9F
	address,data=mode_ZPR(emu_line)
	address=op_BBS1(emu_line,address,data,"ZPR")
	return address

def LDY_IMMED(emu_line): #0xA0
	address,data=mode_IMMED(emu_line)
	address=op_LDY(emu_line,address,data,"IMMED")
	return address+2

def LDA_IZX(emu_line): #0xA1
	address,data=mode_IZX(emu_line)
	address=op_LDA(emu_line,address,data,"IZX")
	return address+2

def LDX_IMMED(emu_line): #0xA2
	address,data=mode_IMMED(emu_line)
	address=op_LDX(emu_line,address,data,"IMMED")
	return address+2

def LDY_ZP(emu_line): #0xA4
	address,data=mode_ZP(emu_line)
	address=op_LDY(emu_line,address,data,"ZP")
	return address+2

def LDA_ZP(emu_line): #0xA5
	address,data=mode_ZP(emu_line)
	address=op_LDA(emu_line,address,data,"ZP")
	return address+2

def LDX_ZP(emu_line): #0xA6
	address,data=mode_ZP(emu_line)
	address=op_LDX(emu_line,address,data,"ZP")
	return address+2

def SMB2_ZP(emu_line): #0xA7
	address,data=mode_ZP(emu_line)
	address=op_SMB2(emu_line,address,data,"ZP")
	return address+2

def TAY_IMP(emu_line): #0xA8
	address,data=mode_IMP(emu_line)
	address=op_TAY(emu_line,address,data,"IMP")
	return address+1

def LDA_IMMED(emu_line): #0xA9
	address,data=mode_IMMED(emu_line)
	address=op_LDA(emu_line,address,data,"IMMED")
	return address+2

def TAX_IMP(emu_line): #0xAA
	address,data=mode_IMP(emu_line)
	address=op_TAX(emu_line,address,data,"IMP")
	return address+1

def LDY_ABS(emu_line): #0xAC
	address,data=mode_ABS(emu_line)
	address=op_LDY(emu_line,address,data,"ABS")
	return address+3

def LDA_ABS(emu_line): #0xAD
	address,data=mode_ABS(emu_line)
	address=op_LDA(emu_line,address,data,"ABS")
	return address+3

def LDX_ABS(emu_line): #0xAE
	address,data=mode_ABS(emu_line)
	address=op_LDX(emu_line,address,data,"ABS")
	return address+3

def BBS2_ZPR(emu_line): #0xAF
	address,data=mode_ZPR(emu_line)
	address=op_BBS2(emu_line,address,data,"ZPR")
	return address

def BCS_REL(emu_line): #0xB0
	address,data=mode_REL(emu_line)
	address=op_BCS(emu_line,address,data,"REL")
	return address

def LDA_IZY(emu_line): #0xB1
	address,data=mode_IZY(emu_line)
	address=op_LDA(emu_line,address,data,"IZY")
	return address+2

def LDA_IZP(emu_line): #0xB2
	address,data=mode_IZP(emu_line)
	address=op_LDA(emu_line,address,data,"IZP")
	return address+2

def LDY_ZPX(emu_line): #0xB4
	address,data=mode_ZPX(emu_line)
	address=op_LDY(emu_line,address,data,"ZPX")
	return address+2

def LDA_ZPX(emu_line): #0xB5
	address,data=mode_ZPX(emu_line)
	address=op_LDA(emu_line,address,data,"ZPX")
	return address+2

def LDX_ZPY(emu_line): #0xB6
	address,data=mode_ZPY(emu_line)
	address=op_LDX(emu_line,address,data,"ZPY")
	return address+2

def SMB3_ZP(emu_line): #0xB7
	address,data=mode_ZP(emu_line)
	address=op_SMB3(emu_line,address,data,"ZP")
	return address+2

def CLV_IMP(emu_line): #0xB8
	address,data=mode_IMP(emu_line)
	address=op_CLV(emu_line,address,data,"IMP")
	return address+1

def LDA_ABSY(emu_line): #0xB9
	address,data=mode_ABSY(emu_line)
	address=op_LDA(emu_line,address,data,"ABSY")
	return address+3

def TSX_IMP(emu_line): #0xBA
	address,data=mode_IMP(emu_line)
	address=op_TSX(emu_line,address,data,"IMP")
	return address+1

def LDY_ABSX(emu_line): #0xBC
	address,data=mode_ABSX(emu_line)
	address=op_LDY(emu_line,address,data,"ABSX")
	return address+3

def LDA_ABSX(emu_line): #0xBD
	address,data=mode_ABSX(emu_line)
	address=op_LDA(emu_line,address,data,"ABSX")
	return address+3

def LDX_ABSY(emu_line): #0xBE
	address,data=mode_ABSY(emu_line)
	address=op_LDX(emu_line,address,data,"ABSY")
	return address+3

def BBS3_ZPR(emu_line): #0xBF
	address,data=mode_ZPR(emu_line)
	address=op_BBS3(emu_line,address,data,"ZPR")
	return address

def CPY_IMMED(emu_line): #0xC0
	address,data=mode_IMMED(emu_line)
	address=op_CPY(emu_line,address,data,"IMMED")
	return address+2

def CMP_IZX(emu_line): #0xC1
	address,data=mode_IZX(emu_line)
	address=op_CMP(emu_line,address,data,"IZX")
	return address+2

def CPY_ZP(emu_line): #0xC4
	address,data=mode_ZP(emu_line)
	address=op_CPY(emu_line,address,data,"ZP")
	return address+2

def CMP_ZP(emu_line): #0xC5
	address,data=mode_ZP(emu_line)
	address=op_CMP(emu_line,address,data,"ZP")
	return address+2

def DEC_ZP(emu_line): #0xC6
	address,data=mode_ZP(emu_line)
	address=op_DEC(emu_line,address,data,"ZP")
	return address+2

def SMB4_ZP(emu_line): #0xC7
	address,data=mode_ZP(emu_line)
	address=op_SMB4(emu_line,address,data,"ZP")
	return address+2

def INY_IMP(emu_line): #0xC8
	address,data=mode_IMP(emu_line)
	address=op_INY(emu_line,address,data,"IMP")
	return address+1

def CMP_IMMED(emu_line): #0xC9
	address,data=mode_IMMED(emu_line)
	address=op_CMP(emu_line,address,data,"IMMED")
	return address+2

def DEX_IMP(emu_line): #0xCA
	address,data=mode_IMP(emu_line)
	address=op_DEX(emu_line,address,data,"IMP")
	return address+1

def WAI_IMP(emu_line): #0xCB
	address,data=mode_IMP(emu_line)
	address=op_WAI(emu_line,address,data,"IMP")
	return address+1

def CPY_ABS(emu_line): #0xCC
	address,data=mode_ABS(emu_line)
	address=op_CPY(emu_line,address,data,"ABS")
	return address+3

def CMP_ABS(emu_line): #0xCD
	address,data=mode_ABS(emu_line)
	address=op_CMP(emu_line,address,data,"ABS")
	return address+3

def DEC_ABS(emu_line): #0xCE
	address,data=mode_ABS(emu_line)
	address=op_DEC(emu_line,address,data,"ABS")
	return address+3

def BBS4_ZPR(emu_line): #0xCF
	address,data=mode_ZPR(emu_line)
	address=op_BBS4(emu_line,address,data,"ZPR")
	return address

def BNE_REL(emu_line): #0xD0
	address,data=mode_REL(emu_line)
	address=op_BNE(emu_line,address,data,"REL")
	return address

def CMP_IZY(emu_line): #0xD1
	address,data=mode_IZY(emu_line)
	address=op_CMP(emu_line,address,data,"IZY")
	return address+2

def CMP_IZP(emu_line): #0xD2
	address,data=mode_IZP(emu_line)
	address=op_CMP(emu_line,address,data,"IZP")
	return address+2

def CMP_ZPX(emu_line): #0xD5
	address,data=mode_ZPX(emu_line)
	address=op_CMP(emu_line,address,data,"ZPX")
	return address+2

def DEC_ZPX(emu_line): #0xD6
	address,data=mode_ZPX(emu_line)
	address=op_DEC(emu_line,address,data,"ZPX")
	return address+2

def SMB5_ZP(emu_line): #0xD7
	address,data=mode_ZP(emu_line)
	address=op_SMB5(emu_line,address,data,"ZP")
	return address+2

def CLD_IMP(emu_line): #0xD8
	address,data=mode_IMP(emu_line)
	address=op_CLD(emu_line,address,data,"IMP")
	return address+1

def CMP_ABSY(emu_line): #0xD9
	address,data=mode_ABSY(emu_line)
	address=op_CMP(emu_line,address,data,"ABSY")
	return address+3

def PHX_IMP(emu_line): #0xDA
	address,data=mode_IMP(emu_line)
	address=op_PHX(emu_line,address,data,"IMP")
	return address+1

def STP_IMP(emu_line): #0xDB
	address,data=mode_IMP(emu_line)
	address=op_STP(emu_line,address,data,"IMP")
	return address+1

def CMP_ABSX(emu_line): #0xDD
	address,data=mode_ABSX(emu_line)
	address=op_CMP(emu_line,address,data,"ABSX")
	return address+3

def DEC_ABSX(emu_line): #0xDE
	address,data=mode_ABSX(emu_line)
	address=op_DEC(emu_line,address,data,"ABSX")
	return address+3

def BBS5_ZPR(emu_line): #0xDF
	address,data=mode_ZPR(emu_line)
	address=op_BBS5(emu_line,address,data,"ZPR")
	return address

def CPX_IMMED(emu_line): #0xE0
	address,data=mode_IMMED(emu_line)
	address=op_CPX(emu_line,address,data,"IMMED")
	return address+2

def SBC_IZX(emu_line): #0xE1
	address,data=mode_IZX(emu_line)
	address=op_SBC(emu_line,address,data,"IZX")
	return address+2

def CPX_ZP(emu_line): #0xE4
	address,data=mode_ZP(emu_line)
	address=op_CPX(emu_line,address,data,"ZP")
	return address+2

def SBC_ZP(emu_line): #0xE5
	address,data=mode_ZP(emu_line)
	address=op_SBC(emu_line,address,data,"ZP")
	return address+2

def INC_ZP(emu_line): #0xE6
	address,data=mode_ZP(emu_line)
	address=op_INC(emu_line,address,data,"ZP")
	return address+2

def SMB6_ZP(emu_line): #0xE7
	address,data=mode_ZP(emu_line)
	address=op_SMB6(emu_line,address,data,"ZP")
	return address+2

def INX_IMP(emu_line): #0xE8
	address,data=mode_IMP(emu_line)
	address=op_INX(emu_line,address,data,"IMP")
	return address+1

def SBC_IMMED(emu_line): #0xE9
	address,data=mode_IMMED(emu_line)
	address=op_SBC(emu_line,address,data,"IMMED")
	return address+2

def NOP_IMP(emu_line): #0xEA
	address,data=mode_IMP(emu_line)
	address=op_NOP(emu_line,address,data,"IMP")
	return address+1

def CPX_ABS(emu_line): #0xEC
	address,data=mode_ABS(emu_line)
	address=op_CPX(emu_line,address,data,"ABS")
	return address+3

def SBC_ABS(emu_line): #0xED
	address,data=mode_ABS(emu_line)
	address=op_SBC(emu_line,address,data,"ABS")
	return address+3

def INC_ABS(emu_line): #0xEE
	address,data=mode_ABS(emu_line)
	address=op_INC(emu_line,address,data,"ABS")
	return address+3

def BBS6_ZPR(emu_line): #0xEF
	address,data=mode_ZPR(emu_line)
	address=op_BBS6(emu_line,address,data,"ZPR")
	return address

def BEQ_REL(emu_line): #0xF0
	address,data=mode_REL(emu_line)
	address=op_BEQ(emu_line,address,data,"REL")
	return address

def SBC_IZY(emu_line): #0xF1
	address,data=mode_IZY(emu_line)
	address=op_SBC(emu_line,address,data,"IZY")
	return address+2

def SBC_IZP(emu_line): #0xF2
	address,data=mode_IZP(emu_line)
	address=op_SBC(emu_line,address,data,"IZP")
	return address+2

def SBC_ZPX(emu_line): #0xF5
	address,data=mode_ZPX(emu_line)
	address=op_SBC(emu_line,address,data,"ZPX")
	return address+2

def INC_ZPX(emu_line): #0xF6
	address,data=mode_ZPX(emu_line)
	address=op_INC(emu_line,address,data,"ZPX")
	return address+2

def SMB7_ZP(emu_line): #0xF7
	address,data=mode_ZP(emu_line)
	address=op_SMB7(emu_line,address,data,"ZP")
	return address+2

def SED_IMP(emu_line): #0xF8
	address,data=mode_IMP(emu_line)
	address=op_SED(emu_line,address,data,"IMP")
	return address+1

def SBC_ABSY(emu_line): #0xF9
	address,data=mode_ABSY(emu_line)
	address=op_SBC(emu_line,address,data,"ABSY")
	return address+3

def PLX_IMP(emu_line): #0xFA
	address,data=mode_IMP(emu_line)
	address=op_PLX(emu_line,address,data,"IMP")
	return address+1

def SBC_ABSX(emu_line): #0xFD
	address,data=mode_ABSX(emu_line)
	address=op_SBC(emu_line,address,data,"ABSX")
	return address+3

def INC_ABSX(emu_line): #0xFE
	address,data=mode_ABSX(emu_line)
	address=op_INC(emu_line,address,data,"ABSX")
	return address+3

def BBS7_ZPR(emu_line): #0xFF
	address,data=mode_ZPR(emu_line)
	address=op_BBS7(emu_line,address,data,"ZPR")
	return address

#Emulator jump table
#===================
emu_ops=[
    BRK_IMP,        #0x00
    ORA_IZX,        #0x01
    NOP_IMP,        #0x02
    NOP_IMP,        #0x03
    TSB_ZP,         #0x04
    ORA_ZP,         #0x05
    ASL_ZP,         #0x06
    RMB0_ZP,        #0x07
    PHP_IMP,        #0x08
    ORA_IMMED,      #0x09
    ASL_IMP,        #0x0A
    NOP_IMP,        #0x0B
    TSB_ABS,        #0x0C
    ORA_ABS,        #0x0D
    ASL_ABS,        #0x0E
    BBR0_ZPR,       #0x0F
    BPL_REL,        #0x10
    ORA_IZY,        #0x11
    ORA_IZP,        #0x12
    NOP_IMP,        #0x13
    TRB_ZP,         #0x14
    ORA_ZPX,        #0x15
    ASL_ZPX,        #0x16
    RMB1_ZP,        #0x17
    CLC_IMP,        #0x18
    ORA_ABSY,       #0x19
    INC_IMP,        #0x1A
    NOP_IMP,        #0x1B
    TRB_ABS,        #0x1C
    ORA_ABSX,       #0x1D
    ASL_ABSX,       #0x1E
    BBR1_ZPR,       #0x1F
    JSR_ABS,        #0x20
    AND_IZX,        #0x21
    NOP_IMP,        #0x22
    NOP_IMP,        #0x23
    BIT_ZP,         #0x24
    AND_ZP,         #0x25
    ROL_ZP,         #0x26
    RMB2_ZP,        #0x27
    PLP_IMP,        #0x28
    AND_IMMED,      #0x29
    ROL_IMP,        #0x2A
    NOP_IMP,        #0x2B
    BIT_ABS,        #0x2C
    AND_ABS,        #0x2D
    ROL_ABS,        #0x2E
    BBR2_ZPR,       #0x2F
    BMI_REL,        #0x30
    AND_IZY,        #0x31
    AND_IZP,        #0x32
    NOP_IMP,        #0x33
    BIT_ZPX,        #0x34
    AND_ZPX,        #0x35
    ROL_ZPX,        #0x36
    RMB3_ZP,        #0x37
    SEC_IMP,        #0x38
    AND_ABSY,       #0x39
    DEC_IMP,        #0x3A
    NOP_IMP,        #0x3B
    BIT_ABSX,       #0x3C
    AND_ABSX,       #0x3D
    ROL_ABSX,       #0x3E
    BBR3_ZPR,       #0x3F
    RTI_IMP,        #0x40
    EOR_IZX,        #0x41
    NOP_IMP,        #0x42
    NOP_IMP,        #0x43
    NOP_IMP,        #0x44
    EOR_ZP,         #0x45
    LSR_ZP,         #0x46
    RMB4_ZP,        #0x47
    PHA_IMP,        #0x48
    EOR_IMMED,      #0x49
    LSR_IMP,        #0x4A
    NOP_IMP,        #0x4B
    JMP_ABS,        #0x4C
    EOR_ABS,        #0x4D
    LSR_ABS,        #0x4E
    BBR4_ZPR,       #0x4F
    BVC_REL,        #0x50
    EOR_IZY,        #0x51
    EOR_IZP,        #0x52
    NOP_IMP,        #0x53
    NOP_IMP,        #0x54
    EOR_ZPX,        #0x55
    LSR_ZPX,        #0x56
    RMB5_ZP,        #0x57
    CLI_IMP,        #0x58
    EOR_ABSY,       #0x59
    PHY_IMP,        #0x5A
    NOP_IMP,        #0x5B
    NOP_IMP,        #0x5C
    EOR_ABSX,       #0x5D
    LSR_ABSX,       #0x5E
    BBR5_ZPR,       #0x5F
    RTS_IMP,        #0x60
    ADC_IZX,        #0x61
    NOP_IMP,        #0x62
    NOP_IMP,        #0x63
    STZ_ZP,         #0x64
    ADC_ZP,         #0x65
    ROR_ZP,         #0x66
    RMB6_ZP,        #0x67
    PLA_IMP,        #0x68
    ADC_IMMED,      #0x69
    ROR_IMP,        #0x6A
    NOP_IMP,        #0x6B
    JMP_IND,        #0x6C
    ADC_ABS,        #0x6D
    ROR_ABS,        #0x6E
    BBR6_ZPR,       #0x6F
    BVS_REL,        #0x70
    ADC_IZY,        #0x71
    ADC_IZP,        #0x72
    NOP_IMP,        #0x73
    STZ_ZPX,        #0x74
    ADC_ZPX,        #0x75
    ROR_ZPX,        #0x76
    RMB7_ZP,        #0x77
    SEI_IMP,        #0x78
    ADC_ABSY,       #0x79
    PLY_IMP,        #0x7A
    NOP_IMP,        #0x7B
    JMP_IAX,        #0x7C
    ADC_ABSX,       #0x7D
    ROR_ABSX,       #0x7E
    BBR7_ZPR,       #0x7F
    BRA_REL,        #0x80
    STA_IZX,        #0x81
    NOP_IMP,        #0x82
    NOP_IMP,        #0x83
    STY_ZP,         #0x84
    STA_ZP,         #0x85
    STX_ZP,         #0x86
    SMB0_ZP,        #0x87
    DEY_IMP,        #0x88
    BIT_IMMED,      #0x89
    TXA_IMP,        #0x8A
    NOP_IMP,        #0x8B
    STY_ABS,        #0x8C
    STA_ABS,        #0x8D
    STX_ABS,        #0x8E
    BBS0_ZPR,       #0x8F
    BCC_REL,        #0x90
    STA_IZY,        #0x91
    STA_IZP,        #0x92
    NOP_IMP,        #0x93
    STY_ZPX,        #0x94
    STA_ZPX,        #0x95
    STX_ZPY,        #0x96
    SMB1_ZP,        #0x97
    TYA_IMP,        #0x98
    STA_ABSY,       #0x99
    TXS_IMP,        #0x9A
    NOP_IMP,        #0x9B
    STZ_ABS,        #0x9C
    STA_ABSX,       #0x9D
    STZ_ABSX,       #0x9E
    BBS1_ZPR,       #0x9F
    LDY_IMMED,      #0xA0
    LDA_IZX,        #0xA1
    LDX_IMMED,      #0xA2
    NOP_IMP,        #0xA3
    LDY_ZP,         #0xA4
    LDA_ZP,         #0xA5
    LDX_ZP,         #0xA6
    SMB2_ZP,        #0xA7
    TAY_IMP,        #0xA8
    LDA_IMMED,      #0xA9
    TAX_IMP,        #0xAA
    NOP_IMP,        #0xAB
    LDY_ABS,        #0xAC
    LDA_ABS,        #0xAD
    LDX_ABS,        #0xAE
    BBS2_ZPR,       #0xAF
    BCS_REL,        #0xB0
    LDA_IZY,        #0xB1
    LDA_IZP,        #0xB2
    NOP_IMP,        #0xB3
    LDY_ZPX,        #0xB4
    LDA_ZPX,        #0xB5
    LDX_ZPY,        #0xB6
    SMB3_ZP,        #0xB7
    CLV_IMP,        #0xB8
    LDA_ABSY,       #0xB9
    TSX_IMP,        #0xBA
    NOP_IMP,        #0xBB
    LDY_ABSX,       #0xBC
    LDA_ABSX,       #0xBD
    LDX_ABSY,       #0xBE
    BBS3_ZPR,       #0xBF
    CPY_IMMED,      #0xC0
    CMP_IZX,        #0xC1
    NOP_IMP,        #0xC2
    NOP_IMP,        #0xC3
    CPY_ZP,         #0xC4
    CMP_ZP,         #0xC5
    DEC_ZP,         #0xC6
    SMB4_ZP,        #0xC7
    INY_IMP,        #0xC8
    CMP_IMMED,      #0xC9
    DEX_IMP,        #0xCA
    WAI_IMP,        #0xCB
    CPY_ABS,        #0xCC
    CMP_ABS,        #0xCD
    DEC_ABS,        #0xCE
    BBS4_ZPR,       #0xCF
    BNE_REL,        #0xD0
    CMP_IZY,        #0xD1
    CMP_IZP,        #0xD2
    NOP_IMP,        #0xD3
    NOP_IMP,        #0xD4
    CMP_ZPX,        #0xD5
    DEC_ZPX,        #0xD6
    SMB5_ZP,        #0xD7
    CLD_IMP,        #0xD8
    CMP_ABSY,       #0xD9
    PHX_IMP,        #0xDA
    STP_IMP,        #0xDB
    NOP_IMP,        #0xDC
    CMP_ABSX,       #0xDD
    DEC_ABSX,       #0xDE
    BBS5_ZPR,       #0xDF
    CPX_IMMED,      #0xE0
    SBC_IZX,        #0xE1
    NOP_IMP,        #0xE2
    NOP_IMP,        #0xE3
    CPX_ZP,         #0xE4
    SBC_ZP,         #0xE5
    INC_ZP,         #0xE6
    SMB6_ZP,        #0xE7
    INX_IMP,        #0xE8
    SBC_IMMED,      #0xE9
    NOP_IMP,        #0xEA
    NOP_IMP,        #0xEB
    CPX_ABS,        #0xEC
    SBC_ABS,        #0xED
    INC_ABS,        #0xEE
    BBS6_ZPR,       #0xEF
    BEQ_REL,        #0xF0
    SBC_IZY,        #0xF1
    SBC_IZP,        #0xF2
    NOP_IMP,        #0xF3
    NOP_IMP,        #0xF4
    SBC_ZPX,        #0xF5
    INC_ZPX,        #0xF6
    SMB7_ZP,        #0xF7
    SED_IMP,        #0xF8
    SBC_ABSY,       #0xF9
    PLX_IMP,        #0xFA
    NOP_IMP,        #0xFB
    NOP_IMP,        #0xFC
    SBC_ABSX,       #0xFD
    INC_ABSX,       #0xFE
    BBS7_ZPR,       #0xFF
	]

#Emulation functions
#===================
def Execute6502(emu_PC,last_line):
    global emu_mem
    global emu_addresses
    global program_lines

    #TODO: support self mod
    if emu_PC not in emu_addresses:
        #Don't emulate if in unitialized memory
        if last_line!=-1:
            program_lines[last_line].execution_status="stopped"
        return False,emu_PC,last_line
    new_index=emu_addresses[emu_PC]
    
    if emu_PC+len(program_lines[new_index].bytes)>0x10000:
        #Don't emulate if part of instruction is beyond end of memory range
        if last_line!=-1:
            program_lines[last_line].execution_status="stopped"
        return False,emu_PC,last_line
    #Copy processor state to next line
    if last_line!=-1:
        #Transcrypt conversion to JavaScript does not support deepcopy
        #program_lines[new_index].CPU=deepcopy(program_lines[last_line].CPU)
        program_lines[new_index].CPU.classcopy(program_lines[last_line].CPU)
        program_lines[new_index].CPU.reset_changed()
    else:
        #No line to copy from - reset
        program_lines[new_index].CPU.reset_regs()
        program_lines[new_index].CPU.reset_changed()
    #Reset source and destination info
    program_lines[new_index].source_address=None
    program_lines[new_index].source_byte=None
    program_lines[new_index].dest_address=None
    program_lines[new_index].dest_byte=None
    #Call function in list corresponding to op code
    emu_PC=emu_ops[program_lines[new_index].bytes[0]](program_lines[new_index])
    program_lines[new_index].CPU.regs_valid=True
    if emu_PC==-1:
        #Catch BRK or other instruction halting execution
        program_lines[new_index].execution_status="stopped" 
        return False,emu_PC,last_line
    else:    
        last_line=new_index
        program_lines[new_index].execution_status="run" 
        return True,emu_PC,last_line

#Instruction modes
def FilterAddress(emu_line,byte_count,addition):
    global emu_mem
    if addition==-1:
        return -1
    address=addition
    for i in range(byte_count):
        byte=emu_mem[emu_line.address+i+1]
        if byte==-1:
            return -1
        address+=byte<<(i*8)
    return address%(0x100**byte_count)

def FilterZP(address,addition):
    global emu_mem
    if address==-1 or addition==-1:
        return -1
    address_lo=(address+addition)%0x100
    address_hi=(address+addition+1)%0x100
    if emu_mem[address_lo]==-1 or emu_mem[address_hi]==-1:
        return -1
    return emu_mem[address_lo]+emu_mem[address_hi]<<8

def mode_ABS(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,2,0)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_ABSX(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,2,emu_line.CPU.X)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_ABSY(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,2,emu_line.CPU.Y)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_IAX(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,2,emu_line.CPU.X)
    emu_line.source_address=address
    if address!=-1:
        address_lo=emu_mem[address]
        address_hi=emu_mem[(address+1)%0x10000]
        if address_lo==-1 or address_hi==-1:
            address=-1
        else:
            address=address_lo+(address_hi<<8)
    data=0 #dummy value
    return address,data

def mode_IMMED(emu_line):
    global emu_mem
    address=emu_line.address+1
    data=emu_mem[address]
    return address,data

def mode_IMP(emu_line):
    global emu_mem
    address=emu_line.address
    data=0  #dummy value
    return address,data

def mode_IND(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,2,0)
    emu_line.source_address=address
    if address!=-1:
        address_lo=emu_mem[address]
        address_hi=emu_mem[(address+1)%0x10000]
        if address_lo==-1 or address_hi==-1:
            address=-1
        else:
            address=address_lo+(address_hi<<8)
    data=0 #dummy value
    return address,data

def mode_IZP(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,1,0)
    address=FilterZP(address,0)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_IZX(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,1,0)
    address=FilterZP(address,emu_line.CPU.X)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_IZY(emu_line):
    global emu_mem
    if emu_line.CPU.Y==-1:
        address=-1
    else:
        address=FilterAddress(emu_line,1,0)
        address=FilterZP(address,0)
        address=(address+emu_line.CPU.Y)%0x10000
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_REL(emu_line):
    address=FilterAddress(emu_line,1,0)
    if address!=-1:
        if address<0x80:
            address=(emu_line.address+address+2)%0x10000
        else:
            address=(emu_line.address-(0x100-address)+2)
            if address<0:
                address+=0x10000
    data=0 #dummy value
    return address,data

def mode_ZP(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,1,0)
    data=emu_mem[address] if address!=-1 else -1
    return address,data
    
def mode_ZPX(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,1,emu_line.CPU.X)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_ZPY(emu_line):
    global emu_mem
    address=FilterAddress(emu_line,1,emu_line.CPU.Y)
    data=emu_mem[address] if address!=-1 else -1
    return address,data

def mode_ZPR(emu_line):
    global emu_mem
    address=emu_mem[emu_line.address+2]
    if address!=-1:
        if address<0x80:
            address=(emu_line.address+address+3)%0x10000
        else:
            address=(emu_line.address-(0x100-address)+3)
            if address<0:
                address+=0x10000
    data_address=emu_mem[emu_line.address+1]
    emu_line.source_address=data_address
    if data_address==-1:
        data=-1
    else:
        data=emu_mem[data_address]
    emu_line.source_byte=data
    return address,data

#Instruction helper functions
def RelAddress(emu_line,address,condition,size=2,invert=False):
    if address==-1:
        return -1
    if condition=="?":
        return -1
    if invert:
        condition=not condition
    if condition:
        #Branch taken
        emu_line.dest_address=address
        return address
    else:
        #Branch not taken
        return emu_line.address+size

def ZprAddress(emu_line,data,address,bit,BBS):
    if data==-1:
        address=-1
    else:
        if BBS:
            condition=data&(1<<bit)
        else:
            condition=not (data&(1<<bit))
        address=RelAddress(emu_line,address,condition,size=3)
    return address

def PushByte(emu_line,byte):
    global emu_mem
    if emu_line.CPU.SP!=-1:
        emu_mem[0x100+emu_line.CPU.SP]=byte
        emu_line.dest_address=0x100+emu_line.CPU.SP
        emu_line.CPU.SP=255 if emu_line.CPU.SP==0 else emu_line.CPU.SP-1
    else:
        emu_line.dest_address=-1
    emu_line.dest_byte=byte
    emu_line.CPU.SP_changed=True

def PullByte(emu_line):
    global emu_mem
    if emu_line.CPU.SP!=-1:
        emu_line.CPU.SP=0 if emu_line.CPU.SP==255 else emu_line.CPU.SP+1
        byte=emu_mem[0x100+emu_line.CPU.SP]
        emu_line.source_address=0x100+emu_line.CPU.SP
    else:
        byte=-1
        emu_line.source_address=-1
    emu_line.source_byte=byte
    emu_line.CPU.SP_changed=True
    return byte

def Compare(emu_line,data,cmp_val):
    if cmp_val==-1 or data==-1:
        emu_line.CPU.C="?"
        emu_line.CPU.N="?"
        emu_line.CPU.Z="?"
    else:
        emu_line.CPU.C=(cmp_val>=data)
        temp=(cmp_val+0x100-data)&0xFF
        emu_line.CPU.N=((temp&0x80)==0x80)
        emu_line.CPU.Z=(cmp_val==data)
    emu_line.CPU.C_changed=True
    emu_line.CPU.N_changed=True
    emu_line.CPU.Z_changed=True

def RMB(emu_line,address,data,bit):
    global emu_mem
    if data!=-1 and address!=-1:
        result=data&~(1<<bit)
        emu_mem[address]=result
    else:
        result=-1
    emu_line.source_address=address
    emu_line.source_byte=data
    emu_line.dest_address=address
    emu_line.dest_byte=result

def SMB(emu_line,address,data,bit):
    global emu_mem
    if data!=-1 and address!=-1:
        result=data|(1<<bit)
        emu_mem[address]=result
    else:
        result=-1
    emu_line.source_address=address
    emu_line.source_byte=data
    emu_line.dest_address=address
    emu_line.dest_byte=result

#Instructions
def op_ADC(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1 or emu_line.CPU.C=="?" or emu_line.CPU.D=="?":
        emu_line.CPU.A=-1
        emu_line.CPU.C="?"
        emu_line.CPU.V="?"
    else:
        if emu_line.CPU.D:
            #Decimal mode
            total=1 if emu_line.CPU.C else 0

            temp=emu_line.CPU.A&0xF
            total+=min(temp,9)
            temp=data&0xF
            total+=min(temp,9)
            if total>9:
                total+=6

            temp=emu_line.CPU.A&0xF0
            total+=min(temp,0x90)
            temp=data&0xF0
            total+=min(temp,0x90)
            if total>0x99:
                total+=0x60

            temp=total
        else:
            #Not decimal mode
            temp=emu_line.CPU.A+data
            if emu_line.CPU.C:
                temp+=1
        #Set C
        if temp>=0x100:
            emu_line.CPU.C=True
            temp-=0x100
        else:
            emu_line.CPU.C=False
        #Set V
        sign1=emu_line.CPU.A&0x80
        sign2=data&0x80
        sign3=temp&0x80
        if sign1==sign2 and sign1!=sign3:
            emu_line.CPU.V=True
        else:
            emu_line.CPU.V=False
        #Set A
        emu_line.CPU.A=temp
    emu_line.CPU.A_changed=True
    emu_line.CPU.C_changed=True
    emu_line.CPU.V_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address
    
def op_AND(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.A=-1
    else:
        emu_line.CPU.A&=data
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_ASL(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1:
            emu_line.CPU.A<<=1
            if emu_line.CPU.A>=0x100:
                emu_line.CPU.C=True
                emu_line.CPU.A-=0x100
            else:
                emu_line.CPU.C=False
        else:
            emu_line.CPU.C="?"
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1:
            result=data<<1
            if result>=0x100:
                emu_line.CPU.C=True
                result-=0x100
            else:
                emu_line.CPU.C=False
        else:
            result=-1
            emu_line.CPU.C="?"
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_BBR0(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,0,False)

def op_BBR1(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,1,False)

def op_BBR2(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,2,False)

def op_BBR3(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,3,False)

def op_BBR4(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,4,False)

def op_BBR5(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,5,False)

def op_BBR6(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,6,False)

def op_BBR7(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,7,False)

def op_BBS0(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,0,True)

def op_BBS1(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,1,True)

def op_BBS2(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,2,True)

def op_BBS3(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,3,True)

def op_BBS4(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,4,True)

def op_BBS5(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,5,True)

def op_BBS6(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,6,True)

def op_BBS7(emu_line,address,data,mode):
    return ZprAddress(emu_line,data,address,7,True)

def op_BCC(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.C,invert=True)

def op_BCS(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.C)

def op_BEQ(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.Z)

def op_BIT(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.Z="?"
    else:
        emu_line.CPU.Z=(emu_line.CPU.A&data)==0
    emu_line.CPU.Z_changed=True
    if mode!="IMMED":
        if emu_line.CPU.A==-1 or data==-1:
            emu_line.CPU.N="?"
            emu_line.CPU.V="?"
        else:
            emu_line.CPU.N=(data&0x80)==0x80
            emu_line.CPU.V=(data&0x40)==0x40
        emu_line.CPU.N_changed=True
        emu_line.CPU.V_changed=True
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_BMI(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.N)

def op_BNE(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.Z,invert=True)

def op_BPL(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.N,invert=True)

def op_BRA(emu_line,address,data,mode):
    emu_line.dest_address=address
    return address

def op_BRK(emu_line,address,data,mode):
    #Adddress of -1 halts execution
    return -1

def op_BVC(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.V,invert=True)
 
def op_BVS(emu_line,address,data,mode):
    return RelAddress(emu_line,address,emu_line.CPU.V)

def op_CLC(emu_line,address,data,mode):
    emu_line.CPU.C=False
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_CLD(emu_line,address,data,mode):
    emu_line.CPU.D=False
    emu_line.CPU.D_changed=True
    return emu_line.address

def op_CLI(emu_line,address,data,mode):
    emu_line.CPU.I=False
    emu_line.CPU.I_changed=True
    return emu_line.address

def op_CLV(emu_line,address,data,mode):
    emu_line.CPU.V=False
    emu_line.CPU.V_changed=True
    return emu_line.address

def op_CMP(emu_line,address,data,mode):
    Compare(emu_line,data,emu_line.CPU.A)
    return emu_line.address

def op_CPX(emu_line,address,data,mode):
    Compare(emu_line,data,emu_line.CPU.X)
    return emu_line.address

def op_CPY(emu_line,address,data,mode):
    Compare(emu_line,data,emu_line.CPU.Y)
    return emu_line.address

def op_DEC(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1:
            emu_line.CPU.A=255 if emu_line.CPU.A==0 else emu_line.CPU.A-1
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1:
            result=255 if data==0 else data-1
        else:
            result=-1
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    return emu_line.address

def op_DEX(emu_line,address,data,mode):
    if emu_line.CPU.X!=-1:
        emu_line.CPU.X=255 if emu_line.CPU.X==0 else emu_line.CPU.X-1
    emu_line.CPU.X_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.X)
    return emu_line.address

def op_DEY(emu_line,address,data,mode):
    if emu_line.CPU.Y!=-1:
        emu_line.CPU.Y=255 if emu_line.CPU.Y==0 else emu_line.CPU.Y-1
    emu_line.CPU.Y_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.Y)
    return emu_line.address

def op_EOR(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.A=-1
    else:
        emu_line.CPU.A^=data
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_INC(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1:
            emu_line.CPU.A=0 if emu_line.CPU.A==255 else emu_line.CPU.A+1
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1:
            result=0 if data==255 else data+1
        else:
            result=-1
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    return emu_line.address

def op_INX(emu_line,address,data,mode):
    if emu_line.CPU.X!=-1:
        emu_line.CPU.X=0 if emu_line.CPU.X==255 else emu_line.CPU.X+1
    emu_line.CPU.X_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.X)
    return emu_line.address

def op_INY(emu_line,address,data,mode):
    if emu_line.CPU.Y!=-1:
        emu_line.CPU.Y=0 if emu_line.CPU.Y==255 else emu_line.CPU.Y+1
    emu_line.CPU.Y_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.Y)
    return emu_line.address

def op_JMP(emu_line,address,data,mode):
    emu_line.dest_address=address
    return address

def op_JSR(emu_line,address,data,mode):
    address_lo=(emu_line.address+2)&0xFF
    address_hi=(emu_line.address+2)>>8
    PushByte(emu_line,address_hi)
    PushByte(emu_line,address_lo)
    emu_line.source_address=None
    emu_line.dest_address=address
    emu_line.dest_byte=None
    return address

def op_LDA(emu_line,address,data,mode):
    emu_line.CPU.A=data
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(data)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_LDX(emu_line,address,data,mode):
    emu_line.CPU.X=data
    emu_line.CPU.X_changed=True
    emu_line.CPU.setNZ(data)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_LDY(emu_line,address,data,mode):
    emu_line.CPU.Y=data
    emu_line.CPU.Y_changed=True
    emu_line.CPU.setNZ(data)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_LSR(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1:
            if emu_line.CPU.A&1:
                emu_line.CPU.C=True
            else:
                emu_line.CPU.C=False
            emu_line.CPU.A>>=1
        else:
            emu_line.CPU.C="?"
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1:
            if data&1:
                emu_line.CPU.C=True
            else:
                emu_line.CPU.C=False
            result=data>>1
        else:
            result=-1
            emu_line.CPU.C="?"
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_NOP(emu_line,address,data,mode):
    return emu_line.address

def op_ORA(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.A=-1
    else:
        emu_line.CPU.A|=data
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_PHA(emu_line,address,data,mode):
    PushByte(emu_line,emu_line.CPU.A)
    return emu_line.address

def op_PHP(emu_line,address,data,mode):
    flags="NV-BDIZC"
    byte=0
    mask=0x80
    for flag in flags:
        if flag=="-":
            byte|=mask
        else:
            temp_flag=getattr(emu_line.CPU,flag)
            if temp_flag=="?":
                byte=-1
            elif temp_flag:
                byte|=mask
        mask>>=1
    PushByte(emu_line,byte)
    return emu_line.address

def op_PHX(emu_line,address,data,mode):
    PushByte(emu_line,emu_line.CPU.X)
    return emu_line.address

def op_PHY(emu_line,address,data,mode):
    PushByte(emu_line,emu_line.CPU.Y)
    return emu_line.address

def op_PLA(emu_line,address,data,mode):
    emu_line.CPU.A=PullByte(emu_line)
    emu_line.CPU.setNZ(emu_line.CPU.A)
    emu_line.CPU.A_changed=True
    return emu_line.address

def op_PLP(emu_line,address,data,mode):
    flags="NV-BDIZC"
    mask=0x80
    byte=emu_line.CPU.A=PullByte(emu_line)
    for flag in flags:
        if flag!="-":
            if byte==-1:
                setattr(emu_line.CPU,flag,"?")
            elif byte&mask:
                setattr(emu_line.CPU,flag,True)
            else:
                setattr(emu_line.CPU,flag,False)
            setattr(emu_line.CPU,flag+"_changed",True)
        mask>>=1
    return emu_line.address

def op_PLX(emu_line,address,data,mode):
    emu_line.CPU.A=PullByte(emu_line)
    emu_line.CPU.setNZ(emu_line.CPU.X)
    emu_line.CPU.X_changed=True
    return emu_line.address

def op_PLY(emu_line,address,data,mode):
    emu_line.CPU.A=PullByte(emu_line)
    emu_line.CPU.setNZ(emu_line.CPU.Y)
    emu_line.CPU.Y_changed=True
    return emu_line.address

def op_RMB0(emu_line,address,data,mode):
    RMB(emu_line,address,data,0)
    return emu_line.address

def op_RMB1(emu_line,address,data,mode):
    RMB(emu_line,address,data,1)
    return emu_line.address

def op_RMB2(emu_line,address,data,mode):
    RMB(emu_line,address,data,2)
    return emu_line.address

def op_RMB3(emu_line,address,data,mode):
    RMB(emu_line,address,data,3)
    return emu_line.address

def op_RMB4(emu_line,address,data,mode):
    RMB(emu_line,address,data,4)
    return emu_line.address

def op_RMB5(emu_line,address,data,mode):
    RMB(emu_line,address,data,5)
    return emu_line.address

def op_RMB6(emu_line,address,data,mode):
    RMB(emu_line,address,data,6)
    return emu_line.address

def op_RMB7(emu_line,address,data,mode):
    RMB(emu_line,address,data,7)
    return emu_line.address

def op_ROL(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1 and emu_line.CPU.C!="?":
            emu_line.CPU.A<<=1
            if emu_line.CPU.C:
                emu_line.CPU.A|=1
            if emu_line.CPU.A>=0x100:
                emu_line.CPU.C=True
                emu_line.CPU.A-=0x100
            else:
                emu_line.CPU.C=False
        else:
            emu_line.CPU.C="?"
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1 and emu_line.CPU.C!="?":
            result=data<<1
            if emu_line.CPU.C:
                result|=1
            if result>=0x100:
                emu_line.CPU.C=True
                result-=0x100
            else:
                emu_line.CPU.C=False
        else:
            result=-1
            emu_line.CPU.C="?"
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_ROR(emu_line,address,data,mode):
    global emu_mem
    if mode=="IMP":
        if emu_line.CPU.A!=-1 and emu_line.CPU.C!="?":
            if emu_line.CPU.C:
                emu_line.CPU.A|=0x100
            if emu_line.CPU.A&1:
                emu_line.CPU.C=True
            else:
                emu_line.CPU.C=False
            emu_line.CPU.A>>=1
        else:
            emu_line.CPU.C="?"
        emu_line.CPU.A_changed=True
        emu_line.CPU.setNZ(emu_line.CPU.A)
    else:
        if data!=-1 and emu_line.CPU.C!="?":
            result=0x100 if emu_line.CPU.C else 0
            result|=data
            if data&1:
                emu_line.CPU.C=True
            else:
                emu_line.CPU.C=False
            result>>=1
        else:
            result=-1
            emu_line.CPU.C="?"
        emu_line.CPU.setNZ(result)
        emu_line.source_address=address
        emu_line.source_byte=data
        emu_line.dest_address=address
        emu_line.dest_byte=result
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_RTI(emu_line,address,data,mode):
    #Interrupts not implemented - halt
    return -1

def op_RTS(emu_line,address,data,mode):
    address_lo=PullByte(emu_line)
    address_hi=PullByte(emu_line)
    if address_lo==-1 or address_hi==-1:
        return -1
    ret_address=(address_lo+(address_hi<<8)+1)&0xFFFF
    emu_line.dest_address=ret_address
    return ret_address

def op_SBC(emu_line,address,data,mode):
    if emu_line.CPU.A==-1 or data==-1 or emu_line.CPU.C=="?" or emu_line.CPU.D=="?":
        emu_line.CPU.A=-1
        emu_line.CPU.C="?"
        emu_line.CPU.V="?"
    else:
        if emu_line.CPU.D:
            #Decimal mode
            ones=0 if emu_line.CPU.C else -1
            tens=0

            temp=emu_line.CPU.A&0xF
            ones+=min(temp,9)
            temp=data&0xF
            ones-=min(temp,9)
            if ones<0:
                tens-=1
                ones+=10

            temp=(emu_line.CPU.A&0xF0)>>4
            tens+=min(temp,9)
            temp=(data&0xF0)>>4
            tens-=min(temp,9)
            if tens<0:
                emu_line.CPU.C=False
                tens+=10
            else:
                emu_line.CPU.C=True

            temp=tens*0x10+ones

        else:
            #Not decimal mode
            temp=emu_line.CPU.A-data
            if not emu_line.CPU.C:
                temp-=1
            #Set C
            if temp<0:
                emu_line.CPU.C=False
                temp+=0x100
            else:
                emu_line.CPU.C=True
        #Set V
        sign1=emu_line.CPU.A&0x80
        sign2=data&0x80
        sign3=temp&0x80
        if sign1!=sign2 and sign1!=sign3:
            emu_line.CPU.V=True
        else:
            emu_line.CPU.V=False
        #Set A
        emu_line.CPU.A=temp
    emu_line.CPU.A_changed=True
    emu_line.CPU.C_changed=True
    emu_line.CPU.V_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    if mode!="IMMED":
        emu_line.source_address=address
        emu_line.source_byte=data
    return emu_line.address

def op_SEC(emu_line,address,data,mode):
    emu_line.CPU.C=True
    emu_line.CPU.C_changed=True
    return emu_line.address

def op_SED(emu_line,address,data,mode):
    emu_line.CPU.D=True
    emu_line.CPU.D_changed=True
    return emu_line.address

def op_SEI(emu_line,address,data,mode):
    emu_line.CPU.I=True
    emu_line.CPU.I_changed=True
    return emu_line.address

def op_SMB0(emu_line,address,data,mode):
    SMB(emu_line,address,data,0)
    return emu_line.address

def op_SMB1(emu_line,address,data,mode):
    SMB(emu_line,address,data,1)
    return emu_line.address

def op_SMB2(emu_line,address,data,mode):
    SMB(emu_line,address,data,2)
    return emu_line.address

def op_SMB3(emu_line,address,data,mode):
    SMB(emu_line,address,data,3)
    return emu_line.address

def op_SMB4(emu_line,address,data,mode):
    SMB(emu_line,address,data,4)
    return emu_line.address

def op_SMB5(emu_line,address,data,mode):
    SMB(emu_line,address,data,5)
    return emu_line.address

def op_SMB6(emu_line,address,data,mode):
    SMB(emu_line,address,data,6)
    return emu_line.address

def op_SMB7(emu_line,address,data,mode):
    SMB(emu_line,address,data,7)
    return emu_line.address

def op_STA(emu_line,address,data,mode):
    global emu_mem
    if address!=-1:
        emu_mem[address]=emu_line.CPU.A
    emu_line.dest_address=address
    emu_line.dest_byte=emu_line.CPU.A
    return emu_line.address

def op_STX(emu_line,address,data,mode):
    global emu_mem
    if address!=-1:
        emu_mem[address]=emu_line.CPU.X
    emu_line.dest_address=address
    emu_line.dest_byte=emu_line.CPU.X
    return emu_line.address

def op_STY(emu_line,address,data,mode):
    global emu_mem
    if address!=-1:
        emu_mem[address]=emu_line.CPU.Y
    emu_line.dest_address=address
    emu_line.dest_byte=emu_line.CPU.Y
    return emu_line.address

def op_STZ(emu_line,address,data,mode):
    global emu_mem
    if address!=-1:
        emu_mem[address]=0
    emu_line.dest_address=address
    emu_line.dest_byte=0
    return emu_line.address

def op_STP(emu_line,address,data,mode):
    return -1

def op_TAX(emu_line,address,data,mode):
    emu_line.CPU.X=emu_line.CPU.A
    emu_line.CPU.X_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.X)
    return emu_line.address

def op_TAY(emu_line,address,data,mode):
    emu_line.CPU.Y=emu_line.CPU.A
    emu_line.CPU.Y_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.Y)
    return emu_line.address

def op_TRB(emu_line,address,data,mode):
    global emu_mem
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.Z="?"
        result=-1
    else:
        emu_line.CPU.Z=(emu_line.CPU.A&data)==0
        result=data&(emu_line.CPU.A^0xFF)
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.Z_changed=True
    emu_line.CPU.A_changed=True
    emu_line.source_address=address
    emu_line.source_byte=data
    emu_line.dest_address=address
    emu_line.dest_byte=result
    return emu_line.address

def op_TSB(emu_line,address,data,mode):
    global emu_mem
    if emu_line.CPU.A==-1 or data==-1:
        emu_line.CPU.Z="?"
        result=-1
    else:
        emu_line.CPU.Z=(emu_line.CPU.A&data)==0
        result=data|emu_line.CPU.A
        if address!=-1:
            emu_mem[address]=result
    emu_line.CPU.Z_changed=True
    emu_line.CPU.A_changed=True
    emu_line.source_address=address
    emu_line.source_byte=data
    emu_line.dest_address=address
    emu_line.dest_byte=result
    return emu_line.address

def op_TSX(emu_line,address,data,mode):
    emu_line.CPU.X=emu_line.CPU.SP
    emu_line.CPU.X_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.X)
    return emu_line.address

def op_TXA(emu_line,address,data,mode):
    emu_line.CPU.A=emu_line.CPU.X
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    return emu_line.address

def op_TXS(emu_line,address,data,mode):
    emu_line.CPU.SP=emu_line.CPU.X
    emu_line.CPU.SP_changed=True
    return emu_line.address

def op_TYA(emu_line,address,data,mode):
    emu_line.CPU.A=emu_line.CPU.Y
    emu_line.CPU.A_changed=True
    emu_line.CPU.setNZ(emu_line.CPU.A)
    return emu_line.address

def op_WAI(emu_line,address,data,mode):
    return -1

