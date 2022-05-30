#!/bin/bash

#Combine program-generated emulator jump table with main program while
#jump table is being worked out. Will move to main program permanently
#after jump table is finalized.

echo "#!/usr/bin/env python3" > combined.py
cat emu_generator/emu_ops.py >> combined.py
cat ia6502.py >> combined.py
./combined.py test.asm
