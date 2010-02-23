from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class SeqEnd(Lexeme):
    string = "]"
    def __init__(self,strLexeme):
        super(SeqEnd,self).__init__(strLexeme)
    matcher = CompareMatcher("]")