from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class This(Lexeme):
    def __init__(self,strLexeme):
        super(This,self).__init__(strLexeme)
    matcher = CompareMatcher("sen")