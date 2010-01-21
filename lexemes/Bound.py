from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Bound(Lexeme):
    def __init__(self,strLexeme):
        super(Bound,self).__init__(strLexeme)
    matcher = CompareMatcher("gleina")