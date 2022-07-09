#!/usr/bin/env python3

#****************************************
#* Main 6502 Interactive Assembler file *
#****************************************

#TODO: limit number of new lines or scroll
#      - limited lines printed but what to do when cursor goes off screen?
#TODO: one TODO in emulator.py

#TODO at end:
# - Kowalski cant do LDA 3+(4)
# - check flags in Kowalski
#   - what did I mean?
# - check missing instructions in Kowalski
#   - rmb?
# - README.md

#Linux console version with curses
from ia6502.linux import *

#JavaScript version converted with Brython
#from ia6502.brython import *

from ia6502.emulator import *
from ia6502.output import *

#Output functions defined in ia6502.linux or ia6502.brython
output_funcs["DrawText"]=DrawText

#Editor variables - needs to be global for JavaScript version
editor_state=EditorStateClass()
timer_id=None

#Step to be performed every time keypress/timeout received
def AssemblerStep(editor_state,key):
    global label_list       #List of labels defined in program
    global set_symbol_list  #List of symbols defined with .SET directive
    global emu_mem          #Emulator memory - 64k
    global emu_addresses    #Dictionary of addresses with code or data defined in aseembly source
    global program_lines    #List of source lines containing parsed symbols and CPU state
    global COLOR_DICT       #Dictionary of colors by use (registers, numbers, etc)

    #Make local copies of editor_state members. Restore below.
    #Originally designed as part of InteractiveAssembler. Factored out to work with Brython.
    current_line=editor_state.current_line
    input_str=editor_state.input_str 
    input_ptr=editor_state.input_ptr
    redraw_text=editor_state.redraw_text
    last_mode=editor_state.last_mode
    
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
        ExitProgram()
    elif key=="KEY_RESIZE":
        #Signal that terminal was resized
        resimulate=True
    elif key=="KEY_BACKSPACE":
        if input_ptr!=0:
            #Delete character in source line
            input_str=input_str[:input_ptr-1]+input_str[input_ptr:]
            input_ptr-=1
        elif current_line>0:
            #At position 0 - copy line to line above if room
            if len(program_lines[current_line-1].raw_str)+len(input_str)<=MAX_INPUT_LEN:
                del program_lines[current_line]
                input_str=program_lines[current_line-1].raw_str+input_str
                input_ptr=len(program_lines[current_line-1].raw_str)
                current_line-=1
            else:
                #Don't redraw if didn't copy line to line above
                redraw_text=False
        else:
            #Don't redraw if nothing deleted
            redraw_text=False
    elif key=="KEY_LEFT":
        if input_ptr>0:
            input_ptr-=1
        elif current_line>0:
            #At beginning of line - move to line above
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
            #At end of line - move to line below
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
            #At first line - move cursor to beginning of line
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
            #At last line - move cursor to end of line
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
    elif key=="KEY_DC": #Delete key
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
            input_str=input_str[:input_ptr]+key+input_str[input_ptr:]
            input_ptr+=1
    else:
        redraw_text=False

    #Update program line
    if redraw_text:
        #Save currently edited line
        program_lines[current_line].raw_str=input_str
        program_lines[current_line].raw_str_ptr=input_ptr

        #Clear all labels and symbols
        label_list.clear()
        set_symbol_list.clear()

        #First assembler pass
        current_address=START_ADDRESS
        symbol_unknown_indexes=[]
        for i,line in enumerate(program_lines):
            #Resolve symbols and generate machine code where possible
            line.address=current_address
            line.selected_line=(i==current_line)
            line.replaced_symbols={}
            line.pass_number=1
            current_address=line.update(current_address)
            #Keep track of lines with forward referenced labels and other unknown symbols
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
                #First line with bytes without unresolved symbols
                if line.bytes and not line.symbol_unknown and not instruction_found:
                    instruction_found=True
                    emu_PC=line.address
                line.execution_status="none"
                line.CPU.regs_valid=False
          
            #If instruction found, start executing
            if instruction_found:
                last_line=-1
                instruction_count=0
                for i in range(MAX_INSTRUCTIONS):
                    success,emu_PC,last_line=Execute6502(emu_PC,last_line)
                    if not success:
                        plural="s" if instruction_count!=1 else ""
                        editor_state.status_line=f"Emulated {instruction_count} instruction{plural}"
                        break
                    instruction_count+=1
                else:
                    if last_line!=-1:
                        program_lines[last_line].execution_status="stopped"
                    plural="s" if instruction_count!=1 else ""
                    editor_state.status_line=f"Halted after {instruction_count} instruction{plural}"
        else:
            editor_state.status_line="Typing..."

    #Stuff editor state variables back into class object
    editor_state.current_line=current_line
    editor_state.input_str=input_str 
    editor_state.input_ptr=input_ptr
    editor_state.redraw_text=redraw_text
    editor_state.last_mode=last_mode

#Draw assembler output
def DrawAll(screen,editor_state):
    ClearScreen(screen)
    DrawAssembler(program_lines,screen,editor_state)
    DrawStatusLine(screen,editor_state)
    ReturnCursor(INPUT_X+editor_state.input_ptr,LINES_START_Y+editor_state.current_line,screen)
    EndDrawing(screen)

#Function called to begin program after setup on Linux
#Not used in JavaScript version, but difficult to abstract into linux.py
def LinuxAssembler(screen,file_input):
    global editor_state
    
    #Initialize colors pairs - must happen here after curses initiated
    InitColors()
    
    #Initialize editor size
    rows,cols=screen.getmaxyx()
    editor_state.col_count=cols
    editor_state.row_count=rows

    #Draw assembler first time
    DrawAll(screen,editor_state)

    while(True):

       #Process keys
        if file_input:
            #If file input left, load as key
            key=file_input[0]
            if key==chr(10):
                key="KEY_ENTER"
            file_input=file_input[1:]
        else:
            key=KeyInput(screen)
            if key!="TIMEOUT":
                editor_state.last_mode="key"
                editor_state.redraw_text=True
            if key=="KEY_RESIZE":
                rows,cols=screen.getmaxyx()
                editor_state.col_count=cols
                editor_state.row_count=rows

        #Process key, resimulate, and update screen
        AssemblerStep(editor_state,key)

        #Redraw screen if necessary
        if editor_state.redraw_text and not file_input:
            DrawAll(screen,editor_state)

#Enter interactive assembler on Linux
#Ignored in JavaScript version since key handler and timer based 
BeginAssembler("linux",LinuxAssembler)

