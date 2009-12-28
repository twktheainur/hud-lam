from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Affectation(Lexeme):
    def __init__(self,strLexeme):
        super(Affectation,self).__init__(strLexeme)
    matcher = CompareMatcher("=")