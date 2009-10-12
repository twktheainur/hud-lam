
class CharacterReader:

    def __init__(self,file):
        self.line=1;
        self.column=0;
        self.currentCharacter='';
        try:
            self.sourceFile = SourceFile(file)
            self.sourceFile.open("r")
        except:
            raise exception,"No Such File:"+self.sourceFile.filename
        self.next()

    def next(self):
        if self.sourceFile.peek() !="":
            if self.currentCharacter=='\n':
                self.column=0;
                self.line+=1;
            self.currentCharacter = self.sourceFile.read(1);
            self.column+=1;



