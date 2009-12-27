from Lexeme import Lexeme
class LexemeFactory(object):
    def __init__(self):
        pass
    @classmethod
    def create_lexeme(cls,str):
        return Lexeme(str)