from lam_exceptions.SemanticError import SemanticError
from lam_exceptions.SyntacticError import SyntacticError
import types
import sys
import Parser
dir(Parser)

class Node(object):
    def __init__(self,parser):
        self.line=parser.lexer.state.line
        self.column=parser.lexer.state.line
        self.parser = parser
    def python(self,indent):
        pass

class ModuleNode(Node):
    def __init__(self,parser):
        super(ModuleNode,self).__init__(parser)
        self.name= parser.mod_name()
        self.imports=[]
        self.classes=[]
        self.main_entry=None
        self.global_context={}

    def type(self):
        return "<module>"

    def module(self):
        return types.ModuleType(str(self.name))

    def add_import(self,import_node):
        self.__register_global(import_node.name,import_node.python_mod)
        self.imports.append(import_node)

    def add_class(self,class_node):
        self.classes.append(class_node)
        
    def add_entry(self, entry):
        self.main_entry = entry

    def __register_global(self,name,item):
        self.global_context.update({name:item})

    
class ImportNode(Node):
    def __init__(self,parser,name):
        super(ImportNode,self).__init__(parser)
        self.python_mod=None
        self.name=name
        try:
            p = Parser.Parser(name+'.lam')
            self.python_mod = p.generate_py_module()
        except (SemanticError,SyntacticError) as se:
            print "In module "+name+": "
            raise se
        except:
            try:
                __import__(name)
                self.python_mod = sys.modules[name]
            except:
                raise Exception("No such module: "+name+" Semantic Error: l"+str(self.line)+"-c"+str(self.column))
        print self.python_mod

class ClassNode(Node):
    def __init__(self,parser,name):
        super(ClassNode,self).__init__(parser)
        self.name = name
        self.members = []
        self.parents = []
    def add_parent(self,name):
        self.parents.append(name)
    def add_member(self,node):
        self.members.append(node)

class InstructionSequenceNode(Node):
    def __init__(self,parser):
        super(InstructionSequenceNode,self).__init__(parser)
        self.instruction = []
    def add_instruction(self,instr_node):
        self.instruction.append(instr_node)

class FunctionNode(Node):
    def __init__(self,parser):
        super(FunctionNode,self).__init__(parser)
        self.instruction_sequence = None
        self.parameters = []
    def add_parameter(self,name):
        self.parameters.append(name)

class InstructionNode(Node):
    def __init__(self,parser):
        super(InstructionNode,self).__init__(parser)
        

class ForInNode(Node):
    def __init__(self,parser,var_name,isseq,seq_node,instr_seq):
        super(ForInNode,self).__init__(parser)

class ForIfNode(Node):
    def __init__(self,parser,isaff,aff_stmt,test,do_instr,instr_seq):
        super(ForIfNode,self).__init__(parser)

class IfNode(Node):
    def __init__(self,parser,test,iftrue,orelse):
        super(IfNode,self).__init__(parser)

class DoNode(Node):
    def __init__(self,parser,test,instr_seq):
        super(DoNode,self).__init__(parser)
        self.test_statement = test
        self.instruction_sequence = instr_seq

class BinaryOperatorNode(Node):
    def __init__(self,parser,left,operator,right):
        super(BinaryOperatorNode,self).__init__(parser)
        self.operator=operator
        self.left=left
        self.right=right
#        if hasattr(left,binary_operator_methods[operator]) and\
#           hasattr(right,binary_operator_methods[operator]):
#               if left.type() != right.type()  :
#                   pass

    def type(self):
        return left.type()
        

class UnaryOperatorNode(Node):
    def __init__(self,parser,operator,right):
        super(UnaryOperator,self).__init__(parser)
        self.operator=operator
        self.right = right

class AffectationNode(Node):
    def __init__(self,parser,affectee,value):
        super(AffectationNode,self).__init__(parser)
        self.affectee = affectee
        self.value = value

class TryNode(Node):
    def __init__(self,parser,try_seq,ex_name,catch_seq):
        super(TryNode,self).__init__(parser)
        self.try_sequence = try_seq
        self.exception_name = ex_name
        self.catch_sequence = catch_seq

class EchoNode(Node):
    def __init__(self,parser):
        super(EchoNode,self).__init__(parser)
        self.expressions = []
        
    def add_expr(self,expr):
        self.expressions.append(expr)


class InputNode(Node):
    def __init__(self,parser,expr):
        super(InputNode,self).__init__(parser)
        self.desination = expr

class ValuedNode(Node):
    def __init__(self,parser,value,type):
        super(ValuedNode,self).__init__(parser)
        self.value=value
        self.type = type
        
class SequenceNode(Node):
    def __init__(self,parser):
        super(SequenceNode,self).__init__(parser)
        self.items=[]
    def add_item(self,item_node):
        self.items.append(item_node)

class AccessNode(Node):
    def __init__(self,parser,name,accessee):
        super(AccessNode,self).__init__(parser)

class SuperNode(Node):
    def __init__(self,parser,parent_name,args):
        super(SuperNode,self).__init__(parser)

class ArrayAccessorNode(Node):
    def __init__(self,parser,expr,subaccessor=None):
        super(ArrayAccessorNode,self).__init__(parser)

class CallNode(Node):
    def __init__(self,parser,name):
        super(CallNode,self).__init__(parser)
        self.arguments=[]
    def add_argument(self,arg):
        self.arguments.append(arg)

class EntryNode(Node):
    def __init__(self,parser):
        super(EntryNode,self).__init__(parser)
        
    def def_function(self,instrction_sequence):
        self.function = FunctionNode(self.parser)
        self.function.instruction_sequence = instrction_sequence
        