#!/usr/bin/env python3

#Text colors for curses
COLOR_NAMES={
    "blue":     0xFF,       #curses.COLOR_BLUE,
    "green":    0xFF00,     #curses.COLOR_GREEN,
    "cyan":     0xFFFF,     #curses.COLOR_CYAN,
    "yellow":   0xFFFF00,   #curses.COLOR_YELLOW,
    "red":      0xFF0000,   #curses.COLOR_RED,
    "magenta":  0xFF00FF,   #curses.COLOR_MAGENTA,
    "white":    0xFFFFFF,   #curses.COLOR_WHITE,
    "black":    0,          #curses.COLOR_BLACK
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
    )

#Maps color types (op, dir, alpha, etc) in TEXT_COLORS to curses color codes in COLOR_NAMES
#Filled in programmatically in InteractiveAssembler function below since needs initialized curses 
COLOR_DICT={}

#Screen output functions
#=======================
def InitColors():
    for i,color in enumerate(TEXT_COLORS):
        #curses.init_pair(i+1,COLOR_NAMES[color[1][0]],COLOR_NAMES[color[1][1]])
        #COLOR_DICT[color[0]]=curses.color_pair(i+1)
        pass
    #COLOR_DICT["none"]=curses.color_pair(0)

def ClearScreen(screen):
    jc.clearScreen()
    return

def DrawText(draw_x,draw_y,text,screen,color="none"):
    #screen.addstr(draw_y,draw_x,text,COLOR_DICT[color])
    jc.drawString(draw_x,draw_y,text)
    return draw_x+len(text)

#Place cursor on input line
def ReturnCursor(x,y,screen):
    #screen.move(y,x)
    return

def EndDrawing(screen):
    jc.drawScreen()
    return

#Key input
#=========

#Shows key names and values - debug only
def GetKeyNames(screen):
    #screen.addstr(1,1,"Key: ")
    #while(True):
    #    key=screen.getkey()
    #    screen.clear()
    #    screen.addstr(1,1,"Key: "+key+"("+str(len(key))+")"+" - "+str(ord(key)) if len(key)==1 else "")
    #    screen.refresh()
    return

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

#File input - none for JavaScript version
#========================================
def FileInput():
    return ""

#Exit - abstract here since JavaScript version can't exit
#========================================================
def ExitProgram():
    return

#Main assembler function
#=======================
#Called by Linux version - ignore
def BeginAssembler(dummy1,dummy2):
    return

