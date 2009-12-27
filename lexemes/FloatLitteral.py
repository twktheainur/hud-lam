from Symbol import Symbol
from matcher.RegExpMatcher import RegExpMatcher
class FloatLitteral(Symbol):
    def __init__(self,strSymbol):
        super(FloatLitteral,self).__init__(strSymbol)
    matcher = RegExpMatcher("[0-9]+\.[0-9]+$")