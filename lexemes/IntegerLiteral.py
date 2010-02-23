from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class IntegerLiteral(Lexeme):
    string = "<integer>"
    def __init__(self,strLexeme):
        super(IntegerLiteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("[0-9]+$")