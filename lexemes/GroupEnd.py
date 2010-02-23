from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class GroupEnd(Lexeme):
    string = ")"
    def __init__(self,strLexeme):
        super(GroupEnd,self).__init__(strLexeme)
    matcher = CompareMatcher(")")