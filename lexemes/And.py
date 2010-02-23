from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class And(Lexeme):
    string = "a"
    def __init__(self,str):
        super(And,self).__init__(str)
    matcher = CompareMatcher("a")