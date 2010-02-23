from SourceFile import *
from CharacterState import CharacterState

class CharacterReader(object):

    def __init__(self,file):
        self.source_file = None
        self.state = CharacterState(self)
        try:
            self.source_file = SourceFile(file)
            self.source_file.open("rb")
        except Exception as ex:
            print "Cannot open source file: "+file
            raise ex
        self.next()

    def next(self):
        if self.source_file.peek(1) !="":
            self.state.next(self.source_file.read(1))


