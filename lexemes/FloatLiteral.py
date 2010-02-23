from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class FloatLiteral(Lexeme):
    string = "<float>"
    def __init__(self,strLexeme):
        super(FloatLiteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("[0-9]+\.[0-9]+$")