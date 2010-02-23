class HudLamError(Exception):
    def __init__(self,type,line,column,expected,found):
        super(HudLamError,self).__init__(type +"error at "+
                                               str(line)+":"+
                                               str(column)+" found: "+found+
                                               " expected: "+expected)