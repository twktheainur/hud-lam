from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class Or(Symbol):
    def __init__(self,strSymbol):
        super(Or,self).__init__(strSymbol)
    matcher = CompareMatcher("egor")