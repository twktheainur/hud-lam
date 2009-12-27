#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

from Lexer import *


if __name__ == "__main__":
    lexer = Lexer("testlex.lam")
    str = lexer.next()

    while str.string!=u"":
        print str.string
        str = lexer.next()
        
