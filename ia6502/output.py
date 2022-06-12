#Constants
#=========
MAX_INPUT_LEN=20

STATUS_WIDTH=1
ADDRESS_WIDTH=7
BYTES_WIDTH=16
INPUT_WIDTH=21
REG_A_WIDTH=3
REG_A_CHAR_WIDTH=4
REG_X_WIDTH=4
REG_Y_WIDTH=4
REG_SP_WIDTH=4+1    #+1 spacing between sections
FLAGS_WIDTH=9+1     #+1 spacing between sections
SOURCE_WIDTH=len("$C000: $AB ")
DEST_WIDTH=len("$C000: $AB ")

START_X=0
STATUS_X=START_X
ADDRESS_X=STATUS_X+STATUS_WIDTH
BYTES_X=ADDRESS_X+ADDRESS_WIDTH
INPUT_X=BYTES_X+BYTES_WIDTH
REG_A_X=INPUT_X+INPUT_WIDTH
REG_A_CHAR_X=REG_A_X+REG_A_WIDTH
REG_X_X=REG_A_CHAR_X+REG_A_CHAR_WIDTH
REG_Y_X=REG_X_X+REG_X_WIDTH
REG_SP_X=REG_Y_X+REG_Y_WIDTH
FLAGS_X=REG_SP_X+REG_SP_WIDTH
SOURCE_X=FLAGS_X+FLAGS_WIDTH
DEST_X=SOURCE_X+SOURCE_WIDTH

HEADER_TEXT="Program              A      X   Y   SP   NV-BDIZC  Source     Destination"
HEADER_X=INPUT_X
HEADER_Y=0

LINES_START_Y=1

#Globals
#=======
output_funcs={}

#Functions
#=========
def Hex2(num):
    if num==-1:
        return "??"
    else:
        return ("00"+hex(num)[2:])[-2:].upper()

def Hex4(num):
    if num==-1:
        return "????"
    else:
        return ("0000"+hex(num)[2:])[-4:].upper()

def DrawAssembler(program_lines,screen=None):
    global output_funcs

    #Text drawing function supplied by module
    DrawTextFunc=output_funcs["DrawText"]

    #Draw headers
    DrawTextFunc(HEADER_X,HEADER_Y,HEADER_TEXT,screen)

    #Draw lines
    for i,line in enumerate(program_lines):
        #Calculate Y offset once
        draw_y=LINES_START_Y+i

        #Execution status
        if line.execution_status=="run":
            DrawTextFunc(STATUS_X,draw_y,">",screen,"status run")
        elif line.execution_status=="stopped":
            DrawTextFunc(STATUS_X,draw_y,">",screen,"status stopped")

        #Address
        if line.symbol_error or line.address==-1:
            color="line error"
        elif line.symbol_unknown and (not line.symbol_unknown_last or not line.selected_line):
            color="line unknown"
        else:
            color="none"
       
        #TODO: why did I add support for $$$$ here?
        address=Hex4(line.address)
        DrawTextFunc(ADDRESS_X,draw_y,address,screen,color)
        DrawTextFunc(ADDRESS_X+5,draw_y,":",screen)

        #Assembled bytes
        if line.byte_overlap:
            DrawTextFunc(BYTES_X,draw_y,"Byte overlap!",screen,"bytes error")
        elif line.bytes!=[]:
            draw_x=BYTES_X
            for i,byte in enumerate(line.bytes):
                if i==4:
                    #Max 4 bytes on screen given column width    
                    DrawTextFunc(draw_x,draw_y,"...",screen)
                    break
                elif byte==[]:
                    DrawTextFunc(draw_x,draw_y,"??",screen,"bytes unknown")
                    DrawTextFunc(draw_x+2,draw_y," ",screen)
                else:
                    DrawTextFunc(draw_x,draw_y,Hex2(byte)+" ",screen)
                draw_x+=3
        else:
            #Byte list empty - syntax error (handled above), blank line (ignore) or instruction with wrong addressing mode like SEC 5
            if line.mode_not_found:
                #Don't warn if only instruction since probably about to type argument 
                if len(line.simplified_symbol_list)!=1 or not line.selected_line:
                    DrawTextFunc(BYTES_X,draw_y,"Mode not found!",screen,"bytes error")
            elif line.range_error:
                DrawTextFunc(BYTES_X,draw_y,"Range error!",screen,"bytes error")

        #Text input
        draw_x=INPUT_X
        for text,color in line.text_symbol_list:
            DrawTextFunc(draw_x,draw_y,text,screen,color)
            draw_x+=len(text)
       
        if line.CPU.regs_valid:
            #Registers
            draw_x=REG_A_X
            for reg in ["A","X","Y","SP"]:
                reg_val=getattr(line.CPU,reg)
                reg_changed=getattr(line.CPU,reg+"_changed")
                if reg=="A":
                    if reg_val<32 or (reg_val>=127 and reg_val<=160):
                        reg_char=" "
                    else:
                        reg_char=chr(reg_val)
                reg_output=Hex2(reg_val)
                if reg_changed: 
                    reg_color="reg changed" 
                elif reg_output=="??": 
                    reg_color="reg unknown" 
                else:
                    reg_color="reg unchanged" 

                draw_x=DrawTextFunc(draw_x,draw_y,"$"+reg_output,screen,reg_color)  
                if reg=="A":
                    draw_x=DrawTextFunc(draw_x,draw_y,"("+reg_char+") ",screen,reg_color)  
                else:
                    draw_x+=1

            #Flags
            draw_x=FLAGS_X
            for flag in "NVBDIZC": 
                flag_val=getattr(line.CPU,flag)
                flag_changed=getattr(line.CPU,flag+"_changed")
                if flag_val=="?":
                    flag_output="?"
                elif flag_val==True:
                    flag_output=flag
                else:
                    flag_output=flag.lower()

                if flag_changed:
                    if flag_val:
                        flag_color="flag changed true"
                    elif flag:
                        flag_color="flag changed false"
                elif flag_val=="?":
                    flag_color="flag unknown"
                else:
                    flag_color="flag unchanged"
                draw_x=DrawTextFunc(draw_x,draw_y,flag_output,screen,flag_color)
                if flag=="V":
                    draw_x=DrawTextFunc(draw_x,draw_y,"-",screen,flag_color)

            #Source and destination
            draw_x=SOURCE_X
            if line.source_address!=None:
                source_color="bytes unknown" if line.source_address==-1 else "none"
                draw_x=DrawTextFunc(draw_x,draw_y,"$"+Hex4(line.source_address),screen,source_color)
                if line.source_address!=-1 and line.source_byte!=None:
                    source_color="bytes unknown" if line.source_byte==-1 else "none"
                    DrawTextFunc(draw_x,draw_y,":$"+Hex2(line.source_byte),screen,source_color)
            draw_x=DEST_X
            if line.dest_address!=None:
                dest_color="bytes unknown" if line.dest_address==-1 else "none"
                draw_x=DrawTextFunc(draw_x,draw_y,"$"+Hex4(line.dest_address),screen,dest_color)
                if line.dest_byte!=None:
                    draw_x=DrawTextFunc(draw_x,draw_y,":",screen,"none")
                    #dest_color="bytes unknown" if line.dest_byte==-1 else "none"
                    dest_color="reg changed"
                    DrawTextFunc(draw_x,draw_y,"$"+Hex2(line.dest_byte),screen,dest_color)


