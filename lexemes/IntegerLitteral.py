from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class IntegerLitteral(Lexeme):
    def __init__(self,strLexeme):
        super(IntegerLitteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("[0-9]+$")