from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher

class EOF(Lexeme):
    string = "<EOF>"
    def __init__(self,symbolStr):
        super(EOF,self).__init__(symbolStr)
        
    matcher = CompareMatcher('')