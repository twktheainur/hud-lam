from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Parent(Lexeme):
    string = "adar"
    def __init__(self,strLexeme):
        super(Parent,self).__init__(strLexeme)
    matcher = CompareMatcher("adar")