

class SourceFile(object):

    def __init__(self,filename):
        self.filename=filename
        self.file = None

    def open(self,mode):
        self.file = open(self.filename,mode)
        if not self.file:
            raise Exception("No Such File:"+self.filename)

    def peek(self,n):
        if n==None:
            n=1;
        currentPosition = self.file.tell()
        self.file.seek(n)
        character = self.file.read(1);
        self.file.seek(currentPosition,0)
        return character

    def read(self,n):
        return self.file.read(n)

    def seek(self,index):
        return self.file.seek(index)

    def tell(self):
        return self.file.tell()