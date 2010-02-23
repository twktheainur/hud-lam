from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class Operator(Lexeme):
    string = "<operator>"
    def __init__(self,strLexeme):
        super(Operator,self).__init__(strLexeme)
    matcher = RegExpMatcher(">|>=|<|<=|\+|-|!=|==|\*|/|%")