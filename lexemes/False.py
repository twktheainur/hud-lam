from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class False(Lexeme):
    string = "neitha"
    def __init__(self,strLexeme):
        super(False,self).__init__(strLexeme)
    matcher = CompareMatcher("neitha")