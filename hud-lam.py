import compiler
#!/usr/bin/env python

from Lexer import *
from lexemes import *
from lexemes.Enter import *
from CharacterReader import *
from Parser import *
from Compiler import *
if __name__ == "__main__":
    parser = Parser("testlex2.lam")
    compiler = Compiler(parser)
    code = compiler.compile()
    exec code
