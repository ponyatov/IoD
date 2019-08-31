# microPython port for embedded devices

import uos as os,sys

class Frame:
    def __init__(self,V):
        # type/class tag (required for PLY parser library)
        self.type = self.__class__.__name__.lower()
        # scalar value
        self.val  = V
        # slots = attributes = string-keyed associative array
        self.slot = {}
        # nested elements = vector = stack = queue
        self.nest = []
    
    # dump

    def __repr__(self): return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self._pad(depth) + self.head(prefix)
        if not depth: Frame._dumped = []
        if self in Frame._dumped: return tree + ' _/'
        else: Frame._dumped.append(self)
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest:
            tree += j.dump(depth+1)
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%.x' % (prefix,self.type,self._val(),id(self))
    def _pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self):
        return str(self.val)

    # operators

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        if callable(that): that = Cmd(that)
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        if callable(that): return self << Cmd(that) # wrap py fn
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

    # stack manipualtions

    def pop(self): return self.nest.pop(-1)
    def pip(self): return self.nest.pop(-2)
    def top(self): return self.nest[-1]
    def tip(self): return self.nest[-2]
    def dup(self): return self // self.top()
    def drop(self): self.pop() ; return self
    def swap(self): return self // self.pip()
    def over(self): return self // self.tip()
    def press(self): self.pip() ; return self
    def dropall(self): self.nest = [] ; return self

print( Frame('hello') // Frame('World') )

class Primitive(Frame):
    def eval(self,ctx): ctx // self

class Str(Primitive):
    def _val(self):
        s = ''
        for c in self.val:
            if c == '\t': s += '\\t'
            elif c == '\r': s += '\\r'
            elif c == '\n': s += '\\n'
            else: s += c
        return s

class Sym(Primitive): pass

class Num(Primitive):
    def __init__(self,V): Primitive.__init__(self,float(V))
class Int(Num):
    def __init__(self,V): Primitive.__init__(self,int(V))
    def todec(self): return Int(self.val)
    def tohex(self): return Hex(hex(self.val))
    def tobin(self): return Bin(bin(self.val))
class Hex(Int):
    def __init__(self,V): Primitive.__init__(self,int(V[2:],0x10))
    def _val(self): return hex(self.val)
class Bin(Int):
    def __init__(self,V): Primitive.__init__(self,int(V[2:],0x02))
    def _val(self): return bin(self.val)

class Container(Frame): pass

class Vector(Container): pass
class Stack(Container): pass
class Dict(Container): pass
class Queue(Container): pass

class Active(Frame): pass
    
class VM(Active): pass

class Cmd(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def eval(self,ctx):
        self.fn(ctx)

vm = VM('IoD')
vm['S'] = vm ; vm['W'] = vm

print(vm)

def BYE(ctx): sys.exit(0)
vm << BYE

def DUP(ctx): ctx.dup()
vm << DUP
def DROP(ctx): ctx.drop()
vm << DROP
def SWAP(ctx): ctx.swap()
vm << SWAP
def OVER(ctx): ctx.over()
vm << OVER
def PRESS(ctx): ctx.press()
vm << PRESS
def DOT(ctx): ctx.dropall()
vm['.'] = DOT

def DEC(ctx): ctx // ctx.pop().todec()
vm << DEC
def HEX(ctx): ctx // ctx.pop().tohex()
vm << HEX
def BIN(ctx): ctx // ctx.pop().tobin()
vm << BIN

import ure as re
class Lexer(Frame):
    def input(self,src): self.src = src
    def token(self):
        if not self.src: return None
        token = ''
        def sym(): self.src = self.src[1:]
        while self.src[0] in ' \t\r\n':
            sym()
        while self.src and self.src[0] not in ' \t\r\n':
            token += self.src[0] ; sym()
        if re.match(r'[+\-]?[0-9]+',token): return Int(token)
        return Sym(token)
lexer = Lexer('metaL')

def WORD(ctx):
    token = lexer.token()
    if token: ctx // token
    return token

def FIND(ctx):
    token = ctx.pop()
    try: ctx // ctx[token.val]
    except KeyError:
        try: ctx // ctx[token.val.upper()]
        except KeyError: ctx // token ; return False
    return True

def EXEC(ctx): ctx.pop().eval(ctx)

def INTERP(ctx):
    lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(),Sym):
            if not FIND(ctx): raise KeyError(ctx.top())
            EXEC(ctx)
        print(ctx)

def REPL():
    while True:
        try: vm // Str(input('ok> '))
        except EOFError: print('BYE\n') ; BYE(vm)
        INTERP(vm)
REPL()
