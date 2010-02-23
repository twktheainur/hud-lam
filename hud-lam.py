#!/usr/bin/env python

from Lexer import *
from lexemes import *
from lexemes.Enter import *
from CharacterReader import *
from Parser import *
if __name__ == "__main__":
    parser = Parser("testlex2.lam")
    print parser.generate_py_module()
#parser._Parser__access_statement(False)
#    parser.parse()
#    l=CharacterReader("testlex.lam")
#    lex = l.state.current_character
#    while lex!="":
#        lex = l.state.current_character
#        print lex,
#        l.next()