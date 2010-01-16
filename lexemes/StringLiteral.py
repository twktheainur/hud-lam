from Lexeme import Lexeme
from matcher.RegExpMatcher import RegExpMatcher
class StringLiteral(Lexeme):
    def __init__(self,strLexeme):
        super(StringLiteral,self).__init__(strLexeme)
    matcher = RegExpMatcher("(\"|\')([^\"]|[^\'])*(\"|\')")