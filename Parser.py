from Lexer import Lexer
from lexemes import *
from lexemes.Import import Import
from lexemes.Enter import Enter
from lexemes.BlockStart import BlockStart
from lexemes.BlockEnd import BlockEnd
from lexemes.Class import Class
from lexemes.Name import Name
from lexemes.ModuleName import ModuleName
from lexemes.ClassName import ClassName
from lexemes.EOF import EOF
class Parser:
    def __init__(self,filename):
        self.lexer = Lexer(filename)
    
    def parse(self):
        self.__program()
    
    def __program(self):
        print "Program"
        while(self.lexer.currentLexeme!=None and not self.__lexeme_is(EOF)):
            if(self.__lexeme_is(Import)):
                self.__import()
            elif self.__lexeme_is(Class):
                self.__class()
            elif (self.__lexeme_is(Enter)):
                self.__entry_point()
    
    def __import(self):
        print "Import statement"
        self.__ascertain_lexeme(Import)
        self.__check_name(ModuleName)
        
    def __class(self):
        print "Class declaration"
        pass
    def __entry_point(self):
        print "Program Main Entry Point"
        self.__ascertain_lexeme(Enter)
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
    
    def __instruction_sequence(self):
        print "Instruction Sequence here"
        print "End Instruction Sequence"
        pass
    def __lexeme_is(self,lclass):
        return self.lexer.currentLexeme == lclass
    
    def __check_name(self,expected_type):
        if(expected_type.match(self.lexer.currentLexeme.string)==None):
            self.__raise_syntax_error(self.lexer.line, self.lexer.column,
                                       "Valid variable name", self.lexer.currentLexeme.string)
        self.lexer.next();
            
    def __ascertain_lexeme(self,lclass):
        if(not self.__lexeme_is(lclass)):
            self.__raise_syntax_error(self.lexer.line, 
                                      self.lexer.column, 
                                      lclass.__name__, 
                                      self.lexer.CurrentLexeme.__name__)
        self.lexer.next();
        
    def __raise_syntax_error(self,line,col,found,exp):
        raise Exception("Syntactic Error at "+line+":"+col+
                            ", Expected: "+found+" found: "+exp);