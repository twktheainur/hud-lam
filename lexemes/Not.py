from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Not(Lexeme):
    def __init__(self,strLexeme):
        super(Not,self).__init__(strLexeme)
    matcher = CompareMatcher("al")