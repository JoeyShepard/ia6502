#!/usr/bin/env python3

#***************************************************
#* Screen output for drawing interactive assembler *
#* (works with Brython or Linux version)           *
#***************************************************


#Constants
#=========
MAX_INPUT_LEN=20    #Maximum character input in assembly source

STATUS_WIDTH=1                  #Width of column showing > for emulated line
ADDRESS_WIDTH=7                 #Width of column showing assembled address
BYTES_WIDTH=16                  #Width of column showing assembled bytes
INPUT_WIDTH=21                  #Width of column showing assembly input
REG_A_WIDTH=3                   #Width of column showing value of A register
REG_A_CHAR_WIDTH=4              #Width of column showing character value of A register
REG_X_WIDTH=4                   #Width of column showing value of X register
REG_Y_WIDTH=4                   #Width of column showing value of Y register
REG_SP_WIDTH=4+1                #Width of column showing value of SP register. +1 spacing between sections
FLAGS_WIDTH=9+1                 #Width of column showing value of flags. +1 spacing between sections
SOURCE_WIDTH=len("$C000: $AB ") #Width of column showing source address and value
DEST_WIDTH=len("$C000: $AB ")   #Width of column showing destinarion address and value

START_X=0                               #Starting X value for printing columns
STATUS_X=START_X                        #X value for column showing > for emulated line
ADDRESS_X=STATUS_X+STATUS_WIDTH         #X value for column showing assembled address
BYTES_X=ADDRESS_X+ADDRESS_WIDTH         #X value for column showing assembled bytes
INPUT_X=BYTES_X+BYTES_WIDTH             #X value for column showing assembly input
REG_A_X=INPUT_X+INPUT_WIDTH             #X value for column showing value of A register
REG_A_CHAR_X=REG_A_X+REG_A_WIDTH        #X value for column showing character value of A register
REG_X_X=REG_A_CHAR_X+REG_A_CHAR_WIDTH   #X value for column showing value of X register
REG_Y_X=REG_X_X+REG_X_WIDTH             #X value for column showing value of Y register
REG_SP_X=REG_Y_X+REG_Y_WIDTH            #X value for column showing value of SP register
FLAGS_X=REG_SP_X+REG_SP_WIDTH           #X value for column showing value of flags
SOURCE_X=FLAGS_X+FLAGS_WIDTH            #X value for column showing source address and value
DEST_X=SOURCE_X+SOURCE_WIDTH            #X value for column showing destination address and value

#Header text of columns
HEADER_TEXT="Program              A      X   Y   SP   NV-BDIZC  Source     Destination"
HEADER_X=INPUT_X                        #X value of header text
HEADER_Y=0                              #Y value of header text

LINES_START_Y=1                         #Y value of first assembly input line

#Globals
#=======
output_funcs={}                         #List of output functions so included module can use output function of including module

#Functions
#=========

#Transcrypt does not translate hex function so reimplement :/
#(Switched from Transcrypt to Brython)
def hex(num):
    if num<0:
        return "0x0"
    result=""
    while num:
        remainder=num%16
        if remainder<10:
            result=str(remainder)+result
        else:
            result=chr(87+remainder)+result
        num=int(num/16)
    if result=="":
        result="0"
    return "0x"+result

#Convert number to uppercase hex without leading 0x
# ie, Hex2("0xab") returns "AB"
def Hex2(num):
    if num==-1:
        return "??"
    else:
        return ("00"+hex(num)[2:])[-2:].upper()

#Convert number to uppercase hex without leading 0x
# ie, Hex4("0xabcd") returns "ABCD"
def Hex4(num):
    if num==-1:
        return "????"
    else:
        #Bugged in Transcrypt! Though switched to Brython
        #return ("0000"+hex(num)[2:])[-4:].upper()
        result=(("0000"+(hex(num)[2:]))).upper()
        return result[-4:]

#Redraw entire assembler screen
#Abstracted out here since JavaScript version is key and timer driven instead of input loop
def DrawAssembler(program_lines,screen,editor_state):
    global output_funcs

    #Text drawing function supplied by output module
    DrawTextFunc=output_funcs["DrawText"]

    #Draw headers of columns: Program, register names, flags, etc
    DrawTextFunc(HEADER_X,HEADER_Y,HEADER_TEXT,screen)

    #Draw lines of assembly input
    for i,line in enumerate(program_lines):
        #Calculate Y offset once of lines of assembly
        draw_y=LINES_START_Y+i

        #Stop printing lines if reached bottom of screen
        if draw_y>editor_state.row_count-2:
            break

        #Execution status in status column of each executed line if executed
        if line.execution_status=="run":
            DrawTextFunc(STATUS_X,draw_y,">",screen,"status run")
        elif line.execution_status=="stopped":
            DrawTextFunc(STATUS_X,draw_y,">",screen,"status stopped")

        #Assembled bytes for line of assembly
        address_error=False
        if line.byte_overlap:
            #Bytes generated for line overlapped bytes generated by other line - error
            DrawTextFunc(BYTES_X,draw_y,"Byte overlap!",screen,"bytes error")
            address_error=True
        elif line.bytes!=[]:
            #Bytes did not overlap - draw
            draw_x=BYTES_X
            for i,byte in enumerate(line.bytes):
                if i==4:
                    #Max 4 bytes on screen given column width    
                    DrawTextFunc(draw_x,draw_y,"...",screen)
                    break
                elif byte==[]:
                    #Byte uninitialized
                    DrawTextFunc(draw_x,draw_y,"??",screen,"bytes unknown")
                    DrawTextFunc(draw_x+2,draw_y," ",screen)
                else:
                    #Draw byte value
                    DrawTextFunc(draw_x,draw_y,Hex2(byte)+" ",screen)
                #Advance text cursor by 3 - width of printed byte and space
                draw_x+=3
        else:
            #Byte list empty - syntax error (handled above), blank line (ignore) or instruction with wrong addressing mode like SEC 5
            if line.mode_not_found:
                #Don't warn if only instruction since probably about to type argument 
                if len(line.simplified_symbol_list)!=1 or not line.selected_line:
                    #Flag error if no bytes generated for instruction
                    DrawTextFunc(BYTES_X,draw_y,"Mode not found!",screen,"bytes error")
                    address_error=True
            elif line.range_error:
                DrawTextFunc(BYTES_X,draw_y,"Range error!",screen,"bytes error")
                address_error=True
        
        #Address of line of assembly
        #(Place second since assembled bytes above may change address color)
        if line.symbol_error or line.address==-1 or address_error: 
            color="line error"
        elif line.symbol_unknown and (not line.symbol_unknown_last or not line.selected_line):
            color="line unknown"
        else:
            color="none"
        address=Hex4(line.address)
        DrawTextFunc(ADDRESS_X,draw_y,address,screen,color)
        DrawTextFunc(ADDRESS_X+5,draw_y,":",screen)

        #Assembly text source for line of assembly
        draw_x=INPUT_X
        #Loop through list of colored text and draw
        for text,color in line.text_symbol_list:
            DrawTextFunc(draw_x,draw_y,text,screen,color)
            draw_x+=len(text)
      
        #Draw values of registers after emulating line of assembly
        if line.CPU.regs_valid:
            draw_x=REG_A_X
            for reg in ["A","X","Y","SP"]:
                reg_val=getattr(line.CPU,reg)
                reg_changed=getattr(line.CPU,reg+"_changed")
                if reg=="A":
                    #Only draw character value of A register if printable character
                    if reg_val<32 or (reg_val>=127 and reg_val<=160):
                        reg_char=" "
                    else:
                        reg_char=chr(reg_val)
                reg_output=Hex2(reg_val)
                #Color register differently if line of assembly changed value in emulation
                if reg_changed: 
                    reg_color="reg changed" 
                elif reg_output=="??": 
                    reg_color="reg unknown" 
                else:
                    reg_color="reg unchanged" 
                
                #Draw value of each register after emulation
                draw_x=DrawTextFunc(draw_x,draw_y,"$"+reg_output,screen,reg_color)  
                if reg=="A":
                    #Draw character value of A register only
                    draw_x=DrawTextFunc(draw_x,draw_y,"("+reg_char+") ",screen,reg_color)  
                else:
                    draw_x+=1

            #Draw flags after emulating line of assembly
            draw_x=FLAGS_X
            for flag in "NVBDIZC": 
                flag_val=getattr(line.CPU,flag)
                flag_changed=getattr(line.CPU,flag+"_changed")
                #If flag value unknown after emulating (ie calculated based on unknown value) draw "?"
                if flag_val=="?":
                    flag_output="?"
                elif flag_val==True:
                    #Draw flag in uppercase if true
                    flag_output=flag
                else:
                    #Draw flag in lowercase if false
                    flag_output=flag.lower()

                #Color flag if changed
                if flag_changed:
                    if flag_val:
                        flag_color="flag changed true"
                    elif flag:
                        flag_color="flag changed false"
                elif flag_val=="?":
                    #If flag did not change and is unknown, color to to relfect that
                    flag_color="flag unknown"
                else:
                    flag_color="flag unchanged"
                draw_x=DrawTextFunc(draw_x,draw_y,flag_output,screen,flag_color)
                #Flags register is 8 bits though only 7 bits used. Print "-" for bit 5.
                if flag=="V":
                    draw_x=DrawTextFunc(draw_x,draw_y,"-",screen,flag_color)

            #Columns showing source and destination address and byte for emulated instructions that have them
            draw_x=SOURCE_X
            #Emulation sets source address, if any. Only draw if set.
            if line.source_address!=None:
                #Color byte differently uninitialized
                source_color="bytes unknown" if line.source_address==-1 else "none"
                draw_x=DrawTextFunc(draw_x,draw_y,"$"+Hex4(line.source_address),screen,source_color)
                #Don't draw source byte if uninitialized or not set
                if line.source_address!=-1 and line.source_byte!=None:
                    source_color="bytes unknown" if line.source_byte==-1 else "none"
                    DrawTextFunc(draw_x,draw_y,":$"+Hex2(line.source_byte),screen,source_color)
            draw_x=DEST_X
            #Emulation sets destination address, if any. Only draw if set.
            if line.dest_address!=None:
                dest_color="bytes unknown" if line.dest_address==-1 else "none"
                draw_x=DrawTextFunc(draw_x,draw_y,"$"+Hex4(line.dest_address),screen,dest_color)
                #Don't draw destination byte if not set, but do draw even if uninitialized
                if line.dest_byte!=None:
                    draw_x=DrawTextFunc(draw_x,draw_y,":",screen,"none")
                    #dest_color="bytes unknown" if line.dest_byte==-1 else "none"
                    dest_color="reg changed"
                    DrawTextFunc(draw_x,draw_y,"$"+Hex2(line.dest_byte),screen,dest_color)

def DrawStatusLine(screen,editor_state):
    global output_funcs

    #Text drawing function supplied by output module
    DrawTextFunc=output_funcs["DrawText"]

    status_msg=" "+editor_state.status_line+" "
    DrawTextFunc(0,editor_state.row_count-1,status_msg,screen,"status line")


