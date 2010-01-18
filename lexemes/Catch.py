from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Catch(Lexeme):
    def __init__(self,strLexeme):
        super(Catch,self).__init__(strLexeme)
    matcher = CompareMatcher("raeda")