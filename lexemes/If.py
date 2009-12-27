from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class If(Symbol):
    def __init__(self,strSymbol):
        super(If,self).__init__(strSymbol)
    matcher = CompareMatcher("gowest")