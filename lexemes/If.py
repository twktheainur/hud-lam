from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class If(Lexeme):
    string = "gowest"
    def __init__(self,strLexeme):
        super(If,self).__init__(strLexeme)
    matcher = CompareMatcher("gowest")