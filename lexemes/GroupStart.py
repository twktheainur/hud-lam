from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class GroupStart(Lexeme):
    string = "("
    def __init__(self,strLexeme):
        super(GroupStart,self).__init__(strLexeme)
    matcher = CompareMatcher("(")