from Symbol import Symbol
from matcher.RegExpMatcher import RegExpMatcher
class VariableName(Symbol):
    def __init__(self,symbolStr):
        super(VariableName,self).__init__(symbolStr)

    matcher = RegExpMatcher("[A-Za-z_][\w]*")