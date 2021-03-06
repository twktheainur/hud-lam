from SourceFile import *
from CharacterState import CharacterState

class CharacterReader(object):

    def __init__(self,file,str_in=False):
        self.source_file = None
        self.state = CharacterState(self)
        self.source_file = SourceFile(file,str_in)
        self.source_file.open("rb")
        self.next()

    def next(self):
        if self.source_file.peek(1) !="":
            self.state.next(self.source_file.read(1))


