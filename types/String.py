class String(Type)
    def __init__(self,value):
        self.value=value
        if self.value[0]=='"':
            self.value = strip(self.value,'"')
        elif self.value[0] == "'":\
            self.value = strip(self.value,"'")

    def type_name(self):
        return "<string>"
        
