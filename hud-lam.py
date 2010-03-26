import compiler
import sys
#!/usr/bin/env python

from Lexer import *
from lexemes import *
from lexemes.Enter import *
from CharacterReader import *
from Parser import *
from Compiler import *
if __name__ == "__main__":
    argc = len(sys.argv)-1
    if argc<1:
        print "Syntax: hud-lam.py module_name"
        sys.exit(1);
    name = sys.argv[1]
    parser = Parser(name+".lam")
    compiler = Compiler(parser)
    code = compiler.compile()
    exec code
