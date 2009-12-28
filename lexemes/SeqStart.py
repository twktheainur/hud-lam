from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class SeqStart(Lexeme):
    def __init__(self,strLexeme):
        super(SeqStart,self).__init__(strLexeme)
    matcher = CompareMatcher("[")