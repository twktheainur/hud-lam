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

from Lexer import Lexer
from LexerState import LexerState
from lam_exceptions.SyntacticError import SyntacticError
from abstract_syntax_tree.Node import *


class Parser(object):
    """
    Parse a source file
    """
    def __init__(self,filename):
        self.lexer = Lexer(filename)

    def mod_name(self):
         fc = self.lexer.reader.source_file.filename.split('.')
         return fc[len(fc)-2]

    def generate_py_module(self):
        tree = self.parse()
#        mod_name = self.mod_name()
#        module = types.ModuleType(mod_name)
        return tree.module()

    def parse(self):
        return self.__program()

    def __program(self):
        node =ModuleNode(self)
        while(self.lexer.state.current_lexeme!=None and not self.__lexeme_is(EOF)):
            if(self.__lexeme_is(Import)):
                node.add_import(self.__import())
            elif self.__lexeme_is(Class):
                node.add_class(self.__class())
            elif (self.__lexeme_is(Enter)):
                node.add_entry(self.__entry_point())
            else:
                self.__raise_error("baur, gond, or minna",
                                   self.__lexeme_string())
        return node

    def __import(self):
        self.__ascertain_lexeme(Import)
        name=self.__lexeme_string()
        self.__check_name(ModuleName)
        return ImportNode(self,name)
    
    def __class(self):
        
        self.__ascertain_lexeme(Class)
        if self.__lexeme_is(Name):
            name= self.__lexeme_string()
            self.__check_name(ClassName)
        node = ClassNode(self,name)
        if self.__lexeme_is(Parent):
            self.lexer.next()
            if self.__lexeme_is(Name) :
                pname = self.__lexeme_string()
                self.__check_name(ClassName)
                node.add_parent(pname)
            while self.__lexeme_is(Separator):
                self.lexer.next()
                if self.__lexeme_is(Name):
                    pname= self.__lexeme_string()
                    self.__check_name(ClassName)
                    node.add_parent(pname)
        self.__ascertain_lexeme(BlockStart)
        while(self.__lexeme_is(Name)):
            node.add_member(self.__affectation_statement())
        self.__ascertain_lexeme(BlockEnd)
        return node


    def __entry_point(self):
        node = EntryNode(self)
        self.__ascertain_lexeme(Enter)
        self.__ascertain_lexeme(BlockStart)
        node.def_function(self.__instruction_sequence())
        self.__ascertain_lexeme(BlockEnd)
        return node

    def __instruction_sequence(self):
        node = InstructionSequenceNode(self)
        node.add_instruction(self.__instruction())
        if(self.__lexeme_is(InstructionSeparator)):
            self.lexer.next()
        while (self.__lexeme_is(Name) or self.__lexeme_is(This) or\
        self.__lexeme_is(For) or self.__lexeme_is(If) or self.__lexeme_is(Do) or
         self.__lexeme_is(Parent) or self.__lexeme_is(Echo) or self.__lexeme_is(Input)) and\
         not self.__lexeme_is(Catch):
            node.add_instruction(self.__instruction())
            if(self.__lexeme_is(InstructionSeparator)):
                self.lexer.next()
        return node

    def __instruction(self):
        node = None
        if self.__lexeme_is(Try):
            node = self.__try__statement()
        elif self.__lexeme_is(If):
            node = self.__if_statement(False)
        elif self.__lexeme_is(Do):
            node = self.__do_statement()
        elif self.__lexeme_is(For):
            if self.__lexeme_is(Name,2) and\
               self.__lexeme_is(In,3):
                node = self.__for_in_statement()
            else:
                node = self.__for_if_statement()
        elif self.__lexeme_is(Echo):
            node = self.__echo_statement()
        elif self.__lexeme_is(Input):
            node = self.__input_statement()
        elif self.__lexeme_is(Name) or self.__lexeme_is(This) or self.__lexeme_is(Parent):
            node = self.__affectation_statement()
        return node
    
    def __for_in_statement(self):
        self.__ascertain_lexeme(For)
        var_name= self.__lexeme_string()
        self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(In)
        isseq = True
        seq_node = None
        if(self.__lexeme_is(SeqStart)):
            seq_node=self.__sequence_litteral()
        else:
#           the Access statement is handled by __affectation_statement
            isseq = False
            seq_node=self.__affectation_statement()
        self.__ascertain_lexeme(BlockStart)
        inst_seq=self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return ForInNode(self,var_name,isseq,seq_node,inst_seq)


    def __for_if_statement(self):
        self.__ascertain_lexeme(For)
        aff_stmt = None
        isaff = True
        do_instr = None
        if self.__lexeme_is(Affectation, 2):
            aff_stmt=self.__affectation_statement()
        else:
            aff_stmt=self.__lexeme_string()
            isaff=False
            self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(If)
        test=self.__boolean_expression()

        if(self.__lexeme_is(Do)):
            self.lexer.next()
            do_instr=self.__instruction()
        self.__ascertain_lexeme(BlockStart)
        instr_seq=self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return ForIfNode(self,isaff,aff_stmt,test,do_instr,instr_seq)

    def __if_statement(self,elseif):
        iftrue = None
        orelse = None
        test = None
        if self.__lexeme_is(If) or\
          (elseif and self.__lexeme_is(Else) and\
           self.__lexeme_is(If,2)):
            if elseif:
                self.lexer.next()
            self.lexer.next()
            test=self.__boolean_expression()
            self.__ascertain_lexeme(BlockStart)
            iftrue=self.__instruction_sequence()
            if self.__lexeme_is(Else) and self.__lexeme_is(If,2):
                orelse = self.__if_statement(True)
            elif self.__lexeme_is(Else):
                self.lexer.next()
                self.__ascertain_lexeme(BlockStart)
                orelse=self.__instruction_sequence()
                self.__ascertain_lexeme(BlockEnd)
            else:
                self.__ascertain_lexeme(BlockEnd)
        return IfNode(self,test,iftrue,orelse)


    def __do_statement(self):
        test=None
        self.__ascertain_lexeme(Do)
        self.__ascertain_lexeme(BlockStart)
        inst_seq=self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        if(self.__lexeme_is(For)):
            self.__ascertain_lexeme(For)
            self.__ascertain_lexeme(If)
            test=self.__boolean_expression()
        return DoNode(self,test,inst_seq)

    def __sequence_litteral(self):
        node = SequenceNode(self)
        self.__ascertain_lexeme(SeqStart)
        node.add_item(self.__expression())
        while self.__lexeme_is(Separator):
            self.lexer.next()
            node.add_item(self.__expression())
        self.__ascertain_lexeme(SeqEnd)
        return node

    def __echo_statement(self):
        print "Glamor:"
        node = EchoNode(self)
        self.__ascertain_lexeme(Echo)
        node.add_expr(self.__expression())
        while self.__lexeme_is(Separator):
            self.lexer.next()
            node.add_expr(self.__expression())
        return node

    def __input_statement(self):
        self.__ascertain_lexeme(Input)
        self.__ascertain_lexeme(GroupStart)
        expr=self.__expression()
        self.__ascertain_lexeme(GroupEnd)
        return InputNode(self,expr)
        
    def __affectation_statement(self):
        affectee=self.__access_statement()
        value=None
        if self.__lexeme_is(Affectation):
            self.__ascertain_lexeme(Affectation)
            if self.__lexeme_is(Function) or self.__lexeme_is(Bound):
                value=self.__function_declaration_statement()
            elif self.__lexeme_is(Input):
                value=self.__input_statement()
            else:
                value=self.__expression()
        return AffectationNode(self,affectee,value)

    def __try__statement(self):
        self.__ascertain_lexeme(Try)
        self.__ascertain_lexeme(BlockStart)
        try_seq = self.__instruction_sequence()
        self.__ascertain_lexeme(Catch)
        if self.__lexeme_is(Name) and self.__name_is(ClassName):
            ex_name=self.__lexeme_string()
            self.lexer.next()
        self.__ascertain_lexeme(BlockStart)
        
        catch_seq = self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return TryNode(self,try_seq,ex_name,catch_seq)

    def __expression(self):
        return self.__boolean_expression()

    def __comparee(self):
        factor=self.__term()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="+" or
                                              self.__lexeme_string()=="-"):
            operator=self.__lexeme_string()
            self.lexer.next()
            right=self.__term()
            factor = BinaryOperatorNode(self,factor,operator,right)
        return factor

    def __term(self):
        factor=self.__factor()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="*" or \
              self.__lexeme_string()=="/" or self.__lexeme_string()=="%"):
            operator=self.__lexeme_string()
            self.lexer.next()
            right=self.__factor()
            factor = BinaryOperatorNode(self,factor,operator,right)
        return factor
    
    def __factor(self):
        ret=None
        if self.__lexeme_is(NoneL):
            ret=ValuedNode(self,"None")
            self.lexer.next()
        elif self.__lexeme_is(FloatLiteral):
            ret=ValuedNode(self,self.__lexeme_string(),FloatLiteral)
            self.lexer.next()
        elif self.__lexeme_is(IntegerLiteral):
            ret=ValuedNode(self,self.__lexeme_string(),IntegerLiteral)
            self.lexer.next()
        elif self.__lexeme_is(StringLiteral):
            ret=ValuedNode(self,self.__lexeme_string(),StringLiteral)
            self.lexer.next()
        elif self.__lexeme_is(SeqStart):
            ret=self.__sequence_litteral()
        elif self.__lexeme_is(This) or self.__lexeme_is(Name):
            ret=self.__access_statement()
        elif self.__lexeme_is(Not) or ( self.__lexeme_is(Operator) and\
                                        self.__lexeme_string()=='-'):
            operator=self.__lexeme_string()
            self.lexer.next()
            ret=UnaryOperator(self,operator,self.__expression())

        elif self.__lexeme_is(GroupStart):
            self.__ascertain_lexeme(GroupStart)
            ret=self.__expression()
            self.__ascertain_lexeme(GroupEnd)
        else:
            self.__raise_error(self.lexer.reader.state.line,
                                      self.lexer.reader.state.column,
                                      "Factor", self.__lexeme_string())
        return ret

    def __boolean_expression(self):
        if(self.__lexeme_is(True)):
            factor= ValueNode(self,self.__lexeme_string(),True)
            self.lexer.next()
        elif self.__lexeme_is(False):
            factor =ValueNode(self,self.__lexeme_string(),False)
            self.lexer.next()
        else:
            factor=self.__relation()
            while (self.__lexeme_is(And) or self.__lexeme_is(Or)):
                operator = self.__lexeme_string()
                self.lexer.next()
                right=self.__relation()
                factor = BinaryOperatorNode(self,factor,operator,right)
        return factor

    def __relation(self):
        factor=self.__comparee()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=='>'  or\
              self.__lexeme_string()=='>=' or self.__lexeme_string()=='<'  or\
              self.__lexeme_string()=='<=' or self.__lexeme_string()=='==' or\
              self.__lexeme_string()=='!='):
                  operator=self.__lexeme_string()
                  self.lexer.next()
                  right=self.__comparee()
                  factor = BinaryOperatorNode(self,factor,operator,right)
        return factor

    def __access_statement(self,rec=False):
        name=None
        accessee=None
        print "access"
        #Access to a class member
        if self.__lexeme_is(This):
            name = self.__lexeme_string()
            print self.__lexeme_string(),
            self.__ascertain_lexeme(This)
        #Access to members of a variable
        elif self.__lexeme_is(Name):
            name = self.__lexeme_string()
            print self.__lexeme_string(),
            self.__ascertain_lexeme(Name)
        #Access to methods/attributes of the parent class
        elif self.__lexeme_is(Parent):
            name = self.__lexeme_string()
            pname = ""
            args = []
            #adar
            self.__ascertain_lexeme(Parent)
            #.
            self.__ascertain_lexeme(Access)
            #(ClassName)
            if self.__lexeme_is(Name):
                pname = self.__lexeme_string()
                self.__check_name(ClassName)
            #((expression)?(separator expression)*)
            self.__ascertain_lexeme(GroupStart)
            while not self.__lexeme_is(GroupEnd):
                args.append(self.__expression())
                if not self.__lexeme_is(GroupEnd):
                    self.__ascertain_lexeme(Separator)
            self.__ascertain_lexeme(GroupEnd)
            accessee = SuperNode(self,pname,args)
            return AccessNode(self,name,accessee)
        #Recursive sub access
        if self.__lexeme_is(Access):
            print "."
            self.__ascertain_lexeme(Access)
            if self.__lexeme_is(Name):
                name = self.__lexeme_string()
                self.__ascertain_lexeme(Name)
                if self.__lexeme_is(SeqStart):
                    accessee = self.__array_access_statement()    
            elif self.__lexeme_is(Call):
                accessee = self.__call_statement(name)
            else:
                accessee = self.__access_statement(True)
        return AccessNode(self,name,accessee)

    def __array_access_statement(self):
        self.__ascertain_lexeme(SeqStart)
        expr = self.__expression()
        sub_accessor=None
        self.__ascertain_lexeme(SeqEnd)
        if self.__lexeme_is(SeqStart):
            sub_accessor = self.__array_access_statement()
        return ArrayAccessorNode(self,expr,sub_accessor)

    def __call_statement(self,name):
        call_node = CallNode(self,name)
        self.__ascertain_lexeme(Call)
        self.__ascertain_lexeme(GroupStart)
        while not self.__lexeme_is(GroupEnd):
            call_node.add_argument(self.__expression())
            if not self.__lexeme_is(GroupEnd):
                self.__ascertain_lexeme(Separator)
        self.__ascertain_lexeme(GroupEnd)
        return call_node

    def __function_declaration_statement(self):
        func_node = FunctionNode(self)
        if self.__lexeme_is(Bound):
            func_node.bound = True
            self.__ascertain_lexeme(Bound)
        self.__ascertain_lexeme(Function)
        self.__ascertain_lexeme(GroupStart)
        if self.__lexeme_is(Name):
            func_node.add_parameter(self.__lexeme_string())
            self.__ascertain_lexeme(Name)
        while self.__lexeme_is(Separator):
            self.lexer.next()
            func_node.add_parameter(self.__lexeme_string())
            self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(GroupEnd)
        self.__ascertain_lexeme(BlockStart)
        func_node.body = self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return func_node
        
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
        return expected_type.match(self.lexer.state.current_lexeme.string)!=None

    def __check_name(self,expected_type):
        if not self.__name_is(expected_type):
            self.__raise_error("Valid " + str(expected_type).split('.')[1],
                                '"'+self.lexer.state.current_lexeme.string+'"')
        self.lexer.next();

    def __ascertain_lexeme(self,lclass):
        if(not self.__lexeme_is(lclass)):
            self.__raise_error(lclass.string,self.lexer.state.current_lexeme.string)
#        print "ACS: ",self.lexer.state.current_lexeme.string
        self.lexer.next();

    def __raise_error(self,exp,found):
        raise SyntacticError(self.lexer.state.line,self.lexer.state.column,exp,found);




