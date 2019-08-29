# Internet of Data implementation /Python3/

import os,sys

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
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        if callable(that): return self << Cmd(that) # wrap py fn
        self[that.val] = that ; return self
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

    # stack manipualtions

    def pop(self): return self.nest.pop(-1)
    def top(self): return self.nest[-1]

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

class Seq(Active,Vector): pass

class Doc(Frame): pass
class Color(Doc): pass
class Font(Doc): pass

class IO(Frame): pass
class Net(IO): pass
class Ip(Net): pass
class Port(Net): pass
class Web(Net):
    def __init__(self,V):
        Net.__init__(self,V)
        self['ip'] = Ip('127.0.0.1')
        self['port'] = Port(8888)
        self['back'] = Color('black')
        self['fore'] = Color('lightgreen')
        self['font'] = Font('monospace')
        self['font']['size'] = Sym('3mm')
    def eval(self,ctx):
        flask = __import__('flask')
        app = flask.Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        wtf     = __import__('flask_wtf')
        wtforms = __import__('wtforms')
        class CLI(wtf.FlaskForm):
            testcmd = '# put your commands here\n-01 +02.30 -4e+5 0xDeadBeef 0b1101'
            pad = wtforms.TextAreaField('pad',default=testcmd)
            go  = wtforms.SubmitField('GO')

        @app.route('/',methods=['GET','POST'])
        def index():
            form = CLI()
            if form.validate_on_submit():
                INTERP( ctx // Str(str(form.pad.data)) )
            return flask.render_template('index.html',ctx=ctx,web=self,form=form)

        @app.route('/<path>.png')
        def png(path):
            return app.send_static_file('%s.png' % path)

        app.run(host=self['ip'].val,port=self['port'].val,debug=True)

vm = VM('IoD')
vm['S'] = vm ; vm['W'] = vm

import ply.lex as lex

tokens = ['sym','num','int','hex','bin']

t_ignore = ' \t\r\n'
t_ignore_comment = r'[\#\\].*'

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)

def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)

def t_num(t):
    r'[+\-]?[0-9]+(\.[0-9]*)?([eE][+\-]?[0-9]+)?'
    return Num(t.value)

def t_sym(t):
    r'[^ \t\r\n\\\#]+'
    return Sym(t.value)

def t_error(t): raise SyntaxError(t)

lexer = lex.lex()

def WORD(ctx):
    token = lexer.token()
    if token: ctx // token
    return token

def FIND(ctx):
    token = ctx.pop()
    try: ctx // ctx[token.val]
    except KeyError: ctx // token ; return False
    return True

def INTERP(ctx):
    lexer.input(ctx.pop().val)
    while True:
        if not WORD(ctx): break
        if isinstance(ctx.top(),Sym):
            if not FIND(ctx): raise KeyError(ctx.top())
        print(ctx)

def WEB(ctx): ctx['WEB'] = Web(ctx.val) ; ctx['WEB'].eval(ctx)
vm << WEB
