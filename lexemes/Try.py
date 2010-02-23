from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Try(Lexeme):
    string="band"
    def __init__(self,str):
        super(Try,self).__init__(str)
    matcher = CompareMatcher("band")