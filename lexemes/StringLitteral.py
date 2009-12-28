from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class StringLitteral(Lexeme):
    def __init__(self,strLexeme):
        super(StringLitteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("(\"|\')([^\"]|[^\'])*(\"|\')")