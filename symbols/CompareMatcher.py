

class CompareMatcher(SymbolMatcher):
    def __init__(self,matcher,matchee):
        super(CompareMatcher,self).__init__(matcher, matchee);

    def match(self):
            return matcher==matchee