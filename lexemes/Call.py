from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Call(Lexeme):
    string = "can"
    def __init__(self,str):
        super(Call,self).__init__(str)
    matcher = CompareMatcher("can")