from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class Name(Lexeme):
    def __init__(self,symbolStr):
        super(Name,self).__init__(symbolStr)

    matcher = RegExpMatcher("[A-Za-z_][\w]*")