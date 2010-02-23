from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Class(Lexeme):
    string = "gond"
    def __init__(self,str):
        super(Class,self).__init__(str)
    matcher = CompareMatcher("gond")