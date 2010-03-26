class ParserTester(object):
    def __init__(self,test_strings):
        self.test_strings = test_strings

    def test(self,string,result):
        print "Testing", self.__class__.__name__[4:]
        print "with string: ",string

    def run(self,str,parser):
        name="_Parser_"
        for c in self.__class__.__name__[4:]:
            if c.isupper():
                name+="_"+c.lower()
            else:
                name+=c
        method = getattr(parser,name)
        res="Ok"
#        try:
        method()
#        except Exception as e:
#            print e
#            res="Ex"+e.__class__.__name__
        self.test(self.test_strings.index(str),str,res)
        
    def success(self):
        print "Test [OK]"

    def failure(self,result):
        print "Test for ",self.__class__.__name__[4:]," failed with result: "+result
        print "Parser testing FAILED!"
        exit()