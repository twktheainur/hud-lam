# To change this template, choose Tools | Templates
# and open the template in the editor.


class Lexeme(object):
    
    def __init__(self, strSymbol):
        self.string = strSymbol
    # This needs to be redefined in sub classes
    matcher = None

    '''
        Returns an instance of the subclass from which it is called if strSymbol
        matches the matcherString of the given subclass
    '''
    @classmethod
    def match(cls,strSymbol):
        ret = None
        if cls.matcher.match(strSymbol):
            ret = cls(strSymbol)
        return ret

    def __eq__(self,other):
        return type(self)==type(other)

