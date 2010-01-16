
class CharacterState(object):
    def __init__(self,reader, *args):
        self.reader=reader
        if len(args)==0:
            self.file_index = 0
            self.line=0
            self.column=0
            self.current_character='';
        elif len(args)==1:
            char_state = args[0]
            self.line=char_state.line
            self.column=char_state.column
            self.file_index = char_state.file_index
            self.current_character = char_state.current_character

    def next(self,c):
        self.current_character=c
        if c=='\n':
            self.column=0
            self.line+=1
        self.column +=1
        self.file_index +=1

    def revert(self):
        self.reader.state = self
        self.file_index-=1
        self.reader.source_file.seek(self.file_index)
        self.reader.next()