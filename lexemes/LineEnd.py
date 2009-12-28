from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class LineEnd(Lexeme):
    def __init__(self,strLexeme):
        super(LineEnd,self).__init__(strLexeme)
    matcher = CompareMatcher('\n')