from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Class(Lexeme):
    def __init__(self,strLexeme):
        super(Class,self).__init__(strLexeme)
    matcher = CompareMatcher("gond")