from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class BlockStart(Lexeme):
    string = ":"
    def __init__(self,strLexeme):
        super(BlockStart,self).__init__(strLexeme)
    matcher = CompareMatcher(":")