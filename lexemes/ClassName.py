from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
from Name import Name
class ClassName(Name):
    def __init__(self,symbolStr):
        super(ClassName,self).__init__(symbolStr)

    matcher = RegExpMatcher("[A-Z][\w]*")