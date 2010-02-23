from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Echo(Lexeme):
    string = "glamor"
    def __init__(self,strLexeme):
        super(Echo,self).__init__(strLexeme)
    matcher = CompareMatcher("glamor")