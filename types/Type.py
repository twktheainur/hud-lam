class Type(object):
    def __init__(self):
        self.value = None
        
    def __eq__(self,other):
        return self.type()==other.type and self.value==other.value

    def is_set(self):
        return self.value!=None

    def type(self):
        return self.__class__

    def type_name(self):
        return "<none>"