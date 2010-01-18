import parser
#!/usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

from Lexer import *
from lexemes import *
from lexemes.Enter import *
from CharacterReader import *
from Parser import *
if __name__ == "__main__":
    parser = Parser("testlex.lam")
    parser.parse()
#    l=CharacterReader("testlex.lam")
#    lex = l.state.current_character
#    while lex!="":
#        lex = l.state.current_character
#        print lex,
#        l.next()