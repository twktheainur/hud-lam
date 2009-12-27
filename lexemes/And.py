from Symbol import Symbol
from matcher.CompareMatcher import CompareMatcher
class And(Symbol):
    def __init__(self,strSymbol):
        super(And,self).__init__(strSymbol)
    matcher = CompareMatcher("a")