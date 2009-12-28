from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class True(Lexeme):
    def __init__(self,strLexeme):
        super(True,self).__init__(strLexeme)
    matcher = CompareMatcher("thand")