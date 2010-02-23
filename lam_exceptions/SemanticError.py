from HudLamError import *
class SemanticError(HudLamError):
    def __init__(self,line,column,expected,found):
        super(SemanticError,self).__init__("Semantic",line,column,expected,found)