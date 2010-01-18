from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Try(Lexeme):
    def __init__(self,strLexeme):
        super(Try,self).__init__(strLexeme)
    matcher = CompareMatcher("can")