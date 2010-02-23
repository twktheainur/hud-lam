from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Separator(Lexeme):
    string = ","
    def __init__(self,strLexeme):
        super(Separator,self).__init__(strLexeme)
    matcher = CompareMatcher(",")