#!/usr/bin/env python3

from sys import path
from os.path import expanduser
path.append(expanduser("~/python/"))

#from color import *
#from sys import exit

def bar():
    print("Bar!")

from lib import *

foo()
