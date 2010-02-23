from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher

class Access(Lexeme):
    string = "."
    def __init__(self,str):
        super(Access,self).__init__(str)
    matcher = CompareMatcher(".")