from Symbol import Symbol
from matcher.CompareMatcher import CompareMatcher
class Class(Symbol):
    def __init__(self,strSymbol):
        super(Class,self).__init__(strSymbol)
    matcher = CompareMatcher("gond")