from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Or(Lexeme):
    string = "egor"
    def __init__(self,strLexeme):
        super(Or,self).__init__(strLexeme)
    matcher = CompareMatcher("egor")