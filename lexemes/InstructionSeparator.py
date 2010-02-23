from Lexeme import Lexeme
from matcher.CompareMatcher import CompareMatcher
class InstructionSeparator(Lexeme):
    string = ";"
    def __init__(self,strLexeme):
        super(InstructionSeparator,self).__init__(strLexeme)
    matcher = CompareMatcher(";")