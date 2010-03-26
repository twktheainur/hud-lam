from ParserTester import *
class TestTryStatement(ParserTester):
    def __init__(self):
        ParserTester.__init__(self,
        ['band: glamor "a" raeda: glamor "lol" meth']
        )

    def test(self,n,string,result):
        ParserTester.test(self,string,result)
        if n==0 and result!="Ok":
            self.failure(result)
        else:
            self.success()

