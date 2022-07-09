#!/usr/bin/env python3

#************************************************
#* I/O functions for curses-based Linux version *
#* (see brython.py for JavaScript I/O version)  *
#************************************************


import curses
from ia6502.classes import EditorStateClass

#Text colors for curses
COLOR_NAMES={
    "blue":     curses.COLOR_BLUE,
    "green":    curses.COLOR_GREEN,
    "cyan":     curses.COLOR_CYAN,
    "yellow":   curses.COLOR_YELLOW,
    "red":      curses.COLOR_RED,
    "magenta":  curses.COLOR_MAGENTA,
    "white":    curses.COLOR_WHITE,
    "black":    curses.COLOR_BLACK
    }

#Colors for different types of text
TEXT_COLORS=(
    ("op",                  ("blue","black")),      #Instruction
    ("dir",                 ("magenta","black")),   #Assembly directive
    ("alpha",               ("white","black")),     #Symbol, ie defined with .SET
    ("label",               ("green","black")),
    ("label colon",         ("white","black")),
    ("number",              ("magenta","black")),
    ("character",           ("green","black")),
    ("string",              ("green","black")),
    ("reg",                 ("blue","black")),      #X or Y register
    ("comment",             ("cyan","black")),
    ("paren selected",      ("white","magenta")),   #Matching parenthesis when cursor on parenthesis
    ("symbol",              ("white","black")),     #Any symbol #,$,&,etc
    ("symbol unknown",      ("black","yellow")),    #Unknown alpha symbol like "foo"
    ("symbol error",        ("white","red")),       #Syntax error like LDA ) or LDA $$
    ("neutral",             ("white","black")),     #Symbol at end of line - not recognized but don't flag as unknown
    ("line current",        ("black","green")),     #Highlight address to show current line
    ("line unknown",        ("black","yellow")),    #Highlight address if contains unknown symbols
    ("line error",          ("white","red")),       #Highlight address if contains syntax error
    ("line breakpoint",     ("red","white")),       #Highlight address if contains breakpoint
    ("bytes unknown",       ("yellow","black")),    #Color of ?? in assembled bytes if value unknown
    ("bytes error",         ("red","black")),       #Color of "Not found" or "Range error" from byte generation
    ("reg unchanged",       ("white","black")),     #Unchanged register
    ("reg changed",         ("green","black")),     #Changed register
    ("reg unknown",         ("yellow","black")),    #Register with unknown value (loaded from uninitialized memory)
    ("flag unchanged",      ("white","black")),     #Unchanged processor flag
    ("flag unknown",        ("yellow","black")),    #Unknown processor flag (generated from value from unitialized memory)
    ("flag changed true",   ("green","black")),     #Changed processor flag that is true
    ("flag changed false",  ("green","black")),     #Changed processor flag that is false
    ("status run",          ("green","black")),     #Emulation status of line - has been run
    ("status rerun",        ("cyan","black")),      #Emulation status of line - has been run more than once
    ("status stopped",      ("black","green")),     #Emulation status of line - has been run and stopped here
    ("status line",         ("black","magenta")),   #Status line at bottom of screen
    )

#Maps color types (op, dir, alpha, etc) in TEXT_COLORS to curses color codes in COLOR_NAMES
#Filled in programmatically in InteractiveAssembler function below since needs initialized curses 
COLOR_DICT={}

#Screen output functions
#=======================

#Initalize curses color pairs in COLOR_DICT
#Needs own function like this since must happen after curses initialization
def InitColors():
    for i,color in enumerate(TEXT_COLORS):
        curses.init_pair(i+1,COLOR_NAMES[color[1][0]],COLOR_NAMES[color[1][1]])
        COLOR_DICT[color[0]]=curses.color_pair(i+1)
    COLOR_DICT["none"]=curses.color_pair(0)

#Clear curses terminal
def ClearScreen(screen):
    screen.clear()

#Draw colored text in curses terminal
def DrawText(draw_x,draw_y,text,screen,color="none"):
    screen.addstr(draw_y,draw_x,text,COLOR_DICT[color])
    return draw_x+len(text)

#Place green cursor on input line
def ReturnCursor(x,y,screen):
    screen.move(y,x)
 
#Render text to curses terminal after all changes have been made
def EndDrawing(screen):
    screen.refresh()

#Key input
#=========

#Shows key names and values - debug only
def GetKeyNames(screen):
    screen.addstr(1,1,"Key: ")
    while(True):
        key=screen.getkey()
        screen.clear()
        screen.addstr(1,1,"Key: "+key+"("+str(len(key))+")"+" - "+str(ord(key)) if len(key)==1 else "")
        screen.refresh()

#Key input with 500ms timeout and keyboard interrupt handling
def KeyInput(screen=None):
    try:
        #Half second timeout for key input
        curses.halfdelay(5)
        key=screen.getkey()
        if key==chr(10):
            key="KEY_ENTER"
    except KeyboardInterrupt:
        #User pressed Ctrl+C - exit program
        key="KB_INTERRUPT"
    except curses.error:
        #Timeout expired without keypress - reassemble and emulate
        #(Could be other error but curses doesn't have way to distinguish)
        key="TIMEOUT"
    return key

#File input from command line (optional)
#=======================================
def FileInput():
    from sys import argv, exit
    error_exit=False
    show_help=False
    file_input=""
    if len(argv)==1:
        #No arguments - proceed to interactive mode
        pass
    elif len(argv)==2:
        #One argument - filename to load or -h
        #Show help message and exit
        if argv[1]=="-h":
            show_help=True
            error_exit=True
        else:
            #One argument - treat as filename to load
            try:
                f=open(argv[1])
                file_input=f.read()
                f.close()
            except:
                #Error in loading file - error and exit
                print(f"Unable to open '{argv[1]}'") 
                show_help=False
                error_exit=True
    else:
        #More than one argument - error and exit
        print("Invalid arguments")
        show_help=True
        error_exit=True

    #If any errors processing command line or -h, show help message and exit
    if error_exit:
        if show_help:
            print("Usage: ia6502 [filename]")
        exit()

    return file_input

#Exit - abstract here since JavaScript version can't exit
#========================================================
def ExitProgram():
    from sys import exit
    exit()

#Main assembler function
#=======================
#Called by main script to initiate curses
#Need to pass function as argument to wrapper for curses cleanup
def BeginAssembler(version,assembler_func):
    if version!="linux":
        print(f'Error: expected version "linux" but found "{version}". Something is very, very wrong.')
    else:
        #Check for file input on command line and exit if error
        file_input=FileInput()
        
        #Pass assembler function to curses
        curses.wrapper(assembler_func,file_input)

