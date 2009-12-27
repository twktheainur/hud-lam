from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class For(Symbol):
    def __init__(self,strSymbol):
        super(For,self).__init__(strSymbol)
    matcher = CompareMatcher("an")