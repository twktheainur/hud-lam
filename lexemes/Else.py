from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class Else(Symbol):
    def __init__(self,strSymbol):
        super(Else,self).__init__(strSymbol)
    matcher = CompareMatcher("minei")