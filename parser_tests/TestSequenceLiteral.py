from ParserTester import *
class TestSequenceLiteral(ParserTester):
    def __init__(self):
        super(TestSequenceLiteral,self).__init__(
        ["[1,2,3,4,5,6]","[1::2]"]
        )
    
    def test(self,n,string,result):
        super(TestSequenceLiteral,self).test(string,result)
        if n==0 and result!="Ok":
            self.failure(result)
        elif n==1 and result!="Ok":
            self.failure(result)
        else:
            self.success()

