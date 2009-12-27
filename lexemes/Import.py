from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class Import(Symbol):
    def __init__(self,strSymbol):
        super(Import,self).__init__(strSymbol)
    matcher = CompareMatcher("baur")