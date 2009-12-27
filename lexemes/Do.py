from Symbol import Symbol
from matcher.CompareMatcher import CompareMatcher
class Do(Symbol):
    def __init__(self,strSymbol):
        super(Do,self).__init__(strSymbol)
    matcher = CompareMatcher("agor")