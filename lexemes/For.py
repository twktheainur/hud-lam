from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class For(Lexeme):
    string = "an"
    def __init__(self,strLexeme):
        super(For,self).__init__(strLexeme)
    matcher = CompareMatcher("an")