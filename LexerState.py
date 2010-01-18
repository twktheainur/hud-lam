from CharacterState import CharacterState
class LexerState(object):
    def __init__(self,lexer,*args):
        """Holds a revertable Lexer state"""
        self.lexer=lexer
        if len(args)==0:
            self.current_lexeme = None
            self.line=self.lexer.reader.state.line
            self.column=self.lexer.reader.state.column
            self.reader_state = self.lexer.reader.state
        elif len(args)==1:
            self.reader_state = CharacterState(self.lexer.reader,self.lexer.reader.state)
            lexer_state = args[0]
            self.line=lexer_state.line
            self.column=lexer_state.column
            self.current_lexeme = lexer_state.current_lexeme



    def next(self, lexeme):
        self.line = self.lexer.reader.state.line
        self.column = self.lexer.reader.state.column
        self.current_lexeme = lexeme

    def revert(self):
        self.lexer.state = self
        self.reader_state.revert()