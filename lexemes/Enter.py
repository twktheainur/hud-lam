from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Enter(Lexeme):
    def __init__(self,strLexeme):
        super(Enter,self).__init__(strLexeme)
    matcher = CompareMatcher("minna")