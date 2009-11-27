
import re;

class RegExpMatcher(SymbolMatcher):
    def __init__(self,matcher,matchee):
        super(RegExpMatcher,self).__init__(re.compile(matcher),matchee)

    def match(self):
        return self.matcher.match()!=None