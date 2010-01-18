from lexemes import *
from lexemes.LexemeFactory import *
from CharacterReader import *
from LexerState import LexerState

class Lexer:
    u"""
        Lexer class: reads and identifies lexemes.
    """
    def __init__(self,filename):
        self.reader = CharacterReader(filename)
        self.__factory = LexemeFactory()
        self.state = LexerState(self)
        self.state.current_lexeme = self.next()

    def next(self):
        u"""
            Creates the Lexeme class instance
            matching the next lexeme string.
        """
        self.__skip_whitespace()
        while(self.__skip_comments()):
            self.__skip_whitespace()
        lex_str = self.__read_lexeme()
        self.state.next(self.__factory.create_lexeme(lex_str))
        return self.state.current_lexeme

    def __read_lexeme(self):
        u"""Reads the next lexeme string from the file"""
        s = u"";
        #Number
        if self.reader.state.current_character.isdigit():
            s = s + self.reader.state.current_character
            self.reader.next()
            while self.reader.state.current_character.isdigit():
                s = s + self.reader.state.current_character
                self.reader.next()
            if self.reader.state.current_character == u'.':
                s=s+u'.'
                self.reader.next()
            while self.reader.state.current_character.isdigit():
                s = s + self.reader.state.current_character
                self.reader.next()
#            if not self.__is_whitespace(self.reader.state.current_character):
#                self.__raise_lexical_error('Whitespace',self.reader.state.current_character)
        #Word
        elif self.reader.state.current_character.isalpha():
            s = s + self.reader.state.current_character
            self.reader.next()
            while(self.reader.state.current_character.isdigit() or
                  self.reader.state.current_character.isalpha() or
                  self.reader.state.current_character=='_'):
                s=s+self.reader.state.current_character
                self.reader.next()
        elif self.reader.state.current_character=='!':
            s+='!'
            self.reader.next()
            if self.reader.state.current_character=='=':
                s+='='
                self.reader.next()
            else:
                self.__raise_lexical_error('=',self.reader.state.current_character)
        elif self.reader.state.current_character=='=':
            s+="=";
            self.reader.next()
            if self.reader.state.current_character=='=':
                s+='='
                self.reader.next()
        elif self.reader.state.current_character=='<':
            s+="<";
            self.reader.next()
            if self.reader.state.current_character=='=':
                s+='='
                self.reader.next()
        elif self.reader.state.current_character=='>':
            s+=">";
            self.reader.next()
            if self.reader.state.current_character=='=':
                s+='='
                self.reader.next()
        elif self.__is_quote(self.reader.state.current_character):
            start_quote = self.reader.state.current_character
            s+=start_quote
            self.reader.next()
            while(self.reader.state.current_character!=start_quote):
                if self.reader.state.current_character == '':
                    self.__raise_lexical_error(start_quote, "EOF")
                elif self.reader.state.current_character=='~':
                    self.__skip_comments()
                s+=self.reader.state.current_character
                self.reader.next()
            s+=start_quote
            self.reader.next()
        elif self.reader.state.current_character!='':
            s+=self.reader.state.current_character
            self.reader.next()
        else:
            s=''
        return s
    
    def __skip_whitespace(self):
        u"""Skips all contiguous white space characters starting from the
            next character in the file"""
        while (self.__is_whitespace(self.reader.state.current_character)):
            self.reader.next()

    def __is_whitespace(self,c):
        """Returns true is c is a whitespace character"""
        return (c == u' ' or c == u'\t' or c == u'\n' or c==u'\r')

    def is_whitespace(self,c):
        return self.__is_whitespace(c)
    def __is_quote(self,c):
        return (c=='\"' or c=='\'')


    def __skip_comments(self):
        u"""Skips all contiguous comments starting from the next character
        in the file"""
#        multi_line = False
        if self.reader.state.current_character=='~':
            self.reader.next()
            while self.reader.state.current_character!='\n':
                self.reader.next()
            return True
        return False
                
    def __raise_lexical_error(self,exp,found):
        raise Exception("Lexical error at "+str(self.reader.state.line)+":"+str(self.reader.state.line)+" found: "+found+" expected: "+exp)