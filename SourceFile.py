

class SourceFile(file):

    def __init__(self,filename):
        self.filename=filename

    def open(self,mode):
        self = open(self.filename,mode)

    def peek(self,n):
        if n==None:
            n=1;
        currentPosition = self.tell()
        self.seek(n)
        character = self.read(1);
        self.seek(currentPosition,0)
        return character
