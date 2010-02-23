from HudLamError import *
class SyntacticError(HudLamError):
    def __init__(self,line,column,expected,found):
        super(SyntacticError,self).__init__("Syntactic ",line,column,expected,found)