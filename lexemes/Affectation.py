from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class Affectation(Lexeme):
    string = "="
    def __init__(self,str):
        super(Affectation,self).__init__(str)
    matcher = CompareMatcher("=")