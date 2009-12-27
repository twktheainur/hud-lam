from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class In(Symbol):
    def __init__(self,strSymbol):
        super(In,self).__init__(strSymbol)
    matcher = CompareMatcher("min")