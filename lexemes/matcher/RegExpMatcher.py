
import re;
from LexemeMatcher import LexemeMatcher

class RegExpMatcher(LexemeMatcher):
    def __init__(self,matcher):
        super(RegExpMatcher,self).__init__(re.compile(matcher))

    def match(self,str):
        return self.matcher.match(str) is not None