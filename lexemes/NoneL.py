from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class NoneL(Lexeme):
    string = "cofn"
    def __init__(self,strLexeme):
        super(NoneL,self).__init__(strLexeme)
    matcher = CompareMatcher("cofn")