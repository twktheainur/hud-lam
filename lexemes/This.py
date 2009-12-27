from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class This(Symbol):
    def __init__(self,strSymbol):
        super(This,self).__init__(strSymbol)
    matcher = CompareMatcher("sen")