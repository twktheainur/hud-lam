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
from lexemes.Slice import Slice

from Lexer import Lexer
from LexerState import LexerState
from lam_exceptions.SyntacticError import SyntacticError
from abstract_syntax_tree.Node import *


class Parser(object):
    """
    Parse a source file
    This is a standard recursive descent parser. The base code offers
    the possibility to do indefinite lookahead which makes it possible to
    implement LL(k) parsers.
    """
    def __init__(self,filename,str_in=False):
#       Instanciate and initialize the Lexer
        self.lexer = Lexer(filename,str_in)
        self.importing = False
        self.name = filename.split('.')[0]

    def mod_name(self):
#        Extracts the name of the main module form the file name
#       ( ie takes off the file extention)
         fc = self.lexer.reader.source_file.filename.split('.')
         return fc[len(fc)-2]

    def generate_py_ast(self):
        print "Parsing dude!"
        #parse source file
        tree = self.parse()
        #generate python AST from hud-lam AST
        return tree.python_ast()

    def parse(self):
        #starting point of the recusive descent
        return self.__program()

    def __program(self):
        # program: import_statement|class_declaration_statement|entry_point_statement
        node =ModuleNode(self)
        while(self.lexer.state.current_lexeme!=None and not self.__lexeme_is(EOF)):
            if(self.__lexeme_is(Import)):
                node.add_import(self.__import())
            elif self.__lexeme_is(Class):
                node.add_class(self.__class())
            elif (self.__lexeme_is(Enter)):
                entry = self.__entry_point()
                if not self.importing:
                    node.add_entry(entry)
            else:
                self.__raise_error("baur, gond, or minna",
                                   self.__lexeme_string())
        return node

    def __import(self):
        #import_statement: IMPORT MODULENAME
        self.__ascertain_lexeme(Import)
        name=self.__lexeme_string()
        self.__check_name(ModuleName)
        return ImportNode(self,name)
    
    def __class(self):
        #class_declaration_statement: CLASS CLASSNAME (PARENT CLASSNAME(SEPARATOR CLASSNAME)*)?
        #                             BLOCKSTART (affectation_statement)* BLOCKEND
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
        while(self.__lexeme_is(Name) or self.__lexeme_is(Function) or self.__lexeme_is(Bound)):
            if self.__lexeme_is(Name):
                node.add_member(self.__affectation_statement())
            else:
                node.add_member(self.__function_declaration_statement())
        self.__ascertain_lexeme(BlockEnd)
        return node


    def __entry_point(self):
        #entry_point_statement: ENTER BLOCKSTART instruction_sequence BLOCKEND
        node = EntryNode(self)
        self.__ascertain_lexeme(Enter)
        self.__ascertain_lexeme(BlockStart)
        node.def_function(self.__instruction_sequence())
        self.__ascertain_lexeme(BlockEnd)
        return node

    def __instruction_sequence(self):
        #instruction_sequence: instruction (instruction INSTRUCTIONSEPARATOR)*
        node = InstructionSequenceNode(self)
        node.add_instruction(self.__instruction())
        if(self.__lexeme_is(InstructionSeparator)):
            self.lexer.next()
        while (self.__lexeme_is(Name) or self.__lexeme_is(This) or\
        self.__lexeme_is(For) or self.__lexeme_is(If) or
         self.__lexeme_is(Parent) or self.__lexeme_is(Echo) or self.__lexeme_is(Input)) and\
         not self.__lexeme_is(Catch):
            node.add_instruction(self.__instruction())
            if(self.__lexeme_is(InstructionSeparator)):
                self.lexer.next()
        return node

    def __instruction(self):
        #instruction: try_statement|if_statement|do_statement|for_statement|echo_statement|
        #             input_statement|affectation_statement
        node = None
        if self.__lexeme_is(Try):
            node = self.__try__statement()
        elif self.__lexeme_is(If):
            node = self.__if_statement(False)
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
        # for_statement: FOR NAME IN sequence_literal|access_statement[[type(sequence)]]
        self.__ascertain_lexeme(For)
        var_name= self.__lexeme_string()
        self.__ascertain_lexeme(Name)
        self.__ascertain_lexeme(In)
        seq_node = None
        if(self.__lexeme_is(SeqStart)):
            seq_node=self.__sequence_literal()
        else:
#           the Access statement is handled by __affectation_statement
            seq_node=self.__affectation_statement()
        self.__ascertain_lexeme(BlockStart)
        inst_seq=self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return ForInNode(self,var_name,seq_node,inst_seq)

    #a While instruction
    def __for_if_statement(self):
        test=None
        if(self.__lexeme_is(For)):
            self.__ascertain_lexeme(For)
            self.__ascertain_lexeme(If)
            test=self.__boolean_expression()
            self.__ascertain_lexeme(BlockStart)
        inst_seq=self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return ForIfNode(self,test,inst_seq)

    def __if_statement(self,elseif):
        #if_statement: IF boolean_expression BLOCKSTART instruction_sequence
        #              (ELSE IF boolean_expression BLOCKSTART instruction_sequence)*
        #              (ELSE BLOCKSTART instruction_sequence)? BLOCKEND
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

    def __sequence_literal(self):
        #sequence_literal: SEQSTART (expression)+|INTEGETLITERAL SLICE INTEGERLITERAL SEQEND
        node = SequenceNode(self)
        self.__ascertain_lexeme(SeqStart)
        if self.__lexeme_is(Slice,2):
            start = int(self.__lexeme_string())
            self.__ascertain_lexeme(IntegerLiteral)
            self.__ascertain_lexeme(Slice)
            end = int(self.__lexeme_string())
            self.__ascertain_lexeme(IntegerLiteral)
            step = 1
            if start>end:
                step=-1
            for i in range(start,end,step):
                node.add_item(ValuedNode(self,str(i),IntegerLiteral))
        else:
            node.add_item(self.__expression())
            while self.__lexeme_is(Separator):
                self.lexer.next()
                node.add_item(self.__expression())
        self.__ascertain_lexeme(SeqEnd)
        return node

    def __echo_statement(self):
        #echo_statement: ECHO expression (SEPARATOR expression)*
        node = EchoNode(self)
        self.__ascertain_lexeme(Echo)
        node.add_expr(self.__expression())
        while self.__lexeme_is(Separator):
            self.lexer.next()
            node.add_expr(self.__expression())
        return node

    def __input_statement(self):
        #input_statement: INPUT GROUPSTART StringLiteral GROUPEND
        self.__ascertain_lexeme(Input)
        self.__ascertain_lexeme(GroupStart)
        expr=ValuedNode(self,self.__lexeme_string(),StringLiteral)
        self.__ascertain_lexeme(StringLiteral)
        self.__ascertain_lexeme(GroupEnd)
        return InputNode(self,expr)
        
    def __affectation_statement(self):
        #affectation_statement: access_statement (AFFECT access_statement|function_declaration_Statement)?
        affectee=self.__access_statement()
        value=None
        if self.__lexeme_is(Affectation):
            self.__ascertain_lexeme(Affectation)
            if self.__lexeme_is(Input):
                value=self.__input_statement()
            else:
                value=self.__expression()
            if value==None:
                return AccessRootNode(self,affectee,'load')
            else:
                return AffectationNode(self,AccessRootNode(self,affectee,'store'),value)

    def __try__statement(self):
        #try_statement: TRY BLOCKSTART instruction_sequence CATCH (ClassName) BLOCKSTART instruction_sequence BLOCKEND
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
        #expression: boolean_expression
        return self.__boolean_expression()

    def __comparee(self):
        #comparee: term ((PLUS|MINUS) term)?
        factor=self.__term()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="+" or
                                              self.__lexeme_string()=="-"):
            operator=self.__lexeme_string()
            self.lexer.next()
            right=self.__term()
            factor = BinaryOperatorNode(self,factor,operator,right)
        return factor

    def __term(self):
        #term = factor ((TIMES|DIVIDED|MODULUS) factor)?
        factor=self.__factor()
        while self.__lexeme_is(Operator) and (self.__lexeme_string()=="*" or \
              self.__lexeme_string()=="/" or self.__lexeme_string()=="%"):
            operator=self.__lexeme_string()
            self.lexer.next()
            right=self.__factor()
            factor = BinaryOperatorNode(self,factor,operator,right)
        return factor
    
    def __factor(self):
        #factor = NONE|FLOATLITERAL|INTEGERLITERAL|STRINGLITERAL|sequence_literal|
        #         access_statement|((MINUS|NOT)expression)| GROUPSTART expression GROUPEND

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
            ret=self.__sequence_literal()
        elif self.__lexeme_is(This) or self.__lexeme_is(Name):
            ret=AccessRootNode(self,self.__access_statement(),'load')
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
            self.__raise_error("Factor", self.__lexeme_string())
        return ret

    def __boolean_expression(self):
        #boolean_expression: TRUE|FALSE|(relation ((AND|OR) relation)?)
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
        #relation = coparee ((LT|GT|LE,GE,EQ,NEQ) comparee)?
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
        #access_Statement: ((PARENT ACCESS CLASSNAME ACCESS NAME
#                           GROUPSTART
#                           expression (SEPARATOR expression)* GROUPEND )
#                           |NAME|THIS) (ACCESS access_statement|array_access_statement|call_statement)
        name=None
        accessee=None
        #Access to a class member
        if self.__lexeme_is(This) and not rec:
            name = self.__lexeme_string()
            self.__ascertain_lexeme(This)
        #Access to members of a variable
        elif self.__lexeme_is(Name):
            name = self.__lexeme_string()
            self.__ascertain_lexeme(Name)
        #Access to methods/attributes of the parent class
        elif self.__lexeme_is(Parent) and not rec:
            name = self.__lexeme_string()
            pname = ""
            mname = ""
            args = []
            #adar
            self.__ascertain_lexeme(Parent)
            #.
            self.__ascertain_lexeme(Access)
            #(ClassName)
            if self.__lexeme_is(Name):
                pname = self.__lexeme_string()
                self.__check_name(ClassName)
            if self.__lexeme_is(Access):
                self.lexer.next()
                mname = self.__lexeme_string()
                self.__ascertain_lexeme(Name)
            #((expression)?(separator expression)*)
            self.__ascertain_lexeme(GroupStart)
            while not self.__lexeme_is(GroupEnd):
                args.append(self.__expression())
                if not self.__lexeme_is(GroupEnd):
                    self.__ascertain_lexeme(Separator)
            self.__ascertain_lexeme(GroupEnd)
            accessee = SuperNode(self,pname,mname,args)
            return accessee
        #Recursive sub access
        if self.__lexeme_is(Access):
            self.__ascertain_lexeme(Access)
            if self.__lexeme_is(Name):
                name = self.__lexeme_string()
                self.__ascertain_lexeme(Name)
                if self.__lexeme_is(SeqStart):
                    accessee = self.__array_access_statement(name)
            elif self.__lexeme_is(Call):
                accessee = self.__call_statement()
            else:
                accessee = self.__access_statement(True)
        return AccessNode(self,name,accessee)

    def __array_access_statement(self):
        #array_access_statement: SEQSTART expression SEQEND
        self.__ascertain_lexeme(SeqStart)
        expr = self.__expression()
        sub_accessor=None
        self.__ascertain_lexeme(SeqEnd)
        if self.__lexeme_is(SeqStart):
            sub_accessor = self.__array_access_statement()
        return ArrayAccessorNode(self,expr,sub_accessor)

    def __call_statement(self):
        #call_Statement: CALL GROUPSTART expression (SEPARATOR expression)* GROUPEND
        call_node = CallNode(self)
        self.__ascertain_lexeme(Call)
        self.__ascertain_lexeme(GroupStart)
        while not self.__lexeme_is(GroupEnd):
            call_node.add_argument(self.__expression())
            if not self.__lexeme_is(GroupEnd):
                self.__ascertain_lexeme(Separator)
        self.__ascertain_lexeme(GroupEnd)
        return call_node

    def __function_declaration_statement(self):
        # (BOUND)? FUNCTION NAME GROUPSTART expression (SEPARATOR expression)* GROUPEND
#         BLOCKSTART instruction_sequence BLOCKEND
        bound = False
        if self.__lexeme_is(Bound):
            bound = True
            self.__ascertain_lexeme(Bound)
        self.__ascertain_lexeme(Function)
        name = self.__lexeme_string()
        self.__ascertain_lexeme(Name)
        func_node = FunctionNode(self,name,bound)
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
        func_node.instruction_sequence = self.__instruction_sequence()
        self.__ascertain_lexeme(BlockEnd)
        return func_node
        
    def __lexeme_is(self,lclass,n=-1):
        #determine if the nth lexeme corresponds to lcalss
        if n<=1:
            return self.lexer.state.current_lexeme == lclass
        #for n>1 we need to do a look ahead in the source file and then restore the start state
        else:
            start_state = LexerState(self.lexer,self.lexer.state)
            lexeme = None
            for i in range(1,n):
                lexeme = self.lexer.next()
            result = (lexeme==lclass)
            start_state.revert()
            return result

    def __lexeme_string(self):
        return self.lexer.state.current_lexeme.string
    
    def __name_is(self,expected_type):
        #returns true if a Name Lexeme's class matches the expected_type subclass type
        return expected_type.match(self.lexer.state.current_lexeme.string)!=None

    def __check_name(self,expected_type):
        #If the name is the wrong type trigger a syntactic error
        if not self.__name_is(expected_type):
            self.__raise_error("Valid " + str(expected_type).split('.')[1],
                                '"'+self.lexer.state.current_lexeme.string+'"')
        self.lexer.next();

    def __ascertain_lexeme(self,lclass):
#        if the current lexeme's class does not match lclass raise and exception
        if(not self.__lexeme_is(lclass)):
            self.__raise_error(lclass.string,self.lexer.state.current_lexeme.string)
        self.lexer.next();

    def __raise_error(self,exp,found):
        raise SyntacticError(self.lexer.state.line,self.lexer.state.column,exp,found);
