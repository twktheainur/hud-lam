from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class True(Lexeme):
    string = "thand"
    def __init__(self,str):
        super(True,self).__init__(str)
    matcher = CompareMatcher("thand")