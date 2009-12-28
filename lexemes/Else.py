from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Else(Lexeme):
    def __init__(self,strLexeme):
        super(Else,self).__init__(strLexeme)
    matcher = CompareMatcher("minei")