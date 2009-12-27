from Symbol import Symbol
from matcher.ComareMatcher import CompareMatcher
class Parent(Symbol):
    def __init__(self,strSymbol):
        super(Parent,self).__init__(strSymbol)
    matcher = CompareMatcher("adar")