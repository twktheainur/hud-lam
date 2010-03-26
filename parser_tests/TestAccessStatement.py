from ParserTester import *
class TestAccessStatement(ParserTester):
    def __init__(self):
        ParserTester.__init__(self,
        ["c.d.e.f.d"]
        )

    def test(self,n,string,result):
        ParserTester.test(self,string,result)
        if n==0 and result!="Ok":
            self.failure(result)
        else:
            self.success()

