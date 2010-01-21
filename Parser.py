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
from lexemes.Try import Try
from lexemes.Catch import Catch
from lexemes.Else import Else
from lexemes.Echo import Echo
from lexemes.Input import Input
from lexemes.In import In

class Parser(object):
    def __init__(self,filename):
        self.lexer = Lexer(filename)

    def parse(self):
        print self.__program(1)

    def __program(self,ilevel):
        s="Program\n"
        while(self.lexer.state.current_lexeme!=None and not self.__lexeme_is(EOF)):
            if(self.__lexeme_is(Import)):
                s+=self.__tabs(ilevel)+self.__import(ilevel+1)+"\n"
            elif self.__lexeme_is(Class):
                s+=self.__tabs(ilevel)+self.__class(ilevel+1)+"\n"
            elif (self.__lexeme_is(Enter)):
                s+=self.__tabs(ilevel)+self.__entry_point(ilevel+1)+"\n"
            else:
                self.__raise_syntax_error(self.lexer.reader.state.line,
                                          self.lexer.reader.state.column,
                                          "baur, gond, or minna",
                                          self.__lexeme_string())
        return s

    def __import(self,ilevel):
        s= self.__tabs(ilevel)+"Import "
        self.__ascertain_lexeme(Import)
        s+=self.__lexeme_string()
        self.__check_name(ModuleName)
        return s
    
    def __class(self,ilevel):
        s= self.__tabs(ilevel)+"Class "
        self.__ascertain_lexeme(Class)
        if self.__lexeme_is(Name):
            s+= self.__lexeme_string()
            self.__check_name(ClassName)
        if self.__lexeme_is(Parent):
            s+= " Inherits from "
            self.lexer.next()
            if self.__lexeme_is(Name) :
                s+= self.__lexeme_string()
                self.__check_name(ClassName),
            while self.__lexeme_is(Separator):
                s+=  ","
                self.lexer.next()
                if self.__lexeme_is(Name):
                    s+= self.__lexeme_string()
                    self.__check_name(ClassName)
            s+= ":\n"
        self.__ascertain_lexeme(BlockStart)
        while(self.__lexeme_is(Name)):
            s+=self.__tabs(ilevel+1)+self.__affectation_statement(ilevel+1)
            s+="\n"
        self.__ascertain_lexeme(BlockEnd)
        s+="\n"+self.__tabs(ilevel)+"end"
        return s


    def __entry_point(self,ilevel):
        s= "Program Main Entry Point:\n"
        self.__ascertain_lexeme(Enter)
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel+1)
        self.__ascertain_lexeme(BlockEnd)
        s+="\n"+self.__tabs(ilevel-2)+"end"
        return s

    def __instruction_sequence(self,ilevel):
        s= ""
        s+=self.__tabs(ilevel)+self.__instruction(ilevel+1)
        if(self.__lexeme_is(InstructionSeparator)):
            s+=";"
            self.lexer.next()
        s+="\n"
        while (self.__lexeme_is(Name) or self.__lexeme_is(This) or\
        self.__lexeme_is(For) or self.__lexeme_is(If) or self.__lexeme_is(Do) or
         self.__lexeme_is(Parent) or self.__lexeme_is(Echo) or self.__lexeme_is(Input)) and\
         not self.__lexeme_is(Catch):
            s+=self.__tabs(ilevel)+self.__instruction(ilevel+1)
            if(self.__lexeme_is(InstructionSeparator)):
                s+=";"
                self.lexer.next()
            s+="\n"
        return s

    def __instruction(self,ilevel):
        s= ""

        if self.__lexeme_is(Try):
            s+= self.__try__statement(ilevel+1)
        elif self.__lexeme_is(If):
            s+= self.__if_statement(False,ilevel+1)

        elif self.__lexeme_is(Do):
            s+= self.__do_statement(ilevel+1)

        elif self.__lexeme_is(For):
            if self.__lexeme_is(Name,2) and\
               self.__lexeme_is(In,3):
                s+= self.__for_in_statement(ilevel+1)
            else:
                s+= self.__for_if_statement(ilevel+1)
        elif self.__lexeme_is(Echo):
            s+=self.__echo_statement(ilevel+1)
        elif self.__lexeme_is(Input):
            s+=self.__input_statement(ilevel+1)
        elif self.__lexeme_is(Name) or self.__lexeme_is(This) or self.__lexeme_is(Parent):
            s+= self.__affectation_statement(ilevel+1)
        return s
    
    def __for_in_statement(self,ilevel):
        s= "For "
        self.__ascertain_lexeme(For)
        s+= self.__lexeme_string()
        self.__ascertain_lexeme(Name)
        s+= " In "
        self.__ascertain_lexeme(In)
        if(self.__lexeme_is(SeqStart)):
            s+=self.__sequence_litteral(ilevel+1)
        else:
            s+=self.__affectation_statement(ilevel+1)
        s+= ":\n"
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel-1)
        self.__ascertain_lexeme(BlockEnd)
        s+="\n"+self.__tabs(ilevel-2)+"end"
        return s


    def __for_if_statement(self,ilevel):
        s= "For "
        self.__ascertain_lexeme(For)
        if self.__lexeme_is(Affectation, 2):
            s+=self.__affectation_statement(ilevel+1)
        else:
            s+=self.__lexeme_string()
            self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(If)
        s+= " When "
        s+=self.__boolean_expression(ilevel+1)

        if(self.__lexeme_is(Do)):
            self.lexer.next()
            s+=" Do "
            s+=self.__instruction(ilevel+1)
            s+=":\n"
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel-1)
        self.__ascertain_lexeme(BlockEnd)
        s+= "\n"+self.__tabs(ilevel-2)+"end"
        return s

    def __if_statement(self,elseif,ilevel):
        s=""
        if self.__lexeme_is(If) or\
          (elseif and self.__lexeme_is(Else) and\
           self.__lexeme_is(If,2)):
            if elseif:
                s+="Else "
                self.lexer.next()
            s+="If "
            self.lexer.next()
            s+=self.__boolean_expression(ilevel+1)
            s+= ":\n"
            self.__ascertain_lexeme(BlockStart)
            s+=self.__instruction_sequence(ilevel+1)
            if self.__lexeme_is(Else) and self.__lexeme_is(If,2):
                s+=self.__tabs(ilevel-2)+self.__if_statement(True,ilevel-2)
            elif self.__lexeme_is(Else):
                s+=self.__tabs(ilevel)+"Else:\n"
                self.lexer.next()
                self.__ascertain_lexeme(BlockStart)
                s+=self.__instruction_sequence(ilevel+1)
                s+="\n"+self.__tabs(ilevel)+"end"
                self.__ascertain_lexeme(BlockEnd)
            else:
                s+="\n"+self.__tabs(ilevel)+"end"
                self.__ascertain_lexeme(BlockEnd)
        return s


    def __do_statement(self,ilevel):
        s= "Do:\n"
        self.__ascertain_lexeme(Do)
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel+1)
        s+= "\n"+self.__tabs(ilevel-2)+"end  "
        self.__ascertain_lexeme(BlockEnd)
        if(self.__lexeme_is(For)):
            s+="For "
            self.__ascertain_lexeme(For)
            s+="When "
            self.__ascertain_lexeme(If)
            s+=self.__boolean_expression(ilevel+1)
        return s

    def __sequence_litteral(self,ilevel):
        s="["
        self.__ascertain_lexeme(SeqStart)
        s+=self.__expression(ilevel+1)
        while self.__lexeme_is(Separator):
            s+=","
            self.lexer.next()
            s+=self.__expression(ilevel+1)
        s+="]"
        self.__ascertain_lexeme(SeqEnd)
        return s

    def __echo_statement(self,ilevel):
        s="echo "
        self.__ascertain_lexeme(Echo)
        s+=self.__expression(ilevel+1)
        while self.__lexeme_is(Separator):
            self.lexer.next()
            s+=", "+self.__expression(ilevel+1)
        return s

    def __input_statement(self,ilevel):
        s="input"
        self.__ascertain_lexeme(Input)
        s+="("
        self.__ascertain_lexeme(GroupStart)
        s+=self.__expression(ilevel+1)
        self.__ascertain_lexeme(GroupEnd)
        s+=")"
        return s
        
    def __affectation_statement(self,ilevel):
        s=""
        s+=self.__access_statement(ilevel+1)
        if self.__lexeme_is(Affectation):
            self.__ascertain_lexeme(Affectation)
            s+=":="
            if self.__lexeme_is(Function) or self.__lexeme_is(Bound):
                s+=self.__function_declaration_statement(ilevel+1)
            elif self.__lexeme_is(Input):
                s+=self.__input_statement(ilevel+1)
            else:
                s+=self.__expression(ilevel+1)
        return s

    def __try__statement(self,ilevel):
        s="try:\n"
        self.__ascertain_lexeme(Try)
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel+1)
        s+=self.__tabs(ilevel-2)+"catch "
        self.__ascertain_lexeme(Catch)
        if self.__lexeme_is(Name) and self.__name_is(ClassName):
            s+=self.__lexeme_string()
            self.lexer.next()
        s+=":\n"
        self.__ascertain_lexeme(BlockStart)
        
        s+=self.__instruction_sequence(ilevel+1)
        self.__ascertain_lexeme(BlockEnd)
        s+="\n"+self.__tabs(ilevel-2)+"end"
        return s

    def __expression(self,ilevel):
        return self.__boolean_expression(ilevel+1)

    def __comparee(self,ilevel):
        s=self.__term(ilevel+1)
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="+" or
                                              self.__lexeme_string()=="-"):
            s+=self.__lexeme_string()
            self.lexer.next()
            s+=self.__term(ilevel+1)
        return s

    def __term(self,ilevel):
        s=self.__factor(ilevel+1)
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="*" or \
              self.__lexeme_string()=="/" or self.__lexeme_string()=="%"):
            s+=self.__lexeme_string()
            self.lexer.next()
            s+=self.__factor(ilevel+1)
        return s
    def __factor(self,ilevel):
        s=""
        if self.__lexeme_is(NoneL):
            s+= "None"
            self.lexer.next()
        elif self.__lexeme_is(FloatLiteral):
            s+=self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(IntegerLiteral):
            s+=self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(StringLiteral):
            s+=self.__lexeme_string()
            self.lexer.next()
        elif self.__lexeme_is(SeqStart):
            s+=self.__sequence_litteral(ilevel+1)
        elif self.__lexeme_is(This) or self.__lexeme_is(Name):
            s+=self.__access_statement(ilevel+1)
        elif self.__lexeme_is(Not) or ( self.__lexeme_is(Operator) and\
                                        self.__lexeme_string()=='-'):
            s+=self.__lexeme_string()
            self.lexer.next()
            s+=self.__expression()
        elif self.__lexeme_is(GroupStart):
            self.__ascertain_lexeme(GroupStart)
            s+= '('
            s+=self.__expression(ilevel+1)
            s+= ')'
            self.__ascertain_lexeme(GroupEnd)
        else:
            self.__raise_syntax_error(self.lexer.reader.state.line,
                                      self.lexer.reader.state.column,
                                      "Factor", self.__lexeme_string())
        return s

    def __boolean_expression(self,ilevel):
        s=""
        if(self.__lexeme_is(True)):
            s+= "True"
            self.lexer.next()
        elif self.__lexeme_is(False):
            s+= "False"
            self.lexer.next()
        else:
            s+=self.__relation(ilevel+1)
            while (self.__lexeme_is(And) or self.__lexeme_is(Or)):
                if self.__lexeme_is(And):
                    s+=" and "
                else:
                    s+=" or "
                self.lexer.next()
                s+=self.__relation(ilevel+1)
        return s

    def __relation(self,ilevel):
        s=self.__comparee(ilevel+1)
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=='>'  or\
              self.__lexeme_string()=='>=' or self.__lexeme_string()=='<'  or\
              self.__lexeme_string()=='<=' or self.__lexeme_string()=='==' or\
              self.__lexeme_string()=='!='):
                  s+=self.__lexeme_string()
                  self.lexer.next()
                  s+=self.__comparee(ilevel+1)
        return s

    def __access_statement(self,ilevel):
        s=""
        if self.__lexeme_is(This):
            #print "This",
            s+="This"
            self.__ascertain_lexeme(This)
        elif self.__lexeme_is(Name):
            s+=self.__lexeme_string()
            self.__ascertain_lexeme(Name)
        elif self.__lexeme_is(Parent):
            self.__ascertain_lexeme(Parent)
            s+="Parent"
            if self.__lexeme_is(Access):
                s+="."
                self.lexer.next()
                if self.__lexeme_is(Name):
                    self.__check_name(ClassName)
                self.__ascertain_lexeme(GroupStart)
                s+="("
                while not self.__lexeme_is(GroupEnd):
                    s+=self.__expression(ilevel+1)
                    if not self.__lexeme_is(GroupEnd):
                        self.__ascertain_lexeme(Separator)
                        s+=","
                s+= ")"
                self.__ascertain_lexeme(GroupEnd)
                
            return s
        while self.__lexeme_is(Access):
            self.lexer.next()
            s+="."
            if self.__lexeme_is(Name):
                s+=self.__lexeme_string()
                self.__ascertain_lexeme(Name)
                if self.__lexeme_is(SeqStart):
                    while self.__lexeme_is(SeqStart):
                        self.__ascertain_lexeme(SeqStart)
                        s+= "["
                        s+=self.__expression(ilevel+1)
                        s+= "]"
                        self.__ascertain_lexeme(SeqEnd)

            elif self.__lexeme_is(Call) or self.__lexeme_is(Bound):
                s+=self.__call_statement(ilevel+1)
        return s

    def __call_statement(self,ilevel):
        s= u"call("
        self.__ascertain_lexeme(Call)
        self.__ascertain_lexeme(GroupStart)
        while not self.__lexeme_is(GroupEnd):
            s+=self.__expression(ilevel+1)
            if not self.__lexeme_is(GroupEnd):
                self.__ascertain_lexeme(Separator)
                s+=","
        s+= ")"
        self.__ascertain_lexeme(GroupEnd)
        return s

    def __function_declaration_statement(self,ilevel):
        s=""
        if self.__lexeme_is(Bound):
            s+= "Bound "
            self.__ascertain_lexeme(Bound)
        self.__ascertain_lexeme(Function)
        s+= "Function("
        self.__ascertain_lexeme(GroupStart)
        if self.__lexeme_is(Name):
            s+= self.__lexeme_string()
            self.__ascertain_lexeme(Name)
        while self.__lexeme_is(Separator):
            s+= self.__lexeme_string()
            self.lexer.next()
            s+= self.__lexeme_string()
            self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(GroupEnd)
        s+= "):\n"
        self.__ascertain_lexeme(BlockStart)
        s+=self.__instruction_sequence(ilevel+1)
        self.__ascertain_lexeme(BlockEnd)
        s+="\n"+self.__tabs(ilevel-1)+"end"
        return s
        
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
    def __tabs(self,level):
        s=""
        for i in range(1,level):
            s+="  "
        return s

    def __lexeme_string(self):
        return self.lexer.state.current_lexeme.string
    def __name_is(self,expected_type):
        return expected_type.match(self.lexer.state.current_lexeme.string)!=None

    def __check_name(self,expected_type):
        if not self.__name_is(expected_type):
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




