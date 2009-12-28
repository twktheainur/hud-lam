from Lexeme import Lexeme
from Name import Name
from matcher.RegExpMatcher import RegExpMatcher
class ModuleName(Name):
    def __init__(self,symbolStr):
        super(ModuleName,self).__init__(symbolStr)

    matcher = RegExpMatcher("[a-z_]*")