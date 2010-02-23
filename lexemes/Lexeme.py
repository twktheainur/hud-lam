# To change this template, choose Tools | Templates
# and open the template in the editor.


class Lexeme(object):
    
    def __init__(self,strLexeme):
        self.string = strLexeme
        
    # This needs to be redefined in sub classes
    matcher = None

    '''
        Returns an instance of the subclass from which it is called if strLexeme
        matches the matcherString of the given subclass
    '''
    @classmethod
    def match(cls,strLexeme):
        ret = None
        if cls.matcher.match(strLexeme):
            ret = cls(strLexeme)
        return ret

    def __eq__(self,other):
        return self.__class__==other

