from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class None(Symbol):
    def __init__(self,strSymbol):
        super(None,self).__init__(strSymbol)
    matcher = CompareMatcher("cofn")