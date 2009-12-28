from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class FloatLitteral(Lexeme):
    def __init__(self,strLexeme):
        super(FloatLitteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("[0-9]+\.[0-9]+$")