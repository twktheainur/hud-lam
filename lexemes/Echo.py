from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Echo(Lexeme):
    def __init__(self,strLexeme):
        super(Echo,self).__init__(strLexeme)
    matcher = CompareMatcher("glamor")