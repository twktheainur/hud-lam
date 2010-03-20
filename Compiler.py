import imp
import marshal
import struct
import ast
import os
import time
class Compiler(object):
    def __init__(self,parser):
        self.name=parser.name
        self.parser = parser
        self.magic = imp.get_magic()

    def __pyc_exists(self):
        try:
            self.pyc = open(self.name+".pyc","rb")
            return True
        except:
            return False

    def compile(self):
        if self.__pyc_exists():
            print self.pyc.read(4) #Python Magic number
            pyctime = self.pyc.read(4)
            print len(pyctime)
            pyctime = struct.unpack('<i', pyctime)
            srctime = os.path.getmtime(self.name+".lam")
            if(srctime<=pyctime[0]):
                self.code = marshal.load(self.pyc)
            else:
                self.__generate_code_object()
                self.__write_pyc()
        else:
            self.__generate_code_object()
            self.__write_pyc()
        return self.code

    def __generate_code_object(self):
        self.ast = self.parser.generate_py_ast()
        print ast.dump(self.ast,True,True)
        self.code = compile(ast.fix_missing_locations((self.ast)),self.name+".py","exec")

    def __write_pyc(self):
        pyc = open(self.name+".pyc","wb")
        pyc.write(self.magic)
        mtime = time.time()
        mtime = struct.pack('<i', mtime)
        pyc.write(mtime)
        marshal.dump(self.code,pyc)
        self.pyc = pyc
        