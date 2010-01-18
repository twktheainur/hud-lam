from Lexer import Lexer
from LexerState import LexerState
from lexemes import *
from lexemes.Import import Import
from lexemes.Enter import Enter
from lexemes.BlockStart import BlockStart
from lexemes.BlockEnd import BlockEnd
from lexemes.GroupStart import GroupStart
from lexemes.GroupEnd import GroupEnd
from lexemes.Class import Class
from lexemes.Name import Name
from lexemes.ModuleName import ModuleName
from lexemes.ClassName import ClassName
from lexemes.Call import Call
from lexemes.EOF import EOF
from lexemes.InstructionSeparator import InstructionSeparator
from lexemes.For import For
from lexemes.Access import Access
from lexemes.Affectation import Affectation
from lexemes.This import This
from lexemes.If import If
from lexemes.Do import Do
from lexemes.Function import Function
from lexemes.FloatLiteral import FloatLiteral
from lexemes.IntegerLiteral import IntegerLiteral
from lexemes.StringLiteral import StringLiteral
from lexemes.Not import Not
from lexemes.NoneL import NoneL
from lexemes.Operator import Operator
from lexemes.Or import Or
from lexemes.And import And
from lexemes.Parent import Parent
from lexemes.Separator import Separator
from lexemes.SeqEnd import SeqEnd
from lexemes.SeqStart import SeqStart
from lexemes.Bound import Bound
class Parser(object):
    def __init__(self,filename):
        self.lexer = Lexer(filename)

    def parse(self):
        self.__program()

    def __program(self):
        print "Program"
        while(self.lexer.state.current_lexeme!=None and not self.__lexeme_is(EOF)):
            if(self.__lexeme_is(Import)):
                self.__import()
            elif self.__lexeme_is(Class):
                self.__class()
            elif (self.__lexeme_is(Enter)):
                self.__entry_point()
            else:
                self.__raise_syntax_error(self.lexer.reader.state.line,
                                          self.lexer.reader.state.column,
                                          "baur, gond, or minna",
                                          self.__lexeme_string())

    def __import(self):
        print "Import ",
        self.__ascertain_lexeme(Import)
        print self.__lexeme_string()
        self.__check_name(ModuleName)

    def __class(self):
        print "Class",
        self.__ascertain_lexeme(Class)
        if self.__lexeme_is(Name):
            print self.__lexeme_string(),
            self.__check_name(ClassName)
        if self.__lexeme_is(Parent):
            print " Inherits from ",
            self.lexer.next()
            if self.__lexeme_is(Name) :
                print self.__lexeme_string(),
                self.__check_name(ClassName),
            while self.__lexeme_is(Separator):
                print ",",
                self.lexer.next()
                if self.__lexeme_is(Name):
                    print self.__lexeme_string(),
                    self.__check_name(ClassName)
            print ""
            print "BlockStart"
        self.__ascertain_lexeme(BlockStart)
        while(self.__lexeme_is(Name)):
            self.__affectation_statement()
        self.__ascertain_lexeme(BlockEnd)


    def __entry_point(self):
        print "Program Main Entry Point"
        self.__ascertain_lexeme(Enter)
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)

    def __instruction_sequence(self):
        print "Instruction sequence start:"
        self.__instruction()
        if(self.__lexeme_is(InstructionSeparator)):
            self.lexer.next()
        while self.__lexeme_is(Name) or self.__lexeme_is(This) or\
        self.__lexeme_is(For) or self.__lexeme_is(If) or self.__lexeme_is(Do):
            self.__instruction()
            if(self.__lexeme_is(InstructionSeparator)):
                self.lexer.next()
        print "Instruction Sequence End"

    def __instruction(self):
        print "Instruction: ",
        if (self.__lexeme_is(Name) or \
            self.__lexeme_is(This)) and \
            self.__lexeme_is(Access,2):

            self.__access_statement()

        elif self.__lexeme_is(Name):
            self.__affectation_statement()

        elif self.__lexeme_is(If):
            self.__if_statement()

        elif self.__lexeme_is(Do):
            self.__do_statement()

        elif self.__lexeme_is(For) and self.__lexeme_is(Name,2) and\
             self.__lexeme_is(In,3):
            self.__for_in_statement()

        elif self.__lexeme_is(For) and self.__lexeme_is(Name,2) and\
             self.__lexeme_is(If,3):
            self.__for_if_statement()

    def __for_in_statement(self):
        print "For",
        self.__ascertain_lexeme(For)
        print self.__lexeme_string(),
        self.__ascertain_lexeme(Name)
        print "In",
        self.__ascertain_lexeme(In)
        if(self.__lexeme_is(SeqStart)):
            self.__sequence_litteral()
        elif self.__lexeme_is(Name):
            print self.__lexeme_string()
            self.lexer.next()
        print "BlockStart"
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        print "BlockEnd"


    def __for_if_statement(self):
        print "For",
        self.__ascertain_lexeme(For)
        if self.__lexeme_is(Name):
            print self.__lexeme_string(),
            self.lexer.next()
        elif self.__lexeme_is(Affectation, 2):
            self.__affectation_statement()

        print "If",
        self.__boolean_expression()

        if(self.__lexeme_is(Do)):
            print "Do:",
            self.__instruction()
        print "BlockStart"
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        print "BlockEnd"

    def __if_statement(self,elseif):
        if self.__lexeme_is(If) or\
          (elseif and self.__lexeme_is(Else) and\
           self.__lexeme_is(If,2)):
            print self.__lexeme_string()
            self.lexer.next()
            self.__boolean_expression()
            print "BlockStart:"
            self.__ascertain_lexeme(BlockStart)
            self.__instruction_sequence()
            if self.__lexeme_is(Else):
                print self.__lexeme_string()
                self.lexer.next()
                self.__instruction_sequence()
                print "BlockEnd"
                self.__ascertain_lexeme(BlockEnd)
            elif self.__lexeme_is(Else) and self.__lexeme_is(If,2):
                self.__if_statement(True)
            else:
                print "BlockEnd"
                self.__ascertain_lexeme(BlockEnd)



    def __do_statement(self):
        print "Do"
        self.__ascertain_lexeme(Do)
        print "BlockStart"
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        print "BlockEnd"
        self.__ascertain_lexeme(BlockEnd)
        if(self.__lexeme_is(For)):
            print "For",
            self.__ascertain_lexeme(For)
            print "If",
            self.__ascertain_lexeme(If)
            self.__boolean_expression()

    def __sequence_litteral(self):
        print "SeqStart:",
        self.__ascertain_lexeme(SeqStart)
        self.__expression()
        while self.__lexeme_is(Separator):
            print "Separator"
            self.lexer.next()
            self.__expression()
        print "SequenceEnd"
        self.__ascertain_lexeme(SeqEnd)

    def __affectation_statement(self):
        print "Affect to:", self.__lexeme_string(),
        self.__access_statement()
        print "I return!!!"
        self.__ascertain_lexeme(Affectation)
        print " Value: ",
        if self.__lexeme_is(Function):
            self.__function_declaration_statement()
        else:
            self.__expression()

    def __expression(self):
        self.__term()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="+" or
                                              self.__lexeme_string()=="-"):
            print self.__lexeme_string()
            self.lexer.next()
            self.__term()


    def __term(self):
        self.__factor()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="*" or \
              self.__lexeme_string()=="/" or self.__lexeme_string()=="%"):
            print self.__lexeme_string()
            self.lexer.next()
            self.__factor()

    def __factor(self):
        if self.__lexeme_is(NoneL):
            print "None"
            self.lexer.next()
        elif self.__lexeme_is(FloatLiteral):
            print "Float:",self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(IntegerLiteral):
            print "Integer:", self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(StringLiteral):
            print "String:",self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(SeqStart):
            self.__sequence_litteral()
        elif self.__lexeme_is(This) or self.__lexeme_is(Name):
            self.__access_statement()
        elif self.__lexeme_is(Not) or ( self.__lexeme_is(Operator) and\
                                        self.__lexeme_string()=='-'):
            print self.__lexeme_string()
            self.__boolean_expression()
        elif self.__lexeme_is(GroupStart):
            self.__ascertain_lexeme(GroupStart)
            self.__boolean_expression()
            print ')'
            self.__ascertain_lexeme(GroupEnd)
        else:
            self.__raise_syntax_error(self.lexer.reader.state.line,
                                      self.lexer.reader.state.column,
                                      "Factor", self.__lexeme_string())

    def __boolean_expression(self):
        if(self.__lexeme_is(True)):
            print "True"
            self.lexer.next()
        elif self.__lexeme_is(False):
            print "False"
            self.lexer.next()
        else:
            self.__relation()
            while (self.__lexeme_is(And) or self.__lexeme_is(Or)):
                self.lexer.next()
                self.__relation()

    def __relation(self):
        self.__expression()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=='>'  or\
              self.__lexeme_string()=='>=' or self.__lexeme_string()=='<'  or\
              self.__lexeme_string()=='<=' or self.__lexeme_string()=='==' or\
              self.__lexeme_string()=='!='):
                  print self.__lexeme_string()
                  self.lexer.next()
                  self.__expression()


    def __access_statement(self):
        s=""
        if self.__lexeme_is(This):
            #print "This",
            s+="This"
            self.__ascertain_lexeme(This)
        elif self.__lexeme_is(Name):
            s+=self.__lexeme_string()
            self.__ascertain_lexeme(Name),
        while self.__lexeme_is(Access):
            self.lexer.next()
            s+="."
            if self.__lexeme_is(Name):
                s+=self.__lexeme_string()
                self.__ascertain_lexeme(Name)
                if self.__lexeme_is(SeqStart):
                    while self.__lexeme_is(SeqStart):
                        self.__ascertain_lexeme(SeqStart)
                        print "[",
                        self.__expression()
                        print "]",
                        self.__ascertain_lexeme(SeqEnd)

            elif self.__lexeme_is(Call):
                s+=self.__call_statement()
        return s

    def __call_statement(self):
        s= u"call("
        self.__ascertain_lexeme(Call)
        self.__ascertain_lexeme(GroupStart)
        while not self.__lexeme_is(GroupEnd):
            self.__expression()
            if not self.__lexeme_is(GroupEnd):
                self.__ascertain_lexeme(Separator)
                s+=","
        s+= ")"
        self.__ascertain_lexeme(GroupEnd)
        return s

    def __function_declaration_statement(self):
        if self.__lexeme_is(Bound):
            print "Bound"
            self.__ascertain_lexeme(Bound)
        self.__ascertain_lexeme(Function)
        print "(",
        self.__ascertain_lexeme(GroupStart)
        if self.__lexeme_is(Name):
            print self.__lexeme_string(),
            self.__ascertain_lexeme(Name)
        while self.__lexeme_is(Separator):
            print self.__lexeme_string(),
            self.lexer.next()
            print self.__lexeme_string(),
            self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(GroupEnd)
        print ")",
        self.__ascertain_lexeme(BlockStart)
        self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        
    def __lexeme_is(self,lclass, *args):
        if len(args)==0 or (len(args)==1 and args[0]==1):
            return self.lexer.state.current_lexeme == lclass
        elif len(args)==1:
            index = args[0]
            start_state = LexerState(self.lexer,self.lexer.state)
            lexeme = None
            for i in range(1,index):
                lexeme = self.lexer.next()
            result = (lexeme==lclass)
            start_state.revert()
            return result

    def __lexeme_string(self):
        return self.lexer.state.current_lexeme.string
    def __name_is(self,expected_type):
        return expected_type.match(self.lexer.state.current_lexeme.string)==None

    def __check_name(self,expected_type):
        if(self.__name_is(expected_type)):
            self.__raise_syntax_error(self.lexer.reader.state.line,
                                      self.lexer.reader.state.column,
                                       "Valid " + str(expected_type).split('.')[1],
                                       '"'+self.lexer.state.current_lexeme.string+'"')
        self.lexer.next();

    def __ascertain_lexeme(self,lclass):
        if(not self.__lexeme_is(lclass)):
            self.__raise_syntax_error(self.lexer.state.line,
                                      self.lexer.state.column,
                                      lclass.__name__,
                                      self.lexer.state.current_lexeme.string)
        self.lexer.next();

    def __raise_syntax_error(self,line,col,exp,found):
        raise Exception("Syntactic Error at "+str(line)+":"+str(col)+
                            ", Expected: "+ exp+". Found: "+found);




