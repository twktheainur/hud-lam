from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Do(Lexeme):
    def __init__(self,strLexeme):
        super(Do,self).__init__(strLexeme)
    matcher = CompareMatcher("agor")