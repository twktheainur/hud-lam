import os
import imp
import sys
sys.path = ['..'] + sys.path
from Parser import Parser
class ParserTest:
    def __init__(self):
        for file in os.listdir('.'):
            fstart = file[0:4]
            fend = file[4:len(file)-3]
            if fstart=='Test' and file[len(file)-3:len(file)]=='.py':
                print "Creating new parser for:",fend
                print fstart+fend
                fp, pathname, description = imp.find_module(fstart+fend)
                module = imp.load_module(fstart+fend, fp, pathname, description)
                testerctr = module.__dict__[fstart+fend]
                tester = testerctr()
                for s in tester.test_strings:
                    p = Parser(s,True)
                    print dir(p)
                    tester.run(s,p)

if __name__=="__main__":
    t = ParserTest()