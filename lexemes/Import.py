from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Import(Lexeme):
    string = "baur"
    def __init__(self,strLexeme):
        super(Import,self).__init__(strLexeme)
    matcher = CompareMatcher("baur")