import lexemes.FloatLiteral
import lexemes.IntegerLiteral
import lexemes.StringLiteral
from lam_exceptions.SemanticError import SemanticError
from lam_exceptions.SyntacticError import SyntacticError
import ast
#For import node
import Parser
import Compiler


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
    
    def python_ast(self):
        main = []
        try:
            main = [self.main_entry.python_ast()]
        except:
            pass
        return ast.Module([s.python_ast() for s in self.children]+
                          main,lineno=self.line,col_offset=self.column)


    def add_import(self,import_node):
        self.children.append(import_node)

    def add_class(self,class_node):
        self.children.append(class_node)
        
    def add_entry(self, entry):
        self.main_entry = entry


class ImportNode(Node):
    def __init__(self,parser,name):
        Node.__init__(self,parser)
        self.name=name
        try:
            p = Parser.Parser(name+'.lam')
            compiler = Compiler.Compiler(p)
            compiler.compile()
        except IOError:
            pass #No lam module found, python modules will be sought by the python code
        except (SyntacticError,SemanticError) as se:
            print "In module "+name+": "
            raise se
    def python_ast(self):
        return ast.Import([ast.alias(self.name,None)],lineno=self.line,col_offset=self.column)

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
        ast_members = []
        for n in self.members:
            if n.__class__.__name__=="FunctionNode":
                n.method = True
            ast_members.append(n)
        ast_members = [n.python_ast() for n in self.members]
        ast_parents = [ast.Name(n,ast.Load(),lineno=self.line,col_offset=self.column) for n in self.parents]
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
        self.arguments = []
        self.name = name
        self.bound = bound
        self.method = False
        
    def add_parameter(self,name):
        self.arguments.append(name)

    def python_ast(self):
        decorators=[]
        iseq = []
        args = []
        if self.method:
            if self.name=="Thavron":
                self.name="__init__"
            args.append(ast.Name("self",ast.Param(),lineno=self.line,col_offset=self.column))
        if self.bound:
            if self.method:
                decorators.append(ast.Name('classmethod',ast.Load()))
            else:
                pass #TODO: Raise Semantic exception!
            
        if self.instruction_sequence:
            iseq = self.instruction_sequence.python_ast()

        return ast.FunctionDef(self.name,
                                ast.arguments(args+[ast.Name(name,ast.Param(),lineno=self.line,col_offset=self.column)
                                              for name in self.arguments],
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
        ptest = self.test.python_ast()
        pi = self.instructions.python_ast()
#        ptest,pi,lineno=self.line,col_offset=self.column
        last =  ast.While(lineno=self.line,col_offset=self.column)
        last.test = ptest
        last.body = pi
        last.orelse = []
        return last
    
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
        if self.left.__class__.__name__=="AccessRootNode":
            self.left.in_expr = True
        elif self.right.__class__.__name__=="AccessRootNode":
            self.right.in_expr = True
        
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


unary_operators_methods={'-':'USub','al':'Not'}
class UnaryOperatorNode(Node):
    def __init__(self,parser,operator,operand):
        Node.__init__(self,parser)
        self.operator=operator
        self.operand = operand
        if self.operand.__class__.__name__=="AccessRootNode":
            self.operand.in_expr=True
        
    def python_ast(self):
        os = self.operator.string
        return ast.UnaryOp(unary_operators_methods[os],operand.python_ast(),lineno=self.line,col_offset=self.column)

class AffectationNode(Node):
    def __init__(self,parser,affectee,value):
        Node.__init__(self,parser)
        self.affectee = affectee
        self.value = value
        if value.__class__.__name__ =="AccessRootNode":
            if value.node.__class__.__name__=="CallNode":
                value.node.affect=True
        
    def python_ast(self):
        return ast.Assign([self.affectee.python_ast()],self.value.python_ast(),lineno=self.line,col_offset=self.column)

class TryNode(Node):
    def __init__(self,parser,try_seq):
        Node.__init__(self,parser)
        self.try_sequence = try_seq
        self.catches = {}

    def add_catch(self,name,seq):
        if name=="":
            name = "#default#"
        self.catches[name] = seq

    def python_ast(self):
        
        te = ast.TryExcept(lineno=self.line,col_offset=self.column)
        te.handlers = []
        te.body= self.try_sequence.python_ast()
        for k,v in self.catches.items():
            if k=="#default#":
                eh = ast.ExceptHandler(lineno=self.line,col_offset=self.column)
                eh.type = None
                eh.name = None
                eh.body = v.python_ast()
                te.handlers.append(eh)
            else:
                eh = ast.ExceptHandler(lineno=self.line,col_offset=self.column)
                eh.type = ast.Name(k,ast.Load(),lineno=self.line,col_offset=self.column)
                eh.name = None
                eh.body = v.python_ast()
                te.handlers.append(eh)
        te.orelse = []
        return te

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
        self.affect=False
    def add_argument(self,arg):
        self.arguments.append(arg)

    def python_ast(self):
        call = ast.Call(self.child.python_ast(),
                        [n.python_ast() for n in self.arguments],
                        [],None,None,lineno=self.line,col_offset=self.column)
        if self.affect:
            return call
        else:
            return ast.Expr(call,lineno=self.line,col_offset=self.column)


class AccessNode(Node):
    def __init__(self,parser,name,accessee):
        Node.__init__(self,parser)
        self.mode = 'load' #default mode, access (as opposed to store for affectation)
        self.leaf = False
        if name=="sen":
            self.name = "self"
        else:
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
        self.in_expr = False
        if node.__class__.__name__=="SuperNode":
            self.node = node
            return
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
        node_list[0].leaf = True

        if new_root.__class__=='CallNode':
            new_root.child.mode=mode #The grammar guarantees new_root.child never is None
        else:
            new_root.mode = mode
        self.node = new_root


    def python_ast(self):
        if self.in_expr:
            self.node.affect = True
        return self.node.python_ast()

class SuperNode(Node):
    def __init__(self,parser,parent_name,method_name,args):
       Node.__init__(self,parser)
       self.parent_name = parent_name
       self.method_name = method_name
       if method_name=="" or method_name=="Thavron":
           self.method_name="__init__"
       self.args = args

    def python_ast(self):
        return ast.Expr(ast.Call(ast.Attribute(ast.Name(self.parent_name,ast.Load(),lineno=self.line,col_offset=self.column),self.method_name,ast.Load(),lineno=self.line,col_offset=self.column),[ast.Name("self",ast.Load(),lineno=self.line,col_offset=self.column)]+[n.python_ast() for n in self.args],[],None,None,lineno=self.line,col_offset=self.column),lineno=self.line,col_offset=self.column)

class ArrayAccessorNode(Node):
    def __init__(self,parser,expr,subaccessor=None):
        Node.__init__(self,parser)
        self.child = subaccessor
        self.index= expr
        self.mode = "load"

    def python_ast(self):
        sub = ast.Subscript(lineno=self.line,col_offset=self.column)
        sub.value = self.child.python_ast()
        sub.slice = ast.Index(self.index.python_ast())
        sub.ctx =  ast.Load(lineno=self.line,col_offset=self.column)
        if self.mode == "store":
            sub.ctx = ast.Store(lineno=self.line,col_offset=self.column)
        return sub

class EntryNode(Node):
    def __init__(self,parser):
        Node.__init__(self,parser)
        
    def python_ast(self):
        return ast.If(test=ast.Compare(left=ast.Name(id='__name__', ctx=ast.Load(),lineno=self.line,col_offset=self.column), ops=[ast.Eq(lineno=self.line,col_offset=self.column)],
                  comparators=[ast.Str(s='__main__',lineno=self.line,col_offset=self.column)],lineno=self.line,col_offset=self.column),
                  body=self.instruction_sequence.python_ast(), orelse=[],lineno=self.line,col_offset=self.column)

    def def_function(self,instrction_sequence):
        self.instruction_sequence = instrction_sequence
        