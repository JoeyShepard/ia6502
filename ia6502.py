#!/usr/bin/env python3

#TODO: more comments
#TODO: screen refresh very noticeable
#TODO: limit number of new lines or scroll
#TODO: breakpoints?
#TODO: eliminate combine.py
#TODO: status output
#TODO: Add cycles column
#TODO: help message and exit
#TODO: check all other files for TODO

#TODO at end:
# - Kowalski cant do LDA 3+(4)
# - double check all debug_msgs removed
# - check flags in Kowalski
# - check instructions in Kowalski
# - all TODOs

#Linux console version with curses
from ia6502.linux import *

#JavaScript version converted with Transcrypt
#from ia6502.transcrypt import *

from sys import path, argv
from sys import exit
from ia6502.emulator import *
from ia6502.output import *

output_funcs["DrawText"]=DrawText

def InteractiveAssembler(screen=None):
    global label_list
    global set_symbol_list
    global emu_mem
    global emu_addresses
    global program_lines
    global COLOR_DICT
    global file_input

    #Initialize colors pairs
    InitColors()

    #Editor variables
    current_line=0
    key=""
    input_str=""
    input_ptr=0
   
    #Main loop
    redraw_text=True
    last_mode="key"
    while(True):
        if redraw_text and not file_input:
            #Draw assembler output
            ClearScreen(screen)
            DrawAssembler(program_lines,screen)
            ReturnCursor(INPUT_X+input_ptr,LINES_START_Y+current_line,screen)
            EndDrawing(screen)

        #Process keys
        if file_input:
            key=file_input[0]
            if key==chr(10):
                key="KEY_ENTER"
            file_input=file_input[1:]
        else:
            key=KeyInput(screen)
            if key!="TIMEOUT":
                last_mode="key"
                redraw_text=True
        resimulate=False
        
        if key=="TIMEOUT":
            #Timeout expired without keypress - reassemble and emulate
            resimulate=True
            key=""
            if last_mode=="key":
                redraw_text=True
            else:
                redraw_text=False
            last_mode="timeout"
        elif key=="KB_INTERRUPT":
            #Ctrl+C - exit program
            #Keyboard handler never returns this code in JavaScript version
            exit()
        elif key=="KEY_RESIZE":
            resimulate=True
        elif key=="KEY_BACKSPACE":
            if input_ptr!=0:
                input_str=input_str[:input_ptr-1]+input_str[input_ptr:]
                input_ptr-=1
            elif current_line>0:
                if len(program_lines[current_line-1].raw_str)+len(input_str)<=MAX_INPUT_LEN:
                    del program_lines[current_line]
                    input_str=program_lines[current_line-1].raw_str+input_str
                    input_ptr=len(program_lines[current_line-1].raw_str)
                    current_line-=1
                else:
                    redraw_text=False
            else:
                redraw_text=False
        elif key=="KEY_LEFT":
            if input_ptr>0:
                input_ptr-=1
            elif current_line>0:
                program_lines[current_line].raw_str=input_str
                input_str=program_lines[current_line-1].raw_str
                input_ptr=len(input_str)
                current_line-=1
            else:
                redraw_text=False
        elif key=="KEY_RIGHT":
            if input_ptr<len(input_str):
                input_ptr+=1
            elif current_line<len(program_lines)-1:
                program_lines[current_line].raw_str=input_str
                input_str=program_lines[current_line+1].raw_str
                input_ptr=0
                current_line+=1
            else:
                redraw_text=False
        elif key=="KEY_UP":
            if current_line>0:
                program_lines[current_line].raw_str=input_str
                input_str=program_lines[current_line-1].raw_str
                if input_ptr>len(input_str):
                    input_ptr=len(input_str)
                current_line-=1
            elif input_ptr>0:
                input_ptr=0
            else:
                redraw_text=False
        elif key=="KEY_DOWN":
            if current_line<len(program_lines)-1:
                program_lines[current_line].raw_str=input_str
                input_str=program_lines[current_line+1].raw_str
                if input_ptr>len(input_str):
                    input_ptr=len(input_str)
                current_line+=1
            elif input_ptr<len(input_str):
                input_ptr=len(input_str)
            else:
                redraw_text=False
        elif key=="KEY_HOME":
            if input_ptr!=0:
                input_ptr=0
            else:
                redraw_text=False
        elif key=="KEY_END":
            if input_ptr!=len(input_str):
                input_ptr=len(input_str)
            else:
                redraw_text=False
        elif key=="KEY_DC":
            if input_ptr!=len(input_str):
                input_str=input_str[:input_ptr]+input_str[input_ptr+1:]
            elif current_line<len(program_lines)-1:
                if len(program_lines[current_line+1].raw_str)+len(input_str)<=MAX_INPUT_LEN:
                    input_str+=program_lines[current_line+1].raw_str
                    del program_lines[current_line+1]
                else:
                    redraw_text=False
            else:
                redraw_text=False
        elif key=="KEY_ENTER":
            program_lines[current_line].raw_str=input_str[:input_ptr]
            program_lines.insert(current_line+1,LineClass())
            current_line+=1
            input_str=input_str[input_ptr:]
            input_ptr=0
        elif len(key)==1 and len(input_str)<MAX_INPUT_LEN:
            #Avoid escaped characters and other junk
            if key.isalnum() or key in " ~`!@#$%^&*()_+-={}[];':<>,.?/|\"\\":
                #TODO: does not work for F1-F12 - inserts multiple characters?
                input_str=input_str[:input_ptr]+key+input_str[input_ptr:]
                input_ptr+=1
        else:
            redraw_text=False

        #Update program line
        if redraw_text and not file_input:
            program_lines[current_line].raw_str=input_str
            program_lines[current_line].raw_str_ptr=input_ptr

            #Clear all labels and symbols
            label_list.clear()
            set_symbol_list.clear()

            #First assembler pass
            current_address=START_ADDRESS
            symbol_unknown_indexes=[]
            for i,line in enumerate(program_lines):
                line.address=current_address
                line.selected_line=(i==current_line)
                line.replaced_symbols={}
                line.pass_number=1
                current_address=line.update(current_address)
                if line.symbol_unknown:
                    symbol_unknown_indexes+=[i]
                current_address+=len(line.bytes)

            #Fill in forward referenced labels
            for i in symbol_unknown_indexes:
                program_lines[i].selected_line=(i==current_line)
                program_lines[i].pass_number=2
                program_lines[i].update(current_address)
                
            #Insert generated bytes into emulator memory
            #(Do here in separate loop so overlap errors flagged in order they appear in source)
            emu_mem.clear()
            emu_mem+=[-1]*(2**16)
            emu_addresses.clear()

            for i,line in enumerate(program_lines):
                if line.address>0xFFFF:
                    #Mark address invalid if out of range even if no bytes generated
                    line.address=-1
                calc_address=line.address
                exit_early=False
                new_bytes=[]
                for byte in line.bytes:
                    if calc_address>0xFFFF:
                        #Mark address invalid if generated byte out of range
                        line.address=-1
                        exit_early=True
                    elif emu_mem[calc_address]!=-1:
                        #Mark address as overlapped if byte already exists at address
                        line.byte_overlap=True
                        exit_early=True
                    elif not line.symbol_unknown:
                        #Save byte for writing to memory unless line contains unresolved symbols
                        new_bytes+=[byte]
                        calc_address+=1
                    if exit_early:
                        break

                #If loop above successful, insert bytes into memory
                if not exit_early:
                    calc_address=line.address
                    for byte in new_bytes:
                        emu_mem[calc_address]=byte
                        emu_addresses[calc_address]=i
                        calc_address+=1

            #Simulate if enough time has passed since last key press
            if resimulate:
                #First, look through source lines for starting instruction
                #Also, reset emulation status

                instruction_found=False
                for line in program_lines:
                    if line.bytes and not line.symbol_unknown and not instruction_found:
                        instruction_found=True
                        emu_PC=line.address
                    line.execution_status="none"
                    line.CPU.regs_valid=False
              
                #If instruction found, start executing
                if instruction_found:
                    last_line=-1
                    for i in range(MAX_INSTRUCTIONS):
                        success,emu_PC,last_line=Execute6502(emu_PC,last_line)
                        if not success:
                            break
                    #TODO: else? color cursor if max reached. color red?

#Get file input and exit if any command line errors
file_input=FileInput(argv)

#Enter interactive assembler 
BeginAssembler(InteractiveAssembler)


