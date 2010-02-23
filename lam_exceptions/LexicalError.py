from HudLamError import *
class LexicalError(HudLamError):
    def __init__(self,line,column,expected,found):
        super(LexicalError,self).__init__("Lexical",line,column,expected,found)