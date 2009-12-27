from Symbol import Symbol
from matcher.CompareMatcher import CompareMatcher

class EOF(Symbol):
    def __init__(self,symbolStr):
        super(EOF,self).__init__(symbolStr)
        
    matcher = CompareMatcher('')