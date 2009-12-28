from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class And(Lexeme):
    def __init__(self,strLexeme):
        super(And,self).__init__(strLexeme)
    matcher = CompareMatcher("a")