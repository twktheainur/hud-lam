from LexemeMatcher import LexemeMatcher

class CompareMatcher(LexemeMatcher):
    def __init__(self,matcher):
        super(CompareMatcher,self).__init__(matcher);

    def match(self,str):
            return self.matcher==str