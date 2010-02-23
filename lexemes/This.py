from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class This(Lexeme):
    string = "sen"
    def __init__(self,str):
        super(This,self).__init__(str)
    matcher = CompareMatcher("sen")