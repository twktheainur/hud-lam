from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Call(Lexeme):
    def __init__(self,strLexeme):
        super(Call,self).__init__(strLexeme)
    matcher = CompareMatcher("can")