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
    """
      Base node class, store the line and column
      corresponding to the actual code in the source file
      in order to allow to locate semantic errors.
    """
    def __init__(self,parser):
        self.line=parser.lexer.state.line
        self.column=parser.lexer.state.line
        self.parser = parser
    def python_ast(self):
        pass

class ModuleNode(Node):
    def __init__(self,parser):
        Node.__init__(self,parser)
        self.name= parser.mod_name()
        self.children = []
        self.main_entry=None
        self.global_context={} 
    
    def python_ast(self):
        return ast.Module([s.python_ast() for s in self.children]+
                          [self.main_entry.python_ast()],lineno=self.line,col_offset=self.column)

    def module(self):
        return types.ModuleType(str(self.name))

    def add_import(self,import_node):
        self.children.append(import_node)

    def add_class(self,class_node):
        self.children.append(class_node)
        
    def add_entry(self, entry):
        self.main_entry = entry

    def __register_global(self,name,item):
        self.global_context.update({name:item})

#TODO: IMPORTANT find a way to handle import of other hudlam modules...
class ImportNode(Node):
    def __init__(self,parser,name):
        Node.__init__(self,parser)
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
        Node.__init__(self,parser)
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
        Node.__init__(self,parser)
        self.instructions = []
    def python_ast(self):
        return [i.python_ast() for i in self.instructions]
         
    def add_instruction(self,instr_node):
        self.instructions.append(instr_node)

class FunctionNode(Node):
    def __init__(self,parser,name,bound):
        Node.__init__(self,parser)
        self.instruction_sequence = None
        self.parameters = []
        self.name = name
        self.bound = bound
        
    def add_parameter(self,name):
        self.parameters.append(name)

    def python_ast(self):
        decorators=[]
        iseq = []
        if self.instruction_sequence:
            iseq = self.instruction_sequence.python_ast()
        if self.bound:
            decorators.append(ast.Name('classmethod',ast.Load()))
        return ast.FunctionDef(self.name,
                                ast.arguments([ast.Name(name,ast.Param())
                                              for name in self.parameters],
                                              None,None,[]),
                                iseq,decorators,lineno=self.line,col_offset=self.column)
class ForInNode(Node):
    def __init__(self,parser,var_name,seq_node,instr_seq):
        Node.__init__(self,parser)
        self.var  = var_name
        self.sequence = seq_node
        self.instructions = instr_seq

    def python_ast(self):
        return ast.For(ast.Name(self.var,ast.Store(),lineno=self.line,col_offset=self.column),
                       self.sequence.python_ast(),
                       self.instructions.python_ast(),[],lineno=self.line,col_offset=self.column)

class ForIfNode(Node):
    def __init__(self,parser,test,instr_seq):
        Node.__init__(self,parser)
        self.test = test
        self.instructions = instr_seq

    def python_ast(self):
        return ast.While(test.python_ast(),self.instructions,[],lineno=self.line,col_offset=self.column)

class IfNode(Node):
    def __init__(self,parser,test,iftrue,orelse):
        Node.__init__(self,parser)
        self.test = test
        self.iftrue = iftrue
        self.orelse=orelse
        
    def python_ast(self):
        test = self.test.python_ast()
        try:
            iftrue = self.iftrue.python_ast()
        except:
            iftrue = []
        try:
            orelse = self.orelse.python_ast()
        except:
            orelse = []
        return ast.If(test,iftrue,orelse,lineno=self.line,col_offset=self.column)

binary_operators_methods={'+':'Add','-':'Sub','%':'Mod','*':'Mult','/':'Div',\
                          '==':'Eq','!=':'NotEq','>':'Gt','>=':'GtE','<':'Lt',\
                          '<=':'lteq','a':'And','egor':'Or'}
class BinaryOperatorNode(Node):
    def __init__(self,parser,left,operator,right):
        Node.__init__(self,parser)
        self.operator=operator
        self.left=left
        self.right=right
        
    def python_ast(self):
        os = self.operator
        op = getattr(ast,binary_operators_methods[os])(lineno=self.line,col_offset=self.column)
        if os== '+' or os=='-' or os=='/' or os=='*' or os=='%':
            return ast.BinOp(self.left.python_ast(),op,self.right.python_ast(),lineno=self.line,col_offset=self.column)
        elif os=='a' :
            return ast.BoolOP(self.left.python_ast(),op,self.right.python_ast(),lineno=self.line,col_offset=self.column)
        else:
            return ast.Compare(self.left.python_ast(),[op],[self.right.python_ast()],lineno=self.line,col_offset=self.column)

    def semantic_check(self):
        pass

    def type(self):
        return left.type()



class UnaryOperatorNode(Node):
    def __init__(self,parser,operator,operand):
        Node.__init__(self,parser)
        self.operator=operator
        self.operand = operand
        
    def python_ast(self):
        os = self.operator.string
        return ast.UnaryOp(unary_operators_methods[os],operand.python_ast(),lineno=self.line,col_offset=self.column)

class AffectationNode(Node):
    def __init__(self,parser,affectee,value):
        Node.__init__(self,parser)
        self.affectee = affectee
        self.value = value
        
    def python_ast(self):
        return ast.Assign([self.affectee.python_ast()],self.value.python_ast(),lineno=self.line,col_offset=self.column)

class TryNode(Node):
    def __init__(self,parser,try_seq,ex_name,catch_seq):
        Node.__init__(self,parser)
        self.try_sequence = try_seq
        self.exception_name = ex_name
        self.catch_sequence = catch_seq

    def python_ast(self):
        return ast.TryExcept(self.try_sequence.python_ast(),[ast.ExceptHandler(ex_name,ast.Load())],None, self.catch_sequence.python_ast(),lineno=self.line,col_offset=self.column)

class EchoNode(Node):
    def __init__(self,parser):
        Node.__init__(self,parser)
        self.expressions = []

    def python_ast(self):
        values = []
        for ex in self.expressions:
            values.append(ex.python_ast())
        return ast.Print(None,values,False,lineno=self.line,col_offset=self.column)
        
    def add_expr(self,expr):
        self.expressions.append(expr)


class InputNode(Node):
    def __init__(self,parser,expr):
        Node.__init__(self,parser)
        self.prompt = expr

    def python_ast(self):
        return ast.Call(ast.Name('raw_input',
                                           ast.Load(),
                                           lineno=self.line,col_offset=self.column),
                                 [self.prompt.python_ast()],
                                 [],None,None,
                                 lineno=self.line,col_offset=self.column)

class ValuedNode(Node):
    def __init__(self,parser,value,type):
        Node.__init__(self,parser)
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
        Node.__init__(self,parser)
        self.items=[]
    def add_item(self,item_node):
        self.items.append(item_node)

    def python_ast(self):
        return ast.List([n.python_ast() for n in self.items],ast.Load(),lineno=self.line,col_offset=self.column)

class CallNode(Node):
    def __init__(self,parser):
        Node.__init__(self,parser)
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
        Node.__init__(self,parser)
        self.mode = 'load' #default mode, access (as opposed to store for affectation)
        self.leaf = False
        self.name = name
        self.child = accessee

    def python_ast(self):
        pmode = ast.Load(lineno=self.line,col_offset=self.column)
        if self.mode=='store':
            pmode = ast.Store(lineno=self.line,col_offset=self.column)
        if self.leaf:
            return ast.Name(self.name.encode('ascii','ignore'),pmode,lineno=self.line,col_offset=self.column)
        else:
            return ast.Attribute(self.child.python_ast(),self.name,pmode,lineno=self.line,col_offset=self.column)
    

class AccessRootNode(Node):
    def __init__(self,parser,node,mode):
        Node.__init__(self,parser)
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
        return self.node.python_ast()

class SuperNode(Node):
    def __init__(self,parser,parent_name,method_name,args):
       Node.__init__(self,parser)
       self.parent_name = parent_name
       self.method_name = method_name
       if method_name=="":
           self.method_name="__init__"
       self.args = args

    def python_ast(self):
        return ast.Call(ast.Attribute(Name(self.parent_name,ast.Load(),lineno=self.line,col_offset=self.column),self.method_name,ast.Load(),lineno=self.line,col_offset=self.column),[n.python_ast() for n in self.args],[],None,None,lineno=self.line,col_offset=self.column)

class ArrayAccessorNode(Node):
    def __init__(self,parser,expr,subaccessor=None):
        Node.__init__(self,parser)
        self.child = subaccessor
        self.index= expr
        self.mode = "load"

    def python_ast(self):
        acc_mode = ast.Load(lineno=self.line,col_offset=self.column)
        if self.mode == "store":
            acc_mode = ast.Store(lineno=self.line,col_offset=self.column)
        return ast.Subscript(self.child.python_ast(),ast.Index(self.index.python_ast(),acc_mode),lineno=self.line,col_offset=self.column)


class EntryNode(Node):
    def __init__(self,parser):
        Node.__init__(self,parser)
        
    def python_ast(self):
        return ast.If(test=ast.Compare(left=ast.Name(id='__name__', ctx=ast.Load(),lineno=self.line,col_offset=self.column), ops=[ast.Eq(lineno=self.line,col_offset=self.column)],
                  comparators=[ast.Str(s='__main__',lineno=self.line,col_offset=self.column)],lineno=self.line,col_offset=self.column),
                  body=self.instruction_sequence.python_ast(), orelse=[],lineno=self.line,col_offset=self.column)

    def def_function(self,instrction_sequence):
        self.instruction_sequence = instrction_sequence
        