from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class BlockEnd(Lexeme):
    def __init__(self,strLexeme):
        super(BlockEnd,self).__init__(strLexeme)
    matcher = CompareMatcher("meth")