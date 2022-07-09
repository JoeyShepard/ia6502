#!/usr/bin/env python3

#*****************************************************
#* I/O functions for JavaScript port with Brython    * 
#* (see linux.py for curses-based Linux I/O version) *
#*****************************************************


#Import statement used by Brython
from browser import bind, console, document, timer, window

#Constants
TERM_COLS=98        #Terminal column count
TERM_ROWS=32        #Terminal row count
CURSOR_FG="black"
CURSOR_BG="green"
KB_TIMEOUT=500      #Keyboard timeout (ms)

#Text colors for Brython (curses in Linux version)
COLOR_NAMES={
    "blue":     0x4080FF,   #Light blue looks better on black than pure blue
    "green":    0xFF00,
    "cyan":     0xFFFF,
    "yellow":   0xFFFF00,
    "red":      0xFF0000,
    "magenta":  0xFF00FF,
    "white":    0xFFFFFF,
    "black":    0
    }

#Colors for different types of text - foreground, background
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
    ("scroll arrows",       ("black","white")),     #Scroll arrows at top and bottom of screen
    )

#Maps color types (op, dir, alpha, etc) in TEXT_COLORS to hex values in COLOR_NAMES
#Filled in below in InitColors like Linux version with curses
COLOR_DICT={}

#Screen output functions
#=======================

#Initialize color pairs in COLOR_DICT used for terminal output in browser
def InitColors():
    for color in TEXT_COLORS:
        COLOR_DICT[color[0]]=(COLOR_NAMES[color[1][0]],COLOR_NAMES[color[1][1]])
    COLOR_DICT["none"]=(COLOR_NAMES["white"],COLOR_NAMES["black"])

#Clear terminal in browser
def ClearScreen(screen):
    window.clearScreen()

#Draw colored text in terminal in browser
def DrawText(draw_x,draw_y,text,screen,color="none"):
    if color not in COLOR_DICT:
        color="none"
    fgcolor=COLOR_DICT[color][0]
    bgcolor=COLOR_DICT[color][1]
    window.drawString(draw_x,draw_y,text,fgcolor,bgcolor)
    return draw_x+len(text)

#Place green cursor on input line
def ReturnCursor(x,y,screen):
    screen_char=window.getScreenChar(x,y)
    window.drawString(x,y,screen_char,COLOR_NAMES[CURSOR_FG],COLOR_NAMES[CURSOR_BG])

#Render text to terminal in browser after all changes have been made
def EndDrawing(screen):
    window.drawScreen()

#Key input
#=========
#Translate key names from JavaScript to curses
def KeyInput(key):
    if key=="Backspace":
        return "KEY_BACKSPACE"
    elif key=="ArrowLeft":
        return "KEY_LEFT"
    elif key=="ArrowRight":
        return "KEY_RIGHT"
    elif key=="ArrowUp":
        return "KEY_UP"
    elif key=="ArrowDown":
        return "KEY_DOWN"
    elif key=="Home":
        return "KEY_HOME"
    elif key=="End":
        return "KEY_END"
    elif key=="Delete":
        return "KEY_DC"
    elif key=="Enter":
        return "KEY_ENTER"
    elif len(key)==1 and key.isalnum():
        return key
    elif key in " ~`!@#$%^&*()_+-={}[];':<>,.?/|\"\\":
        return key
    else:
        return "(none)"

#Exit - abstract here since JavaScript version can't exit
#========================================================
def ExitProgram():
    return

#Main assembler function
#=======================
def BeginAssembler(version,assembler_func=None): 
    #If called from main ia6502.py with version "linux", ignore.
    #JavaScript version started in HTML file with version set to "brython".
    if version=="linux":
        return
    elif version=="brython":
        global timer_id

        #Short code example loaded at startup
        CODE_EXAMPLE="lda #33\nrol\n"

        #Initialization of js-curses. All JS functions loaded in window object.
        window.screenSetup(TERM_COLS,TERM_ROWS)

        #Initialize assembler color list
        InitColors()

        #Initialize editor size
        editor_state.col_count=TERM_COLS
        editor_state.row_count=TERM_ROWS

        #Install key handler defined below
        document.bind("keydown",key_handler)
        
        #Load  example defined above
        for key in CODE_EXAMPLE:
            editor_state.last_mode="key"
            editor_state.redraw_text=False
            key="KEY_ENTER" if key=="\n" else key
            AssemblerStep(editor_state,key)

        #Draw assembler first time
        AssemblerStep(editor_state,"TIMEOUT")
        DrawAll(0,editor_state)

        console.log("i6502 loaded!")
    else:
        console.log("Unknown version: "+version)
        console.log("ia6502 failed to load!")

#Key handler
def key_handler(event):
    global timer_id
    global KB_TIMEOUT
    
    #Pass keys with ctrl pressed through to browser instead of handling here 
    if event.ctrlKey:
        return

    #Process key since ctrl not pressed
    if timer_id!=None:
        timer.clear_timeout(timer_id)
        timer_id=None
    key=KeyInput(event.key)
    if key!="(none)":
        #If useful key came from KeyInput, don't perform it's browser behavior
        event.preventDefault()
    editor_state.last_mode="key"
    editor_state.redraw_text=True
    AssemblerStep(editor_state,key)
    if (editor_state.redraw_text):
        DrawAll(0,editor_state)
    event.stopPropagation()
    timer_id=timer.set_timeout(timer_handler,KB_TIMEOUT)

#Timer handler
def timer_handler():
    global timer_id
    timer_id=None
    AssemblerStep(editor_state,"TIMEOUT")
    if (editor_state.redraw_text):
        DrawAll(0,editor_state)


