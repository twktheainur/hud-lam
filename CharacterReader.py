from SourceFile import *
class CharacterReader:

    def __init__(self,file):
        self.line=1;
        self.column=0;
        self.currentCharacter='';
        self.sourceFile = None
        try:
            self.sourceFile = SourceFile(file)
            self.sourceFile.open("r")
        except:
            print "Cannot open source file: "+file
            return
        self.next()

    def next(self):
        if self.sourceFile.peek(1) !="":
            if self.currentCharacter=='\n':
                self.column=0;
                self.line+=1;
            self.currentCharacter = self.sourceFile.read(1);
            self.column+=1;


