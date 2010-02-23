from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class In(Lexeme):
    string = "min"
    def __init__(self,strLexeme):
        super(In,self).__init__(strLexeme)
    matcher = CompareMatcher("min")