from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Input(Lexeme):
    string = "toltha"
    def __init__(self,strLexeme):
        super(Input,self).__init__(strLexeme)
    matcher = CompareMatcher("toltha")