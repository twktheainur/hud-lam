from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Access(Lexeme):
    def __init__(self,strLexeme):
        super(Access,self).__init__(strLexeme)
    matcher = CompareMatcher(".")