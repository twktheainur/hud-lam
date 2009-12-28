from lexemes import *
from lexemes.LexemeFactory import *
from CharacterReader import *

class Lexer:
    u"""
        Lexer class: reads and identifies lexemes.
    """
    def __init__(self,filename):
        self.line=0
        self.column=0
        self.reader = CharacterReader(filename)
        self.__factory = LexemeFactory()
        self.currentLexeme = self.next()

    def next(self):
        u"""
            Creates the Lexeme class instance
            matching the next lexem string.
        """
        self.line=self.reader.line
        self.column=self.reader.column
        self.__skip_whitespace()
        self.__skip_comments()
        lex_str = self.__read_lexeme()
        self.currentLexeme = self.__factory.create_lexeme(lex_str)
        return self.currentLexeme

    def __read_lexeme(self):
        u"""Reads the next lexeme string from the file"""
        s = u"";
        #Number
        if self.reader.currentCharacter.isdigit():
            s = s + self.reader.currentCharacter
            self.reader.next()
            while self.reader.currentCharacter.isdigit():
                s = s + self.reader.currentCharacter
                self.reader.next()
            if self.reader.currentCharacter == u'.':
                s=s+u'.'
                self.reader.next()
            while self.reader.currentCharacter.isdigit():
                s = s + self.reader.currentCharacter
                self.reader.next()
        #Word
        elif self.reader.currentCharacter.isalpha():
            s = s + self.reader.currentCharacter
            self.reader.next()
            while(self.reader.currentCharacter.isdigit() or
                  self.reader.currentCharacter.isalpha() or
                  self.reader.currentCharacter=='_'):
                s=s+self.reader.currentCharacter
                self.reader.next()
        elif self.reader.currentCharacter=='!':
            s+='!'
            self.reader.next()
            if self.reader.currentCharacter=='=':
                s+='='
                self.reader.next()
            else:
                self.__raise_lexical_error('=',self.reader.currentCharacter)
        elif self.reader.currentCharacter=='=':
            s+="=";
            self.reader.next()
            if self.reader.currentCharacter=='=':
                s+='='
                self.reader.next()
        elif self.reader.currentCharacter=='<':
            s+="=";
            self.reader.next()
            if self.reader.currentCharacter=='=':
                s+='='
                self.reader.next()
        elif self.reader.currentCharacter=='>':
            s+="=";
            self.reader.next()
            if self.reader.currentCharacter=='=':
                s+='='
                self.reader.next()
        elif self.__is_quote(self.reader.currentCharacter):
            start_quote = self.reader.currentCharacter
            s+=start_quote
            self.reader.next()
            while(self.reader.currentCharacter!=start_quote):
                if self.reader.currentCharacter == '':
                    self.__raise_lexical_error(start_quote, "EOF")
                elif self.reader.currentCharacter=='~':
                    self.__skip_comments()
                s+=self.reader.currentCharacter
                self.reader.next()
            s+=start_quote
            self.reader.next()
        elif self.reader.currentCharacter!='':
            s+=self.reader.currentCharacter
            self.reader.next()
        else:
            s=''
        return s
    def __skip_whitespace(self):
        u"""Skips all contiguous white space characters starting from the
            next character in the file"""
        while (self.__is_whitespace(self.reader.currentCharacter)):
            self.reader.next()
    def __is_whitespace(self,c):
        """Returns true is c is a whitespace character"""
        return (c == u' ' or c == u'\t' or c == u'\n' or c==u'\r')
    def __is_quote(self,c):
        return (c=='\"' or c=='\'')


    def __skip_comments(self):
        u"""Skips all contiguous comments starting from the next character
        in the file"""
        multi_line = False
        if self.reader.currentCharacter=='~':
            self.reader.next()
            if(self.reader.currentCharacter!='~'):
                while self.reader.currentCharacter!='\n':
                    self.reader.next()
                
    def __raise_lexical_error(self,exp,found):
        raise Exception("Lexical error at "+str(self.reader.line)+":"+str(self.reader.line)+" found: "+found+" expected: "+exp)
