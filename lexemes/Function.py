from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Function(Lexeme):
    def __init__(self,strLexeme):
        super(Function,self).__init__(strLexeme)
    matcher = CompareMatcher("tass")