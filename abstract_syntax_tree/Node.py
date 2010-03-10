import lexemes.FloatLiteral
import lexemes.IntegerLiteral
import lexemes.StringLiteral
from lam_exceptions.SemanticError import SemanticError
from lam_exceptions.SyntacticError import SyntacticError
import types
import sys
import Parser
import ast

class Node(object):
    def __init__(self,parser):
        self.line=parser.lexer.state.line
        self.column=parser.lexer.state.line
        self.parser = parser
    def python_ast(self):
        pass
    def semantic_check(self):
        return true

class ModuleNode(Node):
    def __init__(self,parser):
        super(ModuleNode,self).__init__(parser)
        self.name= parser.mod_name()
        self.children = []
        self.main_entry=None
        self.global_context={} 

    def type(self):
        return "<module>"
    
    def python_ast(self):
        return ast.Module([s.python_ast() for s in self.children]+
                          [self.main_entry.python_ast()])

    def module(self):
        return types.ModuleType(str(self.name))

    def add_import(self,import_node):
#        self.__register_global(import_node.name,import_node.python_mod)
        self.children.append(import_node)

    def add_class(self,class_node):
        self.children.append(class_node)
        
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
            self.python_mod = p.generate_py_ast()
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

    def python_ast(self):
        ast_members = [n.python_ast() for n in self.members]
        ast_parents = [ast.Name(n,ast.Load()) for n in self.parents]
        return ast.ClassDef(self.name,ast_parents,ast_members,[],lineno=self.line,col_offset=self.column)

class InstructionSequenceNode(Node):
    def __init__(self,parser):
        super(InstructionSequenceNode,self).__init__(parser)
        self.instructions = []
    def python_ast(self):
        return [i.python_ast() for i in self.instructions]
         
    def add_instruction(self,instr_node):
        self.instructions.append(instr_node)

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
        
    def python_ast(self):
        os = self.operator.string
        op = getattr(ast,binary_operators_methods[os])
        if os== '+' or os=='-' or os=='/' or os=='*' or os=='%':
            return ast.BinOp(left.python_ast(),op,right.python_ast(),lineno=self.line,col_offset=self.column)
        elif os=='a' :
            return ast.BoolOP(left.python_ast(),op,right.python_ast(),lineno=self.line,col_offset=self.column)
        else:
            return ast.Compare(left.python_ast(),[op],[right.python_ast()],lineno=self.line,col_offset=self.column)

    def semantic_check(self):
        pass

    def type(self):
        return left.type()



class UnaryOperatorNode(Node):
    def __init__(self,parser,operator,operand):
        super(UnaryOperator,self).__init__(parser)
        self.operator=operator
        self.operand = operand
        
    def python_ast(self):
        os = self.operator.string
        return ast.UnaryOp(unary_operators_methods[os],operand.python_ast(),lineno=self.line,col_offset=self.column)

class AffectationNode(Node):
    def __init__(self,parser,affectee,value):
        super(AffectationNode,self).__init__(parser)
        self.affectee = affectee
        self.value = value
        
    def python_ast(self):
        if value.__class__=="CallNode" or value.is_call:
            py_value = value.python_ast()
        return ast.Assign([affectee.python_ast()],py_value,lineno=self.line,col_offset=self.column)

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

    def python_ast(self):
        values = []
        for ex in self.expressions:
            values.append(ex.python_ast())
        return ast.Print(None,values,False)
        
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
        
    def python_ast(self):
        val = None
        if self.type==lexemes.StringLiteral.StringLiteral:
            return ast.Str(self.value[1:len(self.value)-1],lineno=self.line,col_offset=self.column)
        elif self.type==lexemes.IntegerLiteral.IntegerLiteral:
            val = int(self.value)
        elif self.type==lexemes.FloatLiteral.FloatLiteral:
            val = float(self.value)
        return ast.Num(val,lineno=self.line,col_offset=self.column)
        
class SequenceNode(Node):
    def __init__(self,parser):
        super(SequenceNode,self).__init__(parser)
        self.items=[]
    def add_item(self,item_node):
        self.items.append(item_node)

class CallNode(Node):
    def __init__(self,parser):
        super(CallNode,self).__init__(parser)
        self.arguments=[]
        self.child = None
        self.name='call'
    def add_argument(self,arg):
        self.arguments.append(arg)

    def python_ast(self):
        return ast.Call(self.child.python_ast(),
                        [n.python_ast() for n in self.arguments],
                        [],None,None,lineno=self.line,col_offset=self.column)


class AccessNode(Node):
    def __init__(self,parser,name,accessee):
        super(AccessNode,self).__init__(parser)
        self.mode = 'load' #default mode, access (as opposed to store for affectation)
        self.leaf = False
        self.name = name
        self.child = accessee

    def python_ast(self):
        print "access"
        pmode = ast.Load()
        if self.mode=='store':
            pmode = ast.Store()
        if self.leaf:
            return ast.Name(self.name,pmode,lineno=self.line,col_offset=self.column)
        else:
            return ast.Attribute(self.child.python_ast(),self.name,pmode,lineno=self.line,col_offset=self.column)
    

class AccessRootNode(Node):
    def __init__(self,parser,node,mode):
        super(AccessRootNode,self).__init__(parser)
        # either 'store' or 'load'.
        #if store the last python
        #Attribute Node will be in Store() mode
        self.mode = mode

        current_node = node
        node_list = []
        #Building a list of subnodes in their parsing order of appearence.
        #The part of the tree representing access statements
        #are in fact equivalent to chained lists which makes this possible.
        #Also CallNode and AccessNode both posses a
        while current_node!=None:
            node_list.append(current_node)
            current_node=current_node.child
        #Building a new list in inverse order compared to the parse order,
        #order which is compliant with the one used in the python AST
        i = len(node_list)-1
        new_root = node_list[i]
        current_root = new_root
        i-=1
        while i>=0:
            current_root.child = node_list[i]
            current_root=current_root.child
            i-=1
        current_root.child = None
        current_root.leaf = True

        if new_root.__class__=='CallNode':
            new_root.child.mode=mode #The grammar guarantees new_root.child never is None
        else:
            new_root.mode = mode
        self.node = new_root

    def python_ast(self):
        print "Node:",self.node
        return self.node.python_ast()

class SuperNode(Node):
    def __init__(self,parser,parent_name,args):
        super(SuperNode,self).__init__(parser)

class ArrayAccessorNode(Node):
    def __init__(self,parser,expr,subaccessor=None):
        super(ArrayAccessorNode,self).__init__(parser)

class EntryNode(Node):
    def __init__(self,parser):
        super(EntryNode,self).__init__(parser)
        
    def python_ast(self):
        return ast.If(test=ast.Compare(left=ast.Name(id='__name__', ctx=ast.Load()), ops=[ast.Eq()],
                  comparators=[ast.Str(s='__main__')]),
                  body=self.instruction_sequence.python_ast(), orelse=[],lineno=self.line,col_offset=self.column)

    def def_function(self,instrction_sequence):
        self.instruction_sequence = instrction_sequence
        