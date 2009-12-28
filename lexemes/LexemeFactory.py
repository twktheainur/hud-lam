from Lexeme import Lexeme
from lexemes import *
import sys
import imp
class LexemeFactory(object):
    def __init__(self):
        self.classes=list()
        for lexeme in matchLexemes:            
            module =__import__(lexeme,globals(),locals(),[lexeme])
            self.classes.append(getattr(module,lexeme))
            
    def create_lexeme(self,str):
        lexeme_obj = None
        for lexclass in self.classes:
            lexeme_obj = lexclass.match(str)
            if(lexeme_obj!=None):
                break 
            lexeme_obj=None
        return lexeme_obj