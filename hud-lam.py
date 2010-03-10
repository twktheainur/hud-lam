#!/usr/bin/env python

from Lexer import *
from lexemes import *
from lexemes.Enter import *
from CharacterReader import *
from Parser import *
import ast
if __name__ == "__main__":
    parser = Parser("testlex2.lam")
    exec compile(ast.fix_missing_locations(parser.generate_py_ast()),"testlex2","exec")
#parser._Parser__access_statement(False)
#    parser.parse()
#    l=CharacterReader("testlex.lam")
#    lex = l.state.current_character
#    while lex!="":
#        lex = l.state.current_character
#        print lex,
#        l.next()